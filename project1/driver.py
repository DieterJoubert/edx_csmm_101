import sys, collections, time, math, resource, Queue

class State:
    def __init__(self, board, depth, parent=None):
        self.board = board
        self.hole_index = self.board.index(0)
        self.depth = depth
        self.parent = parent

    def __str__(self):
        return str(self.board)

class Solver:
    def __init__(self, selected_method, board_start):
        self.selected_method = selected_method
        self.methods = {'bfs': self.bfs, 'dfs': self.dfs, 'ast': self.ast, 'ida': self.ida}

        #initial data
        self.solved_board = sorted(board_start)
        self.board_start = board_start
        self.board_width = int(math.sqrt(max(board_start)+1))
        self.move_dict = self.create_move_dict()

        #running data
        self.visited = set()
        self.frontier = set()

        #overview metadata
        self.nodes_expanded = 0
        self.max_fringe_size = 0
        self.max_search_depth = 0
        self.max_ram_usage = 0

        #solution metadata
        self.path = []
        self.cost_of_path = None
        self.fringe_size = None
        self.search_depth = None

    def run(self):
        start_time = time.time()

        f = self.methods[self.selected_method]
        result = f(self.board_start)

        running_time = time.time() - start_time
        result = [self.path, self.cost_of_path, self.nodes_expanded, self.fringe_size, self.max_fringe_size, 
                    self.search_depth, self.max_search_depth, running_time, self.max_ram_usage]
        for item in result:
            print item
        return result

    def get_children(self, state):
        """Get children of input state in UDLR order"""
        children = []
        for (destination_i, move_name) in self.move_dict[state.hole_index]:
            child_board = self.move_result(state.board, state.hole_index, destination_i)
            child = State(child_board, state.depth+1, state)
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
        for hole_index in range(len(self.board_start)):
            moves = []
            for (move_i, move_name) in [(-self.board_width+hole_index, "U"),(self.board_width+hole_index, "D")]:
                if 0 <= move_i <= max(self.board_start):
                    moves.append( (move_i, move_name))
            for (move_i, move_name) in [(-1+hole_index, "L"),(1+hole_index, "R")]:
                if hole_index // self.board_width == move_i // self.board_width:
                    moves.append( (move_i, move_name) )
            d[hole_index] = moves
        return d 

    def get_path(self, curr_state):
        """Backtrack from the solution State to the root, in order to find the path"""
        path = []
        move_name = {-self.board_width: 'Up', self.board_width: 'Down', -1: 'Left', 1: 'Right'}

        while curr_state.parent:
            diff = curr_state.hole_index - curr_state.parent.hole_index 
            path = [move_name[diff]] + path
            curr_state = curr_state.parent
        return path

    def manhattan_score(self, state):
        score = 0

        for i in range(len(state.board)):
            tile = state.board[i]
            dist = abs(tile-i)

            v_moves = int(dist / self.board_width)
            h_moves = dist % self.board_width

            score += v_moves + h_moves

        return score

    def bfs(self, board):
        root = State(board,0)
        queue = collections.deque()
        queue.append(root)

        self.frontier.add( str(root) )

        while len(queue):
            self.max_ram_usage = max(self.max_ram_usage, resource.getrusage(resource.RUSAGE_SELF)[2] * 0.000001)
            self.max_fringe_size = max(self.max_fringe_size, len(queue))

            curr = queue.popleft()

            self.frontier.remove( str(curr) )

            if curr.board == self.solved_board:
                self.path = self.get_path(curr)
                self.cost_of_path = len(self.path)
                self.fringe_size = len(queue)
                self.search_depth = curr.depth
                return

            else:
                self.visited.add( str(curr) )
                self.nodes_expanded += 1

                for child in self.get_children(curr):
                    child_str = str(child)
                    if child_str not in self.frontier and child_str not in self.visited:
                        queue.append(child)
                        self.frontier.add(child_str)

                        self.max_search_depth = max(self.max_search_depth, child.depth)

    def dfs(self,board):
        root = State(board,0)
        stack = [root]

        self.frontier.add( str(root) )

        while stack:
            self.max_ram_usage = max(self.max_ram_usage, resource.getrusage(resource.RUSAGE_SELF)[2] * 0.000001)
            self.max_fringe_size = max(self.max_fringe_size, len(stack))

            curr = stack.pop()
            self.frontier.remove( str(curr) )

            if curr.board == self.solved_board:
                self.path = self.get_path(curr)
                self.cost_of_path = len(self.path)
                self.fringe_size = len(stack)
                self.search_depth = curr.depth
                return

            else:
                self.visited.add( str(curr) )
                self.nodes_expanded += 1

                for child in self.get_children(curr)[::-1]:
                    child_str = str(child)
                    if child_str not in self.frontier and child_str not in self.visited:
                        stack.append(child)
                        self.frontier.add(child_str)

                        self.max_search_depth = max(self.max_search_depth, child.depth)

    def ast(self, board):
        root = State(board,0)
        q = Queue.PriorityQueue()
        q.put( (self.manhattan_score(root), root) )

        self.frontier.add( str(root) )

        while q.qsize() > 0:
            self.max_ram_usage = max(self.max_ram_usage, resource.getrusage(resource.RUSAGE_SELF)[2] * 0.000001)
            self.max_fringe_size = max(self.max_fringe_size, q.qsize())

            curr = q.get()[1]

            self.frontier.remove( str(curr) )

            if curr.board == self.solved_board:
                self.path = self.get_path(curr)
                self.cost_of_path = len(self.path)
                self.fringe_size = q.qsize()
                self.search_depth = curr.depth
                return

            else:
                self.visited.add( str(curr) )
                self.nodes_expanded += 1

                for child in self.get_children(curr):
                    child_str = str(child)
                    if child_str not in self.frontier and child_str not in self.visited:
                        q.put( (child.depth + self.manhattan_score(child), child) )
                        self.frontier.add(child_str)

                        self.max_search_depth = max(self.max_search_depth, child.depth)

    def ida(self):
        pass

def main():
    args = sys.argv
    selected_method = args[1]
    board_start = map(int,args[2].split(","))

    sol = Solver(selected_method,  board_start)
    result = sol.run()

    out = open("output.txt","w")
    fields = ['path_to_goal', 'cost_of_path', 'nodes_expanded', 
              'fringe_size', 'max_fringe_size', 'search_depth', 
              'max_search_depth', 'running_time', 'max_ram_usage']

    for line in map(lambda x: str(x[0]) + ": " + str(x[1]), zip(fields, result)):
        out.write(line + "\n")
    out.close()

if __name__ == "__main__":
    main()