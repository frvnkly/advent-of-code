# --- Day 14: Parabolic Reflector Dish ---

# You reach the place where all of the mirrors were pointing: a massive parabolic reflector dish attached to the side of another large mountain.

# The dish is made up of many small mirrors, but while the mirrors themselves are roughly in the shape of a parabolic reflector dish, each individual mirror seems to be pointing in slightly the wrong direction. If the dish is meant to focus light, all it's doing right now is sending it in a vague direction.

# This system must be what provides the energy for the lava! If you focus the reflector dish, maybe you can go where it's pointing and use the light to fix the lava production.

# Upon closer inspection, the individual mirrors each appear to be connected via an elaborate system of ropes and pulleys to a large metal platform below the dish. The platform is covered in large rocks of various shapes. Depending on their position, the weight of the rocks deforms the platform, and the shape of the platform controls which ropes move and ultimately the focus of the dish.

# In short: if you move the rocks, you can focus the dish. The platform even has a control panel on the side that lets you tilt it in one of four directions! The rounded rocks (O) will roll when the platform is tilted, while the cube-shaped rocks (#) will stay in place. You note the positions of all of the empty spaces (.) and rocks (your puzzle input). For example:

# O....#....
# O.OO#....#
# .....##...
# OO.#O....O
# .O.....O#.
# O.#..O.#.#
# ..O..#O..O
# .......O..
# #....###..
# #OO..#....

# Start by tilting the lever so all of the rocks will slide north as far as they will go:

# OOOO.#.O..
# OO..#....#
# OO..O##..O
# O..#.OO...
# ........#.
# ..#....#.#
# ..O..#.O.O
# ..O.......
# #....###..
# #....#....

# You notice that the support beams along the north side of the platform are damaged; to ensure the platform doesn't collapse, you should calculate the total load on the north support beams.

# The amount of load caused by a single rounded rock (O) is equal to the number of rows from the rock to the south edge of the platform, including the row the rock is on. (Cube-shaped rocks (#) don't contribute to load.) So, the amount of load caused by each rock in each row is as follows:

# OOOO.#.O.. 10
# OO..#....#  9
# OO..O##..O  8
# O..#.OO...  7
# ........#.  6
# ..#....#.#  5
# ..O..#.O.O  4
# ..O.......  3
# #....###..  2
# #....#....  1

# The total load is the sum of the load caused by all of the rounded rocks. In this example, the total load is 136.

# Tilt the platform so that the rounded rocks all roll north. Afterward, what is the total load on the north support beams?

# --- Part Two ---

# The parabolic reflector dish deforms, but not in a way that focuses the beam. To do that, you'll need to move the rocks to the edges of the platform. Fortunately, a button on the side of the control panel labeled "spin cycle" attempts to do just that!

# Each cycle tilts the platform four times so that the rounded rocks roll north, then west, then south, then east. After each tilt, the rounded rocks roll as far as they can before the platform tilts in the next direction. After one cycle, the platform will have finished rolling the rounded rocks in those four directions in that order.

# Here's what happens in the example above after each of the first few cycles:

# After 1 cycle:
# .....#....
# ....#...O#
# ...OO##...
# .OO#......
# .....OOO#.
# .O#...O#.#
# ....O#....
# ......OOOO
# #...O###..
# #..OO#....

# After 2 cycles:
# .....#....
# ....#...O#
# .....##...
# ..O#......
# .....OOO#.
# .O#...O#.#
# ....O#...O
# .......OOO
# #..OO###..
# #.OOO#...O

# After 3 cycles:
# .....#....
# ....#...O#
# .....##...
# ..O#......
# .....OOO#.
# .O#...O#.#
# ....O#...O
# .......OOO
# #...O###.O
# #.OOO#...O

# This process should work if you leave it running long enough, but you're still worried about the north support beams. To make sure they'll survive for a while, you need to calculate the total load on the north support beams after 1000000000 cycles.

# In the above example, after 1000000000 cycles, the total load on the north support beams is 64.

# Run the spin cycle for 1000000000 cycles. Afterward, what is the total load on the north support beams?


import sys

sys.path.append(".")
from util import get_input

def get_platform():
    return list(map(list, get_input("2023/day14/input.txt")))

def tilt_platform(platform, direction):
    tilted_platform = [
        ["."] * len(platform[0]) for _ in range(len(platform))
    ]

    if direction == 0:
        for j in range(len(platform[0])):
            pos = 0
            for i in range(len(platform)):
                if platform[i][j] == "O":
                    tilted_platform[pos][j] = "O"
                    pos += 1
                
                if platform[i][j] == "#":
                    tilted_platform[i][j] = "#"
                    pos = i + 1

    if direction == 1:
        for i in range(len(platform)):
            pos = len(platform[i]) - 1
            for j in range(len(platform[i]) - 1, -1, -1):
                if platform[i][j] == "O":
                    tilted_platform[i][pos] = "O"
                    pos -= 1

                if platform[i][j] == "#":
                    tilted_platform[i][j] = "#"
                    pos = j - 1

    if direction == 2:
        for j in range(len(platform[0])):
            pos = len(platform) - 1
            for i in range(len(platform) - 1, -1, -1):
                if platform[i][j] == "O":
                    tilted_platform[pos][j] = "O"
                    pos -= 1
                
                if platform[i][j] == "#":
                    tilted_platform[i][j] = "#"
                    pos = i - 1

    if direction == 3:
        for i in range(len(platform)):
            pos = 0
            for j in range(len(platform[i])):
                if platform[i][j] == "O":
                    tilted_platform[i][pos] = "O"
                    pos += 1

                if platform[i][j] == "#":
                    tilted_platform[i][j] = "#"
                    pos = j + 1

    return tilted_platform

def get_total_load(platform):
    total_load = 0
    for i in range(len(platform)):
        for j in range(len(platform[i])):
            if platform[i][j] == "O":
                total_load += len(platform) - i

    return total_load

def cycle_platform(platform):
    tilted_north = tilt_platform(platform, 0)
    tilted_west = tilt_platform(tilted_north, 3)
    tilted_south = tilt_platform(tilted_west, 2)
    tilted_east = tilt_platform(tilted_south, 1)

    return tilted_east

def find_load_cycle(history):
    for i in range(len(history) - 2, -1, -1):
        is_repeat = True
        for x in range(len(history) - i + 1):
            if history[i-x] != history[-1-x]:
                is_repeat = False
                break

        if is_repeat:
            return history[i:len(history) - 1]

def part1(platform):
    tilted_platform = tilt_platform(platform, 0)
    return get_total_load(tilted_platform)

def part2(platform):
    cycled_platform = platform
    history = []
    for _ in range(1000):
        cycled_platform = cycle_platform(cycled_platform)
        cycle_load = get_total_load(cycled_platform)

        history.append(cycle_load)

    load_cycle = find_load_cycle(history)
    return load_cycle[(1000000000 - 1000) % len(load_cycle)]

if __name__ == "__main__":
    platform = get_platform()

    print(f"part 1: {part1(platform)}")
    print(f"part 2: {part2(platform)}")
