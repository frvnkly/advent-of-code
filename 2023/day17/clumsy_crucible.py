# --- Day 17: Clumsy Crucible ---

# The lava starts flowing rapidly once the Lava Production Facility is operational. As you leave, the reindeer offers you a parachute, allowing you to quickly reach Gear Island.

# As you descend, your bird's-eye view of Gear Island reveals why you had trouble finding anyone on your way up: half of Gear Island is empty, but the half below you is a giant factory city!

# You land near the gradually-filling pool of lava at the base of your new lavafall. Lavaducts will eventually carry the lava throughout the city, but to make use of it immediately, Elves are loading it into large crucibles on wheels.

# The crucibles are top-heavy and pushed by hand. Unfortunately, the crucibles become very difficult to steer at high speeds, and so it can be hard to go in a straight line for very long.

# To get Desert Island the machine parts it needs as soon as possible, you'll need to find the best way to get the crucible from the lava pool to the machine parts factory. To do this, you need to minimize heat loss while choosing a route that doesn't require the crucible to go in a straight line for too long.

# Fortunately, the Elves here have a map (your puzzle input) that uses traffic patterns, ambient temperature, and hundreds of other parameters to calculate exactly how much heat loss can be expected for a crucible entering any particular city block.

# For example:

# 2413432311323
# 3215453535623
# 3255245654254
# 3446585845452
# 4546657867536
# 1438598798454
# 4457876987766
# 3637877979653
# 4654967986887
# 4564679986453
# 1224686865563
# 2546548887735
# 4322674655533

# Each city block is marked by a single digit that represents the amount of heat loss if the crucible enters that block. The starting point, the lava pool, is the top-left city block; the destination, the machine parts factory, is the bottom-right city block. (Because you already start in the top-left block, you don't incur that block's heat loss unless you leave that block and then return to it.)

# Because it is difficult to keep the top-heavy crucible going in a straight line for very long, it can move at most three blocks in a single direction before it must turn 90 degrees left or right. The crucible also can't reverse direction; after entering each city block, it may only turn left, continue straight, or turn right.

# One way to minimize heat loss is this path:

# 2>>34^>>>1323
# 32v>>>35v5623
# 32552456v>>54
# 3446585845v52
# 4546657867v>6
# 14385987984v4
# 44578769877v6
# 36378779796v>
# 465496798688v
# 456467998645v
# 12246868655<v
# 25465488877v5
# 43226746555v>

# This path never moves more than three consecutive blocks in the same direction and incurs a heat loss of only 102.

# Directing the crucible from the lava pool to the machine parts factory, but not moving more than three consecutive blocks in the same direction, what is the least heat loss it can incur?


import heapq
import sys

sys.path.append(".")
from util import get_input

def get_city_map():
    city_map = []
    for line in get_input("2023/day17/input.txt"):
        city_map.append(list(map(int, list(line))))

    return city_map

def part1(city_map):
    history = [
        [
            [
                [False] * 3 for __ in range(4)
            ] for ___ in range(len(city_map[0]))
        ] for ____ in range(len(city_map))
    ]

    heap = [[0, 0, 0, 0, 0]]
    while heap:
        loss, row, col, direction, times = heapq.heappop(heap)

        if row == len(city_map) - 1 and col == len(city_map[row]) - 1:
            return loss
        
        if history[row][col][direction][times-1]: continue

        history[row][col][direction][times-1] = True
        
        if direction != 2 and not (direction == 0 and times >= 3):
            next_row = row - 1
            next_times = times + 1 if direction == 0 else 1
            if next_row >= 0 and not history[next_row][col][0][next_times-1]:
                heapq.heappush(
                    heap,
                    [
                        loss + city_map[next_row][col],
                        next_row,
                        col,
                        0,
                        next_times
                    ]
                )

        if direction != 3 and not (direction == 1 and times >= 3):
            next_col = col + 1
            next_times = times + 1 if direction == 1 else 1
            if (
                next_col < len(city_map[row]) and
                not history[row][next_col][1][next_times-1]
            ):
                heapq.heappush(
                    heap,
                    [
                        loss + city_map[row][next_col],
                        row,
                        next_col,
                        1,
                        next_times
                    ]
                )

        if direction != 0 and not (direction == 2 and times >= 3):
            next_row = row + 1
            next_times = times + 1 if direction == 2 else 1
            if (
                next_row < len(city_map) and
                not history[next_row][col][2][next_times-1]
            ):
                heapq.heappush(
                    heap,
                    [
                        loss + city_map[next_row][col],
                        next_row,
                        col,
                        2,
                        next_times
                    ]
                )

        if direction != 1 and not (direction == 3 and times >= 3):
            next_col = col - 1
            if next_col >= 0 and not history[row][next_col][3][next_times-1]:
                heapq.heappush(
                    heap,
                    [
                        loss + city_map[row][next_col],
                        row,
                        next_col,
                        3,
                        next_times
                    ]
                )

if __name__ == "__main__":
    city_map = get_city_map()

    print(f"part 1: {part1(city_map)}")
