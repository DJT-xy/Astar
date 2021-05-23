from collections import namedtuple

Node = namedtuple('Node', 'x y')

class Map:
    def __init__(self):
        self.nodes = [Node(i, j) for i in range(1, 37) for j in range(1, 36)]
        self.constrains = [(Node(i, j), Node(i, j+1)) for i in range(1, 37) for j in range(1, 35)]
        for i in [7, 18, 29]:
            for j in range(1, 35):
                self.constrains.remove((Node(i, j), Node(i, j+1)))
        self.constrains += [(Node(i, j), Node(i+1, j)) for i in [12, 23] for j in range(1, 36)]
        for i in [12, 23]:
            for j in [1, 3, 19, 34]:
                self.constrains.remove((Node(i, j), Node(i+1, j)))
        self.constrains += [(Node(13, 1), Node(14, 1)), (Node(24, 1), Node(25, 1))]

class Astar:
    def __init__(self, start, goal, heuristic=None):
        self.start = start
        self.goal = goal
        self.h = heuristic
        self.map = Map()
        self.frontier = []
        self.iter = []
    
    def heuristic(self, path):
        if(self.h == 'M'):
            value = abs(path[-1].x - self.goal.x) + abs(path[-1].y - self.goal.y)
        elif(self.h == 'E'):
            value = ((path[-1].x - self.goal.x)**2 + (path[-1].y - self.goal.y)**2)**0.5
        else:
            value = 0
        return value
    
    def cost(self, path):
        current = None
        last = None
        lastlast = None
        value = 0
        for n in path:
            lastlast = last
            last = current
            current = n
            if lastlast and (lastlast.x - n.x)*(lastlast.y - n.y) != 0:
                value += 6 + 1
            elif last:
                value += 1
        return value
    
    def value(self, path):
        return self.cost(path) + self.heuristic(path)
    
    def backtrack(self, path):
        last = None
        current = None
        for n in path[::-1]:
            last = current
            current = n
            if (last, current) in self.map.constrains or (current, last) in self.map.constrains:
                return False
        return True

    def solve(self, path=None):
        if path == None:
            path = [self.start,]
        if path[-1] == self.goal:
            self.path = path
            return True
        nodes = [Node(path[-1].x + 1, path[-1].y),
                 Node(path[-1].x, path[-1].y + 1),
                 Node(path[-1].x - 1, path[-1].y),
                 Node(path[-1].x, path[-1].y - 1)]
        for n in nodes:
            if self.backtrack(path + [n]) and len(set(path + [n])) == len((path + [n])) and n in self.map.nodes:
                self.frontier.append(path + [n])
        self.frontier.sort(key=self.value)
        path = self.frontier[0]
        self.iter.append(path)
        del self.frontier[0]
        self.solve(path)
