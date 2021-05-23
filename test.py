from map import draw
from Astar import Node

if __name__ == '__main__':
    start=Node(12, 1)
    goal=Node(24, 10)
    draw(start, goal, heuristic='M')
