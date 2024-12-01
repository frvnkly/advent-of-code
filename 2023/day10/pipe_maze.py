# --- Day 10: Pipe Maze ---

# You use the hang glider to ride the hot air from Desert Island all the way up to the floating metal island. This island is surprisingly cold and there definitely aren't any thermals to glide on, so you leave your hang glider behind.

# You wander around for a while, but you don't find any people or animals. However, you do occasionally find signposts labeled "Hot Springs" pointing in a seemingly consistent direction; maybe you can find someone at the hot springs and ask them where the desert-machine parts are made.

# The landscape here is alien; even the flowers and trees are made of metal. As you stop to admire some metal grass, you notice something metallic scurry away in your peripheral vision and jump into a big pipe! It didn't look like any animal you've ever seen; if you want a better look, you'll need to get ahead of it.

# Scanning the area, you discover that the entire field you're standing on is densely packed with pipes; it was hard to tell at first because they're the same metallic silver color as the "ground". You make a quick sketch of all of the surface pipes you can see (your puzzle input).

# The pipes are arranged in a two-dimensional grid of tiles:

# | is a vertical pipe connecting north and south.
# - is a horizontal pipe connecting east and west.
# L is a 90-degree bend connecting north and east.
# J is a 90-degree bend connecting north and west.
# 7 is a 90-degree bend connecting south and west.
# F is a 90-degree bend connecting south and east.
# . is ground; there is no pipe in this tile.
# S is the starting position of the animal; there is a pipe on this tile, but your sketch doesn't show what shape the pipe has.

# Based on the acoustics of the animal's scurrying, you're confident the pipe that contains the animal is one large, continuous loop.

# For example, here is a square loop of pipe:

# .....
# .F-7.
# .|.|.
# .L-J.
# .....

# If the animal had entered this loop in the northwest corner, the sketch would instead look like this:

# .....
# .S-7.
# .|.|.
# .L-J.
# .....

# In the above diagram, the S tile is still a 90-degree F bend: you can tell because of how the adjacent pipes connect to it.

# Unfortunately, there are also many pipes that aren't connected to the loop! This sketch shows the same loop as above:

# -L|F7
# 7S-7|
# L|7||
# -L-J|
# L|-JF

# In the above diagram, you can still figure out which pipes form the main loop: they're the ones connected to S, pipes those pipes connect to, pipes those pipes connect to, and so on. Every pipe in the main loop connects to its two neighbors (including S, which will have exactly two pipes connecting to it, and which is assumed to connect back to those two pipes).

# Here is a sketch that contains a slightly more complex main loop:

# ..F7.
# .FJ|.
# SJ.L7
# |F--J
# LJ...

# Here's the same example sketch with the extra, non-main-loop pipe tiles also shown:

# 7-F7-
# .FJ|7
# SJLL7
# |F--J
# LJ.LJ

# If you want to get out ahead of the animal, you should find the tile in the loop that is farthest from the starting position. Because the animal is in the pipe, it doesn't make sense to measure this by direct distance. Instead, you need to find the tile that would take the longest number of steps along the loop to reach from the starting point - regardless of which way around the loop the animal went.

# In the first example with the square loop:

# .....
# .S-7.
# .|.|.
# .L-J.
# .....

# You can count the distance each tile in the loop is from the starting point like this:

# .....
# .012.
# .1.3.
# .234.
# .....

# In this example, the farthest point from the start is 4 steps away.

# Here's the more complex loop again:

# ..F7.
# .FJ|.
# SJ.L7
# |F--J
# LJ...

# Here are the distances for each tile on that loop:

# ..45.
# .236.
# 01.78
# 14567
# 23...

# Find the single giant loop starting at S. How many steps along the loop does it take to get from the starting position to the point farthest from the starting position?


import sys

sys.path.append(".")
from util import get_input

def get_start(maze):
    for i in range(len(maze)):
        for j in range(len(maze[i])):
            if maze[i][j] == "S":
                return i, j
            
def get_starting_pipe(maze, i, j):
    directions = [0, 0, 0, 0]
    
    if 0 <= i - 1 and maze[i-1][j] in ["|", "7", "F"]:
        directions[0] = 1
    if j + 1 < len(maze[i]) and maze[i][j+1] in ["-", "J", "7"]:
        directions[1] = 1
    if i + 1 < len(maze) and maze[i+1][j] in ["|", "L", "J"]:
        directions[2] = 1
    if 0 <= j - 1 and maze[i][j-1] in ["-", "L", "F"]:
        directions[3] = 1

    if directions[0]:
        if directions[1]: return "L"
        if directions[2]: return "|"
        if directions[3]: return "J"
    if directions[1]:
        if directions[2]: return "F"
        if directions[3]: return "-"
    if directions[2]:
        if directions[3]: return "7"
            
def format_maze(maze):
    formatted = list(map(list, maze))

    start = get_start(maze)
    formatted[start[0]][start[1]] = get_starting_pipe(maze, start[0], start[1])

    for i in range(len(formatted)):
        for j in range(len(formatted[i])):
            if formatted[i][j] == "|":
                formatted[i][j] = (0, 2)
            elif formatted[i][j] == "-":
                formatted[i][j] = (1, 3)
            elif formatted[i][j] == "L":
                formatted[i][j] = (0, 1)
            elif formatted[i][j] == "J":
                formatted[i][j] = (0, 3)
            elif formatted[i][j] == "7":
                formatted[i][j] = (2, 3)
            elif formatted[i][j] == "F":
                formatted[i][j] = (1, 2)
            else: formatted[i][j] = None

    return formatted
            
def get_maze():
    maze = get_input("2023/day10/input.txt")    
    return format_maze(maze), get_start(maze)

def get_loop_length(maze, start):
    steps = 0
    start_x, start_y = start
    starting_direction = maze[start[0]][start[1]][0]
    current = (start_x, start_y, starting_direction)
    while True:
        x, y, d = current

        for direction in maze[x][y]:
            if direction != d:
                next_direction = direction
                break
        
        if next_direction == 0:
            current = (x - 1, y, 2)
        elif next_direction == 1:
            current = (x, y + 1, 3)
        elif next_direction == 2:
            current = (x + 1, y, 0)
        elif next_direction == 3:
            current = (x, y - 1, 1)

        steps += 1

        if current[0] == start_x and current[1] == start_y:
            break

    return steps

def simplify_maze(maze, start):
    maze_copy = [[None] * len(maze[0]) for _ in range(len(maze))]
    start_x, start_y = start
    starting_direction = maze[start[0]][start[1]][0]
    current = (start_x, start_y, starting_direction)
    while True:
        x, y, d = current

        maze_copy[x][y] = maze[x][y]

        for direction in maze[x][y]:
            if direction != d:
                next_direction = direction
                break
        
        if next_direction == 0:
            current = (x - 1, y, 2)
        elif next_direction == 1:
            current = (x, y + 1, 3)
        elif next_direction == 2:
            current = (x + 1, y, 0)
        elif next_direction == 3:
            current = (x, y - 1, 1)        

        if current[0] == start_x and current[1] == start_y:
            break

    return maze_copy

def count_enclosed_tiles(maze):
    enclosed_tiles = 0
    for i in range(len(maze)):
        is_enclosed = False
        for j in range(len(maze[i])):
            if maze[i][j]:
                if 0 in maze[i][j] or 2 in maze[i][j]:
                    is_enclosed = not is_enclosed
            else:
                if is_enclosed:
                    print(i, j)
                    enclosed_tiles += 1
    
    return enclosed_tiles

def part1(maze, start):
    loop_length = get_loop_length(maze, start)
    return int(loop_length / 2)

def part2(maze, start):
    simplified_maze = simplify_maze(maze, start)
    return count_enclosed_tiles(simplified_maze)

if __name__ == "__main__":
    maze, start = get_maze()

    print(f"part 1: {part1(maze, start)}")
    print(f"part 2: {part2(maze, start)}")
