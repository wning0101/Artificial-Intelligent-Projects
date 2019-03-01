# Ching-Wei Lin
# CS541 assign 1
# This is a 3.7 version Python program
# Operation Instruction:
# 1.Enter which algorithm do you want to use?(enter 1 or 2) 1.Best-First Search 2.A* search
# 2.Enter which heuristic do you want to use?(enter 1, 2, or 3) (1)h1 (2)h2 (3)h3
# 3.Enter the initial state. For example: 41b763528

class Node:
    def __init__(self, data, level, fval):
        """ Initialize the node with the data, level of the node and the calculated fvalue """
        self.data = data
        self.level = level
        self.fval = fval


    def generate_child(self):
        """ Generate child nodes from the given node by moving the blank space
            either in the four directions {up,down,left,right} """
        for i in range(len(self.data)):
            for j in range(len(self.data)):
                if self.data[i][j] == 'b':
                    x = i
                    y = j

        """ val_list contains position values for moving the blank space in either of
            the 4 directions [up,down,left,right] respectively. """
        next_list = [[x, y - 1], [x, y + 1], [x - 1, y], [x + 1, y]]
        next_level = []
        for i in next_list:
            temp = self.shuffle(self.data, x, y, i[0], i[1])
            if temp is not None:
                child_node = Node(temp, self.level + 1, 0)
                next_level.append(child_node)
        return next_level

    def shuffle(self, puz, x1, y1, x2, y2):
        """ Move the blank space in the given direction and if the position value are out
            of limits the return None """
        if x2 >= 0 and x2 < len(self.data) and y2 >= 0 and y2 < len(self.data):
            temp_puz = []
            temp_puz = self.copy(puz)
            temp = temp_puz[x2][y2]
            temp_puz[x2][y2] = 'b'
            temp_puz[x1][y1] = temp
            return temp_puz
        else:
            return None

    def copy(self, root):
        """ Copy function to create a similar matrix of the given node"""
        temp = []
        for i in root:
            t = []
            for j in i:
                t.append(j)
            temp.append(t)
        return temp

class Puzzle:
    def __init__(self,size):
        """ Initialize the puzzle size by the specified size,open and closed lists to empty """
        self.n = size
        self.open = []
        self.closed = []

    def accept(self):
        """ Accepts the puzzle from the user """
        puz = input().split(" ")
        return puz

    def f(self,start,goal, bfs, heu):
        """ Heuristic Function to calculate hueristic value f(x) = h(x) + g(x) """
        if bfs:
            return self.h(start.data, goal, bfs, heu)
        return self.h(start.data, goal,bfs, heu)+start.level

    def h(self, start, goal, bfs, heu):
        """ Calculates the different between the given puzzles """
        temp = 0
        if heu == 1:
            for i in range(len(start[0])):
                for j in range(len(start[0])):
                    if start[i][j] != goal[i][j] and start[i][j] != 'b':
                        temp += 1
            return temp
        if heu == 2:
            for i in range(len(start[0])):
                for j in range(len(start[0])):
                    if start[i][j] == '1':
                        temp += abs(i-0) + abs(j-0)
                    if start[i][j] == '2':
                        temp += abs(i - 0) + abs(j - 1)
                    if start[i][j] == '3':
                        temp += abs(i - 0) + abs(j - 2)
                    if start[i][j] == '4':
                        temp += abs(i - 1) + abs(j - 0)
                    if start[i][j] == '5':
                        temp += abs(i - 1) + abs(j - 1)
                    if start[i][j] == '6':
                        temp += abs(i - 1) + abs(j - 2)
                    if start[i][j] == '7':
                        temp += abs(i - 2) + abs(j - 0)
                    if start[i][j] == '8':
                        temp += abs(i - 2) + abs(j - 1)
            return temp
        if heu == 3:
            for i in range(len(start[0])):
                for j in range(len(start[0])):
                    if start[i][j] == '1':
                        temp += 2*(abs(i-0) + abs(j-0))
                    if start[i][j] == '2':
                        temp += abs(i - 0) + abs(j - 1)
                    if start[i][j] == '3':
                        temp += 2*(abs(i - 0) + abs(j - 2))
                    if start[i][j] == '4':
                        temp += abs(i - 1) + abs(j - 0)
                    if start[i][j] == '5':
                        temp += abs(i - 1) + abs(j - 1)
                    if start[i][j] == '6':
                        temp += abs(i - 1) + abs(j - 2)
                    if start[i][j] == '7':
                        temp += 2*(abs(i - 2) + abs(j - 0))
                    if start[i][j] == '8':
                        temp += abs(i - 2) + abs(j - 1)
            return temp

def transform(goal):
    trans = []
    index = 0
    for i in range(3):
        temp = []
        for j in range(3):
            temp.append(goal[index])
            index += 1
        trans.append(temp)
    return trans

def process(puzzle, algorithm, heu):
        """ Accept Start and Goal Puzzle state"""
        print("Enter the start state matrix \n")
        temp = input()
        startf = []
        for i in temp:
            startf.append(i)

        goalf = ['1', '2', '3', '4', '5', '6', '7', '8', 'b']
        goal = transform(goalf)
        start = transform(startf)

        if algorithm == 1:
            bfs = True
        else:
            bfs = False
        start = Node(start, 0, 0)
        start.fval = puzzle.f(start, goal, bfs, heu)
        """ Put the start node in the open list"""
        openlist = []
        openlist.append(start)
        closed_list = []
        print("\n\n")
        step = 1
        while True:
            cur = openlist[0]
            to_print = []
            for i in cur.data:
                for j in i:
                    to_print.append(j)
            print(to_print, end="->")
            h_score = puzzle.h(cur.data, goal, bfs, heu)
            if h_score == 0:
                print("\n")
                print(step)
                break
            if step > 10000:
                print("Path not found")
                break
            for i in cur.generate_child():
                already = False
                for j in closed_list:
                    if j.data == i.data:
                        already = True
                if not already:
                    i.fval = puzzle.f(i, goal, bfs, heu)
                    openlist.append(i)
            closed_list.append(cur)
            del openlist[0]
            openlist.sort(key=lambda x: x.fval, reverse=False)
            step += 1

print("Which algorithm? 1.Best-First Search 2.A* search")
algorithm = int(input())
print("Which heuristic? (1)h1 (2)h2 (3)h3")
heuristic = int(input())
puz = Puzzle(3)
process(puz, algorithm, heuristic)