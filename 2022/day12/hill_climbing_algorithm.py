# --- Day 12: Hill Climbing Algorithm ---

# You try contacting the Elves using your handheld device, but the river you're following must be too low to get a decent signal.

# You ask the device for a heightmap of the surrounding area (your puzzle input). The heightmap shows the local area from above broken into a grid; the elevation of each square of the grid is given by a single lowercase letter, where a is the lowest elevation, b is the next-lowest, and so on up to the highest elevation, z.

# Also included on the heightmap are marks for your current position (S) and the location that should get the best signal (E). Your current position (S) has elevation a, and the location that should get the best signal (E) has elevation z.

# You'd like to reach E, but to save energy, you should do it in as few steps as possible. During each step, you can move exactly one square up, down, left, or right. To avoid needing to get out your climbing gear, the elevation of the destination square can be at most one higher than the elevation of your current square; that is, if your current elevation is m, you could step to elevation n, but not to elevation o. (This also means that the elevation of the destination square can be much lower than the elevation of your current square.)

# For example:

# Sabqponm
# abcryxxl
# accszExk
# acctuvwj
# abdefghi

# Here, you start in the top-left corner; your goal is near the middle. You could start by moving down or right, but eventually you'll need to head toward the e at the bottom. From there, you can spiral around to the goal:

# v..v<<<<
# >v.vv<<^
# .>vv>E^^
# ..v>>>^^
# ..>>>>>^

# In the above diagram, the symbols indicate whether the path exits each square moving up (^), down (v), left (<), or right (>). The location that should get the best signal is still E, and . marks unvisited squares.

# This path reaches the goal in 31 steps, the fewest possible.

# What is the fewest steps required to move from your current position to the location that should get the best signal?

# --- Part Two ---

# As you walk up the hill, you suspect that the Elves will want to turn this into a hiking trail. The beginning isn't very scenic, though; perhaps you can find a better starting point.

# To maximize exercise while hiking, the trail should start as low as possible: elevation a. The goal is still the square marked E. However, the trail should still be direct, taking the fewest steps to reach its goal. So, you'll need to find the shortest path from any square at elevation a to the square marked E.

# Again consider the example from above:

# Sabqponm
# abcryxxl
# accszExk
# acctuvwj
# abdefghi

# Now, there are six choices for starting position (five marked a, plus the square marked S that counts as being at elevation a). If you start at the bottom-left square, you can reach the goal most quickly:

# ...v<<<<
# ...vv<<^
# ...v>E^^
# .>v>>>^^
# >^>>>>>^

# This path reaches the goal in only 29 steps, the fewest possible.

# What is the fewest steps required to move starting from any square with elevation a to the location that should get the best signal?

import sys

sys.path.append('.')
from util import get_input

def get_start(heightmap):
    for i in range(len(heightmap)):
        for j in range(len(heightmap[i])):
            if heightmap[i][j] == 'S':
                return (i, j)

def get_starts(heightmap):
    starts = []
    for i in range(len(heightmap)):
        for j in range(len(heightmap[i])):
            if heightmap[i][j] in ['a', 'S']:
                starts.append((i, j))

    return starts

def get_minimum_steps(heightmap, start):
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    
    level = []
    for d in directions:
        a = start[0] + d[0]
        b = start[1] + d[1]

        if (
            0 <= a < len(heightmap) and
            0 <= b < len(heightmap[a]) and
            'a' <= heightmap[a][b] <= 'b'
        ): level.append((a, b))

    visited = [[False] * len(heightmap[0]) for _ in range(len(heightmap))]
    visited[start[0]][start[1]] = True
    step = 1
    while level:
        next_level = []

        for i, j in level:
            if visited[i][j]: continue
            visited[i][j] = True

            for d in directions:
                a = i + d[0]
                b = j + d[1]

                if (
                    0 <= a < len(heightmap) and 
                    0 <= b < len(heightmap[a])
                ):
                    if heightmap[a][b] == 'E':
                        if 'y' <= heightmap[i][j] <= 'z':
                            return step + 1
                    elif ord(heightmap[a][b]) - ord(heightmap[i][j]) <= 1:
                        next_level.append((a, b))

        level = next_level
        step += 1

def part1(heightmap):
    start = get_start(heightmap)
    return get_minimum_steps(heightmap, start)

def part2(heightmap):
    starts = get_starts(heightmap)
    paths = filter(
        lambda x: not x is None,
        map(
            lambda start: get_minimum_steps(heightmap, start),
            starts
        )
    )
    return min(paths)

if __name__ == '__main__':
    heightmap = get_input('2022/day12/input.txt')
    
    print(f'part 1: {part1(heightmap)}')
    print(f'part 2: {part2(heightmap)}')
