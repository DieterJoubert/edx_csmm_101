import sys, collections

solved_board = [0,1,2,3,4,5,6,7,8]

def solved(board):
    """Check if the board is in solved state"""
    return board == list(range(9))

def possible_moves(board):
    """Get the indices to where the hole can be moved with the name of the moves"""
    hole_index = board.index(0)
    moves = []

    for (move_i, move_name) in [(-3+hole_index, "Up"),(3+hole_index, "Down")]:
        if 0 <= move_i <= 8:
            moves.append( (move_i, move_name))

    for (move_i, move_name) in [(-1+hole_index, "Left"),(1+hole_index, "Right")]:
        if hole_index // 3 == move_i // 3:
            moves.append( (move_i, move_name) )

    return moves

def move(board, destination_index):
    """Move the hole (0) to the destination index"""
    board = list(board)
    hole_index = board.index(0)
    destination_value = board[destination_index]
    board[destination_index] = 0
    board[hole_index] = destination_value
    hole_index = destination_index
    return board

def bfs(board):
    global solved_board

    q = collections.deque()
    q.append((board, []))
    visited = set()
    queued_up = set()
    queued_up.add(tuple(board))

    nodes_expanded = 0

    while len(q):
        print "ITE"
        curr_board, curr_path = q.popleft()

        queued_up.remove(tuple(curr_board))

        if curr_board == solved_board:
            print "-------SOLVED--------"
            print curr_path
            print "nodes expanded: " + str(nodes_expanded)
            return


        else:
            visited.add(tuple(curr_board))
            nodes_expanded += 1

            for (move_i, move_name) in possible_moves(curr_board):
                new_board = move(curr_board, move_i)
                new_t = tuple(new_board)
                if new_t not in queued_up and new_t not in visited:
                    q.append( (new_board, curr_path + [move_name]))
                    queued_up.add(tuple(new_board))

def dfs(board):
    pass

def ast(board):
    pass

def ida(board):
    pass

def main():
    args = sys.argv
    chosen_method = args[1]
    starter_board = map(int,args[2].split(","))

    methods = {'bfs': bfs, 'dfs': dfs, 'ast': ast, 'ida': ida}

    f = methods[chosen_method]
    f(starter_board)    

if __name__ == "__main__":
    main()