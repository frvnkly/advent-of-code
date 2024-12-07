# --- Day 6: Guard Gallivant ---

# The Historians use their fancy device again, this time to whisk you all away to the North Pole prototype suit manufacturing lab... in the year 1518! It turns out that having direct access to history is very convenient for a group of historians.

# You still have to be careful of time paradoxes, and so it will be important to avoid anyone from 1518 while The Historians search for the Chief. Unfortunately, a single guard is patrolling this part of the lab.

# Maybe you can work out where the guard will go ahead of time so that The Historians can search safely?

# You start by making a map (your puzzle input) of the situation. For example:

# ....#.....
# .........#
# ..........
# ..#.......
# .......#..
# ..........
# .#..^.....
# ........#.
# #.........
# ......#...

# The map shows the current position of the guard with ^ (to indicate the guard is currently facing up from the perspective of the map). Any obstructions - crates, desks, alchemical reactors, etc. - are shown as #.

# Lab guards in 1518 follow a very strict patrol protocol which involves repeatedly following these steps:

# If there is something directly in front of you, turn right 90 degrees.
# Otherwise, take a step forward.
# Following the above protocol, the guard moves up several times until she reaches an obstacle (in this case, a pile of failed suit prototypes):

# ....#.....
# ....^....#
# ..........
# ..#.......
# .......#..
# ..........
# .#........
# ........#.
# #.........
# ......#...

# Because there is now an obstacle in front of the guard, she turns right before continuing straight in her new facing direction:

# ....#.....
# ........>#
# ..........
# ..#.......
# .......#..
# ..........
# .#........
# ........#.
# #.........
# ......#...

# Reaching another obstacle (a spool of several very long polymers), she turns right again and continues downward:

# ....#.....
# .........#
# ..........
# ..#.......
# .......#..
# ..........
# .#......v.
# ........#.
# #.........
# ......#...

# This process continues for a while, but the guard eventually leaves the mapped area (after walking past a tank of universal solvent):

# ....#.....
# .........#
# ..........
# ..#.......
# .......#..
# ..........
# .#........
# ........#.
# #.........
# ......#v..

# By predicting the guard's route, you can determine which specific positions in the lab will be in the patrol path. Including the guard's starting position, the positions visited by the guard before leaving the area are marked with an X:

# ....#.....
# ....XXXXX#
# ....X...X.
# ..#.X...X.
# ..XXXXX#X.
# ..X.X.X.X.
# .#XXXXXXX.
# .XXXXXXX#.
# #XXXXXXX..
# ......#X..

# In this example, the guard will visit 41 distinct positions on your map.

# Predict the path of the guard. How many distinct positions will the guard visit before leaving the mapped area?


import sys

sys.path.append('.')
from util import get_input

def get_guard_position_and_direction(lab_map):
    for x in range(len(lab_map)):
        for y in range(len(lab_map[x])):
            if lab_map[x][y] in ['.', '#']:
                continue

            if lab_map[x][y] == '^':
                dx, dy = -1, 0
            elif lab_map[x][y] == '>':
                dx, dy = 0, 1
            elif lab_map[x][y] == 'v':
                dx, dy = 1, 0
            else:
                dx, dy = 0, -1

            return x, y, dx, dy
        
def move_guard(lab_map, x, y, dx, dy):
    while True:
        x2 = x + dx
        y2 = y + dy

        if not 0 <= x2 < len(lab_map) or not 0 <= y2 < len(lab_map[x2]):
            return x, y, dx, dy
        
        if lab_map[x2][y2] == '#':
            dx, dy = dy, dx * -1
            continue

        return x2, y2, dx, dy
        
def part1(lab_map):
    x, y, dx, dy = get_guard_position_and_direction(lab_map)
    visited = set([(x, y)])
    while True:
        x2, y2, dx2, dy2 = move_guard(lab_map, x, y, dx, dy)

        if x2 == x and y2 == y:
            break
                    
        x = x2
        y = y2
        dx = dx2
        dy = dy2
        visited.add((x, y))

    print(f'part 1: {len(visited)}')

if __name__ == '__main__':
    lab_map = get_input('2024/day6/input.txt')
    part1(lab_map)
