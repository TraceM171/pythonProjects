import math
import random
import sys
import pygame
import tkinter as tk
from tkinter import messagebox

width = 500
rows = 20
rowW = width // rows
tick = 3

class Cube():
    def __init__(self, pos, color=(0,255,0)):
        self.pos = pos
        self.color = color

    def move(self, mdir):
        if not self.canMove(mdir): return False
        self.pos = self.getNewPos(mdir)
        return True

    def canMove(self, mdir):
        x, y = self.getNewPos(mdir)
        return x >= 0 and x < rows and y >= 0 and y < rows

    def getNewPos(self, mdir):
        x, y = self.pos
        if mdir == 1:
            y -= 1
        elif mdir == 2:
            x += 1
        elif mdir == 3:
            y += 1
        elif mdir == 4:
            x -= 1
        return x, y

    def draw(self, surface, beforePos=None, eyes=False):
        x, y = self.pos
        ox, oy = rowToX(x), rowToX(y)
        w, h = rowW - 1, rowW - 1
        if beforePos:
            bx, by = beforePos
            if bx < x:
                ox -= 1
                w += 1
            if bx > x:
                w += 1
            if by < y:
                oy -= 1
                h += 1
            if by > y:
                h += 1
        pygame.draw.rect(surface, self.color, pygame.Rect((ox, oy), (w, h)))
        if eyes:
            radius = rowW // 8
            c1 = rowW // 4
            cc1 = rowToX(x) + c1, rowToX(y) + c1
            c2 = rowW // 4 * 3
            cc2 = rowToX(x) + c2, rowToX(y) + c1
            pygame.draw.circle(surface, (0, 0, 0), cc1, radius)
            pygame.draw.circle(surface, (0, 0, 0), cc2, radius)

class Snake():
    body = []
    turns = {}
    pendingCube = False
    def __init__(self, color, pos):
        self.color = color
        self.head = Cube(pos)
        self.body.append(self.head)
        self.mdir = 1

    def move(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                k = event.key
                if k == pygame.K_UP:
                    self.mdir = 1
                elif k == pygame.K_RIGHT:
                    self.mdir = 2
                elif k == pygame.K_DOWN:
                    self.mdir = 3
                elif k == pygame.K_LEFT:
                    self.mdir = 4

        self.turns[self.head.pos] = self.mdir
       
        for c in self.body:
            oldPos = c.pos
            if c == self.head:
                if not c.move(self.turns[c.pos]) or c.pos in self.turns:
                    sys.exit()
            else:
                c.move(self.turns[c.pos])
            if c == self.body[-1]:
                if self.pendingCube:
                    self.body.append(Cube(oldPos))
                    self.pendingCube = False
                    break
                else:
                    self.turns.pop(oldPos)
        
    def reset(self, pos):
        pass

    def addCube(self):
        self.pendingCube = True

    def draw(self, surface):
        for c, cPrev in zip(self.body, self.body[1:]):
            c.draw(surface, beforePos=cPrev.pos, eyes=c==self.head)
        if len(self.body) > 1:
            self.body[-1].draw(surface)
        else:
            self.head.draw(surface, eyes=True)

    def isInSnake(self, pos):
        return pos == self.head.pos or pos in self.turns

def rowToX(row):
    return row * rowW + 1

def drawGrid(surface):
    w = width
    x = 0
    y = 0

    for l in range(rows):
        x += rowW
        y += rowW
        pygame.draw.line(surface, (25, 25, 25), (x, 0), (x, w))
        pygame.draw.line(surface, (25, 25, 25), (0, y), (w, y))

    pygame.draw.line(surface, (255, 255, 255), (0, 0), (w, 0))
    pygame.draw.line(surface, (255, 255, 255), (w, 0), (w, w))
    pygame.draw.line(surface, (255, 255, 255), (w, w), (0, w))
    pygame.draw.line(surface, (255, 255, 255), (0, w), (0, 0))

def redrawWindow(surface, snake, snack):
    surface.fill((0, 0, 0))
    drawGrid(surface)
    snack.draw(surface)
    snake.draw(surface)
    pygame.display.update()

def randomSnack(surface, snake):
    x, y = randomRow(), randomRow()
    while snake.isInSnake((x, y)): x, y = randomRow(), randomRow()
    pos = x, y
    return Cube(pos, (255, 0, 0))

def randomRow():
    return random.randint(0, rows-1)

def message_box(subject, content):
    pass

def main():
    win = pygame.display.set_mode((width + 1, width + 1))
    snake = Snake((255, 0, 0), (rows // 2, rows // 2))
    snack = randomSnack(win, snake)
    clock = pygame.time.Clock()

    randomSnack(win, snake)

    flag = True
    while flag:
        redrawWindow(win, snake, snack)
        clock.tick(tick)
        snake.move()
        if snake.isInSnake(snack.pos):
            snake.addCube()
            snack = randomSnack(win, snake)

if __name__ == "__main__":
    main()
