class EightPuzzle:

    def __init__(self, board):
        self.board = board
        print board
        self.width = 3
        self.hole_index = board.index(0)
        self.visited = {}

    def solved(self):
        """Check if the board is in solved state"""
        return self.board == list(range(9))

    def possible_moves(self):
        """Get the indices to where the hole can be moved"""
        destinations = map(lambda x: self.hole_index + x, [-3, 3, -1, 1])
        destinations = [x for x in destinations if 0 <= x <= 8]
        return destinations

    def move(self, destination_index):
        """Move the hole (0) to the destination index"""
        destination_value = self.board[destination_index]
        self.board[destination_index] = 0
        self.board[self.hole_index] = destination_value
        self.hole_index = destination_index

    def __str__(self):
        s = " ".join(map(str,self.board[:3])) + "\n"
        s += " ".join(map(str,self.board[3:6])) + "\n"
        s += " ".join(map(str,self.board[6:]))
        return s










def main():

    print "---------TEST------------"

    p = EightPuzzle(starter_board)
    print p
    print p.possible_moves()

    print "-------------"
    p.move(1)
    print p
    print p.hole_index
    print p.possible_moves()

    print "-------------"
    p.move(4)
    print p
    print p.hole_index
    print p.possible_moves()


    print "------------------------------------"