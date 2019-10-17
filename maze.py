# -*- coding: utf-8 -*-

import numpy as np
import random
from os import system
import sys

# function to print the maze
def printMaze(maze):
  system('clear')
  for i in range(len(maze)):
    for j in range(len(maze[i])):
      if maze[i][j] == 0:
        print('██', end="")
      elif maze[i][j] == 1:
        print('  ', end="")
    print('')

# function to generate the maze
def generate_maze(n, m):
  def find(p, q):
    if p != cells[p] or q != cells[q]:
      cells[p], cells[q] = find(cells[p], cells[q])
    return cells[p], cells[q]    # find spanning tree

  # make even size to avoid issues in the future
  if n % 2 == 1:
    n = n + 1
  if m % 2 == 1:
    m = m + 1

  # maze checkerboard of wall squares and squares that can be either walls or pathways
  maze = np.tile([[1, 2], [2, 0]], (n // 2 + 1, m // 2 + 1))
  maze = maze[:-1, :-1]
  cells = {(i, j): (i, j) for i, j in np.argwhere(maze == 1)}
  walls = np.argwhere(maze == 2)    # union-find
  np.random.shuffle(walls)

  # kruskal's maze algorithm
  for wi, wj in walls:
    if wi % 2:
      p, q = find((wi - 1, wj), (wi + 1, wj))
    else:
      p, q = find((wi, wj - 1), (wi, wj + 1))
    maze[wi, wj] = p != q
    if p != q:
      cells[p] = q

  # initialise the two types of border
  vertBorders = np.zeros((n + 3,), dtype=int)
  horiBorders = np.zeros((m + 1,), dtype=int)

  # pad maze with walls
  maze = np.concatenate(([horiBorders], maze), axis=0)
  maze = np.concatenate((maze, [horiBorders]), axis=0)
  maze = np.insert(maze, 0, vertBorders, axis=1)
  maze = np.insert(maze, len(maze[0]), vertBorders, axis=1)

  return maze

# get command line arguments and generate the maze
width = int(sys.argv[2])
height = int(sys.argv[1])
maze = generate_maze(width, height)

printMaze(maze)
