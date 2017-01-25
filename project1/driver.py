import sys, collections
import os, time

class State:
    def __init__(self, board, path, depth):
        self.board = board
        self.path = path
        self.hole_index = self.board.index(0)
        self.depth = depth

    def __str__(self):
        return "".join(map(str,self.board))

class Solver:
    def __init__(self):
        self.solved_board = None
        self.move_dict = self.create_move_dict()
        self.board_width = 3
        self.methods = {'bfs': self.bfs, 'dfs': self.dfs, 'ast': self.ast, 'ida': self.ida}

    def run(self, search_method, board_start):
        self.solved_board = sorted(board_start)

        start_time = time.time()

        f = self.methods[search_method]
        f(board_start)

        end_time = time.time()
        print "time_elapsed: " + str(end_time-start_time)

    def get_children(self, state):
        """Get children of input state in UDLR order"""
        children = []
        for (destination_i, move_name) in self.move_dict[state.hole_index]:
            child_board = self.move_result(state.board, state.hole_index, destination_i)
            child = State(child_board, state.path + move_name, state.depth+1)
            children.append(child)
        return children

    def move_result(self, board, hole_index, destination_index):
        """Get the result of moving the hole (0) to the destination index
        Returns a list representing the new board"""
        board = list(board)
        destination_value = board[destination_index]
        board[destination_index] = 0
        board[hole_index] = destination_value
        return board

    def create_move_dict(self):
        d = {}
        for hole_index in range(9):
            moves = []
            for (move_i, move_name) in [(-3+hole_index, "U"),(3+hole_index, "D")]:
                if 0 <= move_i <= 8:
                    moves.append( (move_i, move_name))
            for (move_i, move_name) in [(-1+hole_index, "L"),(1+hole_index, "R")]:
                if hole_index // 3 == move_i // 3:
                    moves.append( (move_i, move_name) )
            d[hole_index] = moves
        return d 

    def bfs(self, board):
        root = State(board,"",0)
        queue = collections.deque()
        queue.append(root)

        visited = set()
        in_queue = set()

        in_queue.add( str(root) )

        nodes_expanded = 0
        max_fringe_size = 0
        max_depth = 0

        while len(queue):
            max_fringe_size = max(max_fringe_size, len(queue))
            #print nodes_expanded
            curr = queue.popleft()

            in_queue.remove( str(curr) )

            if curr.board == self.solved_board:
                print "-------SOLVED WITH BREADTH--------"
                print "path_to_goal:" + str(curr.path)
                print "cost_of_path: " + str(len(curr.path))
                print "nodes_expanded: " + str(nodes_expanded)
                print "fringe_size: " + str(len(queue))
                print "max_fringe_size: " + str(max_fringe_size)
                print "search_depth: " + str(len(curr.path))
                print "max_search_depth: " + str(max_depth)
                return

            else:
                visited.add( str(curr) )
                nodes_expanded += 1

                for child in self.get_children(curr):
                    child_str = str(child)
                    if child_str not in in_queue and child_str not in visited:
                        max_depth = max(max_depth, child.depth)
                        queue.append(child)
                        in_queue.add(child_str)

    def dfs(self,board):
        root = State(board,"",0)
        stack = [root]

        visited = set()
        on_stack = set()

        on_stack.add( str(root) )

        nodes_expanded = 0
        max_fringe_size = 0
        max_depth = 0

        while stack:
            max_fringe_size = max(max_fringe_size, len(stack))
            #print nodes_expanded
            curr = stack.pop()

            on_stack.remove( str(curr) )

            if curr.board == self.solved_board:
                print "-------SOLVED WITH DEPTH--------"
                print "path_to_goal:" + str(curr.path)
                print "cost_of_path: " + str(len(curr.path))
                print "nodes_expanded: " + str(nodes_expanded)
                print "fringe_size: " + str(len(stack))
                print "max_fringe_size: " + str(max_fringe_size)
                print "search_depth: " + str(len(curr.path))
                print "max_search_depth: " + str(max_depth)
                return

            else:
                visited.add( str(curr) )
                nodes_expanded += 1

                for child in self.get_children(curr)[::-1]:
                    child_str = str(child)
                    if child_str not in on_stack and child_str not in visited:
                        max_depth = max(max_depth, child.depth)
                        stack.append(child)
                        on_stack.add(child_str)


    def ast(self):
        pass

    def ida(self):
        pass


def main():
    args = sys.argv
    chosen_method = args[1]
    board_start = map(int,args[2].split(","))

    sol = Solver()
    sol.run(chosen_method, board_start)

if __name__ == "__main__":
    main()