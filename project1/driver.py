import sys



def main():
    args = sys.argv

    method = args[1]
    starter_board = map(int,args[2].split(","))

    print method
    print starter_board

    methods = {'bfs': bfs, 'dfs': dfs, 'ast': ast, 'ida': ida}

if __name__ == "__main__":
    main()