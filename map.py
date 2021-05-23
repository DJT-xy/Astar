import pygame
import sys
from Astar import Node, Map, Astar

pygame.init()
pygame.font.init()
font = pygame.font.Font("DejaVuSans-Bold.ttf", 58)
sys.setrecursionlimit(5000)
size = width, height = 2400, 1462 # 1862
screen = pygame.display.set_mode(size)

def write(t, p):
    text = font.render(t, True, pygame.Color(0, 0, 0))
    screen.blit(text, p)

def draw(start, goal, heuristic):
    maze = pygame.image.load('map.png')
    mazerect = maze.get_rect()

    w, h = 51.7, 41.7
    a = Astar(start, goal, heuristic)
    a.solve()
    path = a.path
    search = a.iter
    i = 0
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        screen.fill(pygame.Color(255, 255, 255))
        screen.blit(maze, mazerect)
        pygame.draw.rect(screen, (50, 50, 200), pygame.Rect((start.x - 1) * w, (35 - start.y) * h, w, h))
        pygame.draw.rect(screen, (255, 0, 0), pygame.Rect((goal.x - 1) * w, (35 - goal.y) * h, w, h))
        write("Simple A*", (1950, 100))
        write("Start: {0}, {1}".format(a.start.x, a.start.y), (1900, 600))
        write("Goal : {0}, {1}".format(a.goal.x, a.goal.y), (1900, 700))
        write("Iter  : {}".format(i), (1900, 800))
        write("Heuristic:", (1950, 300))
        if a.h == 'M':
            write("Manhattan", (1950, 400))
        elif a.h == 'E':
            write("Euclidean", (1950, 400))
        else:
            write(" 0 (LCFS)", (1950, 400))
        last = None
        current = None
        if i < len(search):
            for node in search[i]:
                last = current
                current = node
                if last != None:
                    pygame.draw.line(screen, (255, 0, 0), ((last.x - 1) * w + w/2, ((35 - last.y) * h) + h/2), ((current.x - 1) * w + w/2, ((35 - current.y) * h) + h/2), width=4)
            write("Cost : {}".format(a.cost(search[i])), (1900, 900))
            write("Value: {}".format(a.value(search[i])), (1900, 1000))
            i += 1
        else:
            for node in search[-1]:
                last = current
                current = node
                if last != None:
                    pygame.draw.line(screen, (255, 0, 0), ((last.x - 1) * w + w/2, ((35 - last.y) * h) + h/2), ((current.x - 1) * w + w/2, ((35 - current.y) * h) + h/2), width=10)
            write("Cost : {}".format(a.cost(search[-1])), (1900, 900))
            write("Value: {}".format(a.value(search[-1])), (1900, 1000))
            write("Goal Reached!", (1900, 1200))
        pygame.display.update()
        pygame.time.delay(20)
  
    pygame.quit()
