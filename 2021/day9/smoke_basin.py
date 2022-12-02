# --- Day 9: Smoke Basin ---
# These caves seem to be lava tubes. Parts are even still volcanically active; small hydrothermal vents release smoke into the caves that slowly settles like rain.

# If you can model how the smoke flows through the caves, you might be able to avoid it and be that much safer. The submarine generates a heightmap of the floor of the nearby caves for you (your puzzle input).

# Smoke flows to the lowest point of the area it's in. For example, consider the following heightmap:

# 2199943210
# 3987894921
# 9856789892
# 8767896789
# 9899965678
# Each number corresponds to the height of a particular location, where 9 is the highest and 0 is the lowest a location can be.

# Your first goal is to find the low points - the locations that are lower than any of its adjacent locations. Most locations have four adjacent locations (up, down, left, and right); locations on the edge or corner of the map have three or two adjacent locations, respectively. (Diagonal locations do not count as adjacent.)

# In the above example, there are four low points, all highlighted: two are in the first row (a 1 and a 0), one is in the third row (a 5), and one is in the bottom row (also a 5). All other locations on the heightmap have some lower adjacent location, and so are not low points.

# The risk level of a low point is 1 plus its height. In the above example, the risk levels of the low points are 2, 1, 6, and 6. The sum of the risk levels of all low points in the heightmap is therefore 15.

# Find all of the low points on your heightmap. What is the sum of the risk levels of all low points on your heightmap?

# --- Part Two ---
# Next, you need to find the largest basins so you know what areas are most important to avoid.

# A basin is all locations that eventually flow downward to a single low point. Therefore, every low point has a basin, although some basins are very small. Locations of height 9 do not count as being in any basin, and all other locations will always be part of exactly one basin.

# The size of a basin is the number of locations within the basin, including the low point. The example above has four basins.

# The top-left basin, size 3:

# 2199943210
# 3987894921
# 9856789892
# 8767896789
# 9899965678
# The top-right basin, size 9:

# 2199943210
# 3987894921
# 9856789892
# 8767896789
# 9899965678
# The middle basin, size 14:

# 2199943210
# 3987894921
# 9856789892
# 8767896789
# 9899965678
# The bottom-right basin, size 9:

# 2199943210
# 3987894921
# 9856789892
# 8767896789
# 9899965678
# Find the three largest basins and multiply their sizes together. In the above example, this is 9 * 14 * 9 = 1134.

# What do you get if you multiply together the sizes of the three largest basins?

def find_risk_points(heightmap: 'list[list[int]]') -> 'list[tuple[int, int]]':
    risk_points = []
    for i in range(len(heightmap)):
        for  j in range(len(heightmap[i])):
            is_risky = True
            for d in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                x = i + d[0]
                y = j + d[1]

                if 0 <= x < len(heightmap) and 0 <= y < len(heightmap[x]):
                    if heightmap[x][y] <= heightmap[i][j]:
                        is_risky = False
                        break

            if is_risky: risk_points.append((i, j))

    return risk_points

def get_risk_score(
    heightmap: 'list[list[int]]',
    risk_points: 'list[tuple[int, int]]'
) -> int:
    risk_score = 0
    for x, y in risk_points:
        risk_score += heightmap[x][y] + 1
    return risk_score

def get_basin_score(
    heightmap: 'list[list[int]]',
    risk_points: 'list[tuple[int, int]]'
) -> int:
    basin_sizes = []
    for risk_point in risk_points:
        basin = set()
        stack = [risk_point]
        while stack:
            point = stack.pop()
            basin.add(point)

            i, j = point
            for d in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                x = i + d[0]
                y = j + d[1]                

                if (
                    0 <= x < len(heightmap) and
                    0 <= y < len(heightmap[x]) and 
                    not (x, y) in basin and
                    heightmap[i][j] < heightmap[x][y] < 9
                ):
                    stack.append((x, y))

        basin_sizes.append(len(basin))

    basin_score = 1
    for size in sorted(basin_sizes)[-3:]: basin_score *= size
    return basin_score

if __name__ == '__main__':
    heightmap = []
    with open('input.txt', 'r') as f:
        for line in f:
            row = list(map(int, list(line.strip())))
            heightmap.append(row)
        f.close()

    risk_points = find_risk_points(heightmap)

    print(f'part 1: {get_risk_score(heightmap, risk_points)}')
    print(f'part 2: {get_basin_score(heightmap, risk_points)}')
