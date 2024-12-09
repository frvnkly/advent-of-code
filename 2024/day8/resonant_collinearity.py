# --- Day 8: Resonant Collinearity ---

# You find yourselves on the roof of a top-secret Easter Bunny installation.

# While The Historians do their thing, you take a look at the familiar huge antenna. Much to your surprise, it seems to have been reconfigured to emit a signal that makes people 0.1% more likely to buy Easter Bunny brand Imitation Mediocre Chocolate as a Christmas gift! Unthinkable!

# Scanning across the city, you find that there are actually many such antennas. Each antenna is tuned to a specific frequency indicated by a single lowercase letter, uppercase letter, or digit. You create a map (your puzzle input) of these antennas. For example:

# ............
# ........0...
# .....0......
# .......0....
# ....0.......
# ......A.....
# ............
# ............
# ........A...
# .........A..
# ............
# ............

# The signal only applies its nefarious effect at specific antinodes based on the resonant frequencies of the antennas. In particular, an antinode occurs at any point that is perfectly in line with two antennas of the same frequency - but only when one of the antennas is twice as far away as the other. This means that for any pair of antennas with the same frequency, there are two antinodes, one on either side of them.

# So, for these two antennas with frequency a, they create the two antinodes marked with #:

# ..........
# ...#......
# ..........
# ....a.....
# ..........
# .....a....
# ..........
# ......#...
# ..........
# ..........

# Adding a third antenna with the same frequency creates several more antinodes. It would ideally add four antinodes, but two are off the right side of the map, so instead it adds only two:

# ..........
# ...#......
# #.........
# ....a.....
# ........a.
# .....a....
# ..#.......
# ......#...
# ..........
# ..........

# Antennas with different frequencies don't create antinodes; A and a count as different frequencies. However, antinodes can occur at locations that contain antennas. In this diagram, the lone antenna with frequency capital A creates no antinodes but has a lowercase-a-frequency antinode at its location:

# ..........
# ...#......
# #.........
# ....a.....
# ........a.
# .....a....
# ..#.......
# ......A...
# ..........
# ..........

# The first example has antennas with two different frequencies, so the antinodes they create look like this, plus an antinode overlapping the topmost A-frequency antenna:

# ......#....#
# ...#....0...
# ....#0....#.
# ..#....0....
# ....0....#..
# .#....A.....
# ...#........
# #......#....
# ........A...
# .........A..
# ..........#.
# ..........#.

# Because the topmost A-frequency antenna overlaps with a 0-frequency antinode, there are 14 total unique locations that contain an antinode within the bounds of the map.

# Calculate the impact of the signal. How many unique locations within the bounds of the map contain an antinode?

# --- Part Two ---

# Watching over your shoulder as you work, one of The Historians asks if you took the effects of resonant harmonics into your calculations.

# Whoops!

# After updating your model, it turns out that an antinode occurs at any grid position exactly in line with at least two antennas of the same frequency, regardless of distance. This means that some of the new antinodes will occur at the position of each antenna (unless that antenna is the only one of its frequency).

# So, these three T-frequency antennas now create many antinodes:

# T....#....
# ...T......
# .T....#...
# .........#
# ..#.......
# ..........
# ...#......
# ..........
# ....#.....
# ..........

# In fact, the three T-frequency antennas are all exactly in line with two antennas, so they are all also antinodes! This brings the total number of antinodes in the above example to 9.

# The original example now has 34 antinodes, including the antinodes that appear on every antenna:

# ##....#....#
# .#.#....0...
# ..#.#0....#.
# ..##...0....
# ....0....#..
# .#...#A....#
# ...#..#.....
# #....#.#....
# ..#.....A...
# ....#....A..
# .#........#.
# ...#......##

# Calculate the impact of the signal using this updated model. How many unique locations within the bounds of the map contain an antinode?


import sys

sys.path.append('.')
from util import get_input

def locate_antennae(city_map):
    antennae = {}
    for i in range(len(city_map)):
        for j in range(len(city_map[i])):
            if city_map[i][j].isalnum():
                if city_map[i][j] in antennae:
                    antennae[city_map[i][j]].append((i, j))
                else:
                    antennae[city_map[i][j]] = [(i, j)]
    return antennae

def locate_antinodes(city_map, antennae, include_antennae=False, limit=float('inf')):
    antinodes = set()
    for antenna_group in antennae.values():
        for i in range(len(antenna_group) - 1):
            for j in range(i + 1, len(antenna_group)):
                a = antenna_group[i]
                b = antenna_group[j]

                dx = b[0] - a[0]
                dy = b[1] - a[1]

                if include_antennae:
                    antinodes.add(a)
                    antinodes.add(b)

                directions = [1, -1]
                for d in directions:
                    count = 0
                    antinode = a
                    while count < limit:
                        antinode = (antinode[0] + dx * d, antinode[1] + dy * d)

                        if antinode == a or antinode == b:
                            continue

                        if (
                            not 0 <= antinode[0] < len(city_map)
                            or not 0 <= antinode[1] < len(city_map[antinode[0]])
                        ):
                            break

                        antinodes.add(antinode)
                        count += 1
    return list(antinodes)

def part1(city_map, antennae):
    antinodes = locate_antinodes(city_map, antennae, limit=1)    
    print(f'part 1: {len(antinodes)}')

def part2(city_map, antennae):
    antinodes = locate_antinodes(city_map, antennae, include_antennae=True)
    print(f'part 2: {len(antinodes)}')

if __name__ == '__main__':
    city_map = list(map(list, get_input('2024/day8/input.txt')))
    antennae = locate_antennae(city_map)
    part1(city_map, antennae)
    part2(city_map, antennae)
