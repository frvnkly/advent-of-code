# --- Day 18: Lavaduct Lagoon ---

# Thanks to your efforts, the machine parts factory is one of the first factories up and running since the lavafall came back. However, to catch up with the large backlog of parts requests, the factory will also need a large supply of lava for a while; the Elves have already started creating a large lagoon nearby for this purpose.

# However, they aren't sure the lagoon will be big enough; they've asked you to take a look at the dig plan (your puzzle input). For example:

# R 6 (#70c710)
# D 5 (#0dc571)
# L 2 (#5713f0)
# D 2 (#d2c081)
# R 2 (#59c680)
# D 2 (#411b91)
# L 5 (#8ceee2)
# U 2 (#caa173)
# L 1 (#1b58a2)
# U 2 (#caa171)
# R 2 (#7807d2)
# U 3 (#a77fa3)
# L 2 (#015232)
# U 2 (#7a21e3)

# The digger starts in a 1 meter cube hole in the ground. They then dig the specified number of meters up (U), down (D), left (L), or right (R), clearing full 1 meter cubes as they go. The directions are given as seen from above, so if "up" were north, then "right" would be east, and so on. Each trench is also listed with the color that the edge of the trench should be painted as an RGB hexadecimal color code.

# When viewed from above, the above example dig plan would result in the following loop of trench (#) having been dug out from otherwise ground-level terrain (.):

# #######
# #.....#
# ###...#
# ..#...#
# ..#...#
# ###.###
# #...#..
# ##..###
# .#....#
# .######

# At this point, the trench could contain 38 cubic meters of lava. However, this is just the edge of the lagoon; the next step is to dig out the interior so that it is one meter deep as well:

# #######
# #######
# #######
# ..#####
# ..#####
# #######
# #####..
# #######
# .######
# .######

# Now, the lagoon can contain a much more respectable 62 cubic meters of lava. While the interior is dug out, the edges are also painted according to the color codes in the dig plan.

# The Elves are concerned the lagoon won't be large enough; if they follow their dig plan, how many cubic meters of lava could it hold?


import sys

sys.path.append(".")
from util import get_input

def get_dig_plan():
    dig_plan = []
    for line in get_input("2023/day18/input.txt"):
        direction, meters, color = line.split()
        dig_plan.append([direction, int(meters), color[1:-1]])

    return dig_plan

def dig_outline(dig_plan):
    coords = [(0, 0)]
    for direction, meters, _ in dig_plan:
        if direction == "U":
            coords.append((coords[-1][0] - meters, coords[-1][1]))
        elif direction == "D":
            coords.append((coords[-1][0] + meters, coords[-1][1]))
        elif direction == "L":
            coords.append((coords[-1][0], coords[-1][1] - meters))
        elif direction == "R":
            coords.append((coords[-1][0], coords[-1][1] + meters))

    min_row = 0
    max_row = 0
    min_col = 0
    max_col = 0
    for coord in coords:
        min_row = min(min_row, coord[0])
        max_row = max(max_row, coord[0])
        min_col = min(min_col, coord[1])
        max_col = max(max_col, coord[1])

    num_rows = max_row - min_row + 1
    num_cols = max_col - min_col + 1

    adjusted_coords = list(map(
        lambda x: (x[0] - min_row, x[1] - min_col),
        coords
    ))

    lagoon = [["."] * num_cols for _ in range(num_rows)]

    cursor = adjusted_coords[0]
    lagoon[cursor[0]][cursor[1]] = "#"
    for i in range(1, len(adjusted_coords)):
        row, col = adjusted_coords[i]

        if row < cursor[0]:
            for r in range(row, cursor[0]):
                lagoon[r][cursor[1]] = "#"
        elif row > cursor[0]:
            for r in range(cursor[0] + 1, row + 1):
                lagoon[r][cursor[1]] = "#"
        elif col < cursor[1]:
            for c in range(col, cursor[1]):
                lagoon[cursor[0]][c] = "#"
        elif col > cursor[1]:
            for c in range(cursor[1] + 1, col + 1):
                lagoon[cursor[0]][c] = "#"

        cursor = (row, col)

    return lagoon

def dig_interior(lagoon):
    for col in range(len(lagoon[0])):
        if lagoon[0][col] == "#":
            start = (1, col + 1)
            break

    stack = [start]
    while stack:
        row, col = stack.pop()

        if lagoon[row][col] == "#": continue

        lagoon[row][col] = "#"

        for d in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            r = row + d[0]
            c = col + d[1]

            if 0 <= r < len(lagoon) and 0 <= c < len(lagoon[r]):
                stack.append((r, c))

def part1(dig_plan):
    lagoon = dig_outline(dig_plan)
    dig_interior(lagoon)

    volume = 0
    for row in lagoon:
        volume += len(list(filter(lambda x: x == "#", row)))

    return volume

if __name__ == "__main__":
    dig_plan = get_dig_plan()

    print(f"part 1: {part1(dig_plan)}")
