# --- Day 11: Cosmic Expansion ---

# You continue following signs for "Hot Springs" and eventually come across an observatory. The Elf within turns out to be a researcher studying cosmic expansion using the giant telescope here.

# He doesn't know anything about the missing machine parts; he's only visiting for this research project. However, he confirms that the hot springs are the next-closest area likely to have people; he'll even take you straight there once he's done with today's observation analysis.

# Maybe you can help him with the analysis to speed things up?

# The researcher has collected a bunch of data and compiled the data into a single giant image (your puzzle input). The image includes empty space (.) and galaxies (#). For example:

# ...#......
# .......#..
# #.........
# ..........
# ......#...
# .#........
# .........#
# ..........
# .......#..
# #...#.....

# The researcher is trying to figure out the sum of the lengths of the shortest path between every pair of galaxies. However, there's a catch: the universe expanded in the time it took the light from those galaxies to reach the observatory.

# Due to something involving gravitational effects, only some space expands. In fact, the result is that any rows or columns that contain no galaxies should all actually be twice as big.

# In the above example, three columns and two rows contain no galaxies:

#    v  v  v
#  ...#......
#  .......#..
#  #.........
# >..........<
#  ......#...
#  .#........
#  .........#
# >..........<
#  .......#..
#  #...#.....
#    ^  ^  ^

# These rows and columns need to be twice as big; the result of cosmic expansion therefore looks like this:

# ....#........
# .........#...
# #............
# .............
# .............
# ........#....
# .#...........
# ............#
# .............
# .............
# .........#...
# #....#.......

# Equipped with this expanded universe, the shortest path between every pair of galaxies can be found. It can help to assign every galaxy a unique number:

# ....1........
# .........2...
# 3............
# .............
# .............
# ........4....
# .5...........
# ............6
# .............
# .............
# .........7...
# 8....9.......

# In these 9 galaxies, there are 36 pairs. Only count each pair once; order within the pair doesn't matter. For each pair, find any shortest path between the two galaxies using only steps that move up, down, left, or right exactly one . or # at a time. (The shortest path between two galaxies is allowed to pass through another galaxy.)

# For example, here is one of the shortest paths between galaxies 5 and 9:

# ....1........
# .........2...
# 3............
# .............
# .............
# ........4....
# .5...........
# .##.........6
# ..##.........
# ...##........
# ....##...7...
# 8....9.......

# This path has length 9 because it takes a minimum of nine steps to get from galaxy 5 to galaxy 9 (the eight locations marked # plus the step onto galaxy 9 itself). Here are some other example shortest path lengths:

# Between galaxy 1 and galaxy 7: 15
# Between galaxy 3 and galaxy 6: 17
# Between galaxy 8 and galaxy 9: 5

# In this example, after expanding the universe, the sum of the shortest path between all 36 pairs of galaxies is 374.

# Expand the universe, then find the length of the shortest path between every pair of galaxies. What is the sum of these lengths?

# --- Part Two ---

# The galaxies are much older (and thus much farther apart) than the researcher initially estimated.

# Now, instead of the expansion you did before, make each empty row or column one million times larger. That is, each empty row should be replaced with 1000000 empty rows, and each empty column should be replaced with 1000000 empty columns.

# (In the example above, if each empty row or column were merely 10 times larger, the sum of the shortest paths between every pair of galaxies would be 1030. If each empty row or column were merely 100 times larger, the sum of the shortest paths between every pair of galaxies would be 8410. However, your universe will need to expand far beyond these values.)

# Starting with the same initial image, expand the universe according to these new rules, then find the length of the shortest path between every pair of galaxies. What is the sum of these lengths?


from bisect import bisect_left
import sys

sys.path.append(".")
from util import get_input

def get_universe():
    universe = []
    for line in get_input("2023/day11/input.txt"):
        universe.append(list(line))

    return universe

def get_expanded_rows(universe):
    expanded_rows = []
    for i in range(len(universe)):
        if not len(list(filter(lambda x: x == "#", universe[i]))):
            expanded_rows.append(i)

    return expanded_rows

def get_expanded_columns(universe):
    expanded_columns = []
    for j in range(len(universe[0])):
        is_expanded = True
        for i in range(len(universe)):
            if universe[i][j] == "#":
                is_expanded = False
                break

        if is_expanded: expanded_columns.append(j)

    return expanded_columns

def get_galaxies(universe, expansion):
    expanded_rows = get_expanded_rows(universe)
    expanded_columns = get_expanded_columns(universe)

    galaxies = []
    for i in range(len(universe)):
        for j in range(len(universe)):
            if universe[i][j] == ".":
                continue

            additional_rows = bisect_left(expanded_rows, i) * (expansion - 1)
            additional_columns = (
                bisect_left(expanded_columns, j) * (expansion - 1)
            )

            galaxies.append((i + additional_rows, j + additional_columns))

    return galaxies

def get_shortest_path(galaxy_a, galaxy_b):
    a_x, a_y = galaxy_a
    b_x, b_y = galaxy_b

    return abs(a_x - b_x) + abs(a_y - b_y)

def get_shortest_paths_sum(universe, expansion):
    galaxies = get_galaxies(universe, expansion)
    shortest_paths_sum = 0
    for i in range(len(galaxies) - 1):
        galaxy_a = galaxies[i]
        for j in range(i + 1, len(galaxies)):
            galaxy_b = galaxies[j]
            shortest_paths_sum += get_shortest_path(galaxy_a, galaxy_b)

    return shortest_paths_sum

def part1(universe):
    return get_shortest_paths_sum(universe, 2)

def part2(universe):
    return get_shortest_paths_sum(universe, 1000000)

if __name__ == "__main__":
    universe = get_universe()

    print(f"part 1: {part1(universe)}")
    print(f"part 2: {part2(universe)}")
