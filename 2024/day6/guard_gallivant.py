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

# --- Part Two ---

# While The Historians begin working around the guard's patrol route, you borrow their fancy device and step outside the lab. From the safety of a supply closet, you time travel through the last few months and record the nightly status of the lab's guard post on the walls of the closet.

# Returning after what seems like only a few seconds to The Historians, they explain that the guard's patrol area is simply too large for them to safely search the lab without getting caught.

# Fortunately, they are pretty sure that adding a single new obstruction won't cause a time paradox. They'd like to place the new obstruction in such a way that the guard will get stuck in a loop, making the rest of the lab safe to search.

# To have the lowest chance of creating a time paradox, The Historians would like to know all of the possible positions for such an obstruction. The new obstruction can't be placed at the guard's starting position - the guard is there right now and would notice.

# In the above example, there are only 6 different positions where a new obstruction would cause the guard to get stuck in a loop. The diagrams of these six situations use O to mark the new obstruction, | to show a position where the guard moves up/down, - to show a position where the guard moves left/right, and + to show a position where the guard moves both up/down and left/right.

# Option one, put a printing press next to the guard's starting position:

# ....#.....
# ....+---+#
# ....|...|.
# ..#.|...|.
# ....|..#|.
# ....|...|.
# .#.O^---+.
# ........#.
# #.........
# ......#...

# Option two, put a stack of failed suit prototypes in the bottom right quadrant of the mapped area:


# ....#.....
# ....+---+#
# ....|...|.
# ..#.|...|.
# ..+-+-+#|.
# ..|.|.|.|.
# .#+-^-+-+.
# ......O.#.
# #.........
# ......#...

# Option three, put a crate of chimney-squeeze prototype fabric next to the standing desk in the bottom right quadrant:

# ....#.....
# ....+---+#
# ....|...|.
# ..#.|...|.
# ..+-+-+#|.
# ..|.|.|.|.
# .#+-^-+-+.
# .+----+O#.
# #+----+...
# ......#...

# Option four, put an alchemical retroencabulator near the bottom left corner:

# ....#.....
# ....+---+#
# ....|...|.
# ..#.|...|.
# ..+-+-+#|.
# ..|.|.|.|.
# .#+-^-+-+.
# ..|...|.#.
# #O+---+...
# ......#...

# Option five, put the alchemical retroencabulator a bit to the right instead:

# ....#.....
# ....+---+#
# ....|...|.
# ..#.|...|.
# ..+-+-+#|.
# ..|.|.|.|.
# .#+-^-+-+.
# ....|.|.#.
# #..O+-+...
# ......#...

# Option six, put a tank of sovereign glue right next to the tank of universal solvent:

# ....#.....
# ....+---+#
# ....|...|.
# ..#.|...|.
# ..+-+-+#|.
# ..|.|.|.|.
# .#+-^-+-+.
# .+----++#.
# #+----++..
# ......#O..

# It doesn't really matter what you choose to use as an obstacle so long as you and The Historians can put it into position without the guard noticing. The important thing is having enough options that you can find one that minimizes time paradoxes, and in this example, there are 6 different positions you could choose.

# You need to get the guard stuck in a loop by adding a single new obstruction. How many different positions could you choose for this obstruction?


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

def part2(lab_map):
    (start_x, start_y,
     start_dx, start_dy) = get_guard_position_and_direction(lab_map)

    num_possible_obstacles = 0
    for obstacle_x in range(len(lab_map)):
        for obstacle_y in range(len(lab_map[obstacle_x])):
            if lab_map[obstacle_x][obstacle_y] != '.':
                continue

            lab_map[obstacle_x][obstacle_y] = '#'

            x, y, dx, dy = start_x, start_y, start_dx, start_dy
            visited = set([(x, y, dx, dy)])
            while True:
                x2, y2, dx2, dy2 = move_guard(lab_map, x, y, dx, dy)

                if x2 == x and y2 == y:
                    break

                if (x2, y2, dx2, dy2) in visited:
                    num_possible_obstacles += 1
                    break

                x = x2
                y = y2
                dx = dx2
                dy = dy2
                visited.add((x, y, dx, dy))

            lab_map[obstacle_x][obstacle_y] = '.'

    print(f'part 2: {num_possible_obstacles}')

if __name__ == '__main__':
    lab_map = list(map(list, get_input('2024/day6/input.txt')))
    part1(lab_map)
    part2(lab_map)
