# --- Day 9: Disk Fragmenter ---

# Another push of the button leaves you in the familiar hallways of some friendly amphipods! Good thing you each somehow got your own personal mini submarine. The Historians jet away in search of the Chief, mostly by driving directly into walls.

# While The Historians quickly figure out how to pilot these things, you notice an amphipod in the corner struggling with his computer. He's trying to make more contiguous free space by compacting all of the files, but his program isn't working; you offer to help.

# He shows you the disk map (your puzzle input) he's already generated. For example:

# 2333133121414131402

# The disk map uses a dense format to represent the layout of files and free space on the disk. The digits alternate between indicating the length of a file and the length of free space.

# So, a disk map like 12345 would represent a one-block file, two disk_map of free space, a three-block file, four disk_map of free space, and then a five-block file. A disk map like 90909 would represent three nine-block files in a row (with no free space between them).

# Each file on disk also has an ID number based on the order of the files as they appear before they are rearranged, starting with ID 0. So, the disk map 12345 has three files: a one-block file with ID 0, a three-block file with ID 1, and a five-block file with ID 2. Using one character for each block where digits are the file ID and . is free space, the disk map 12345 represents these individual disk_map:

# 0..111....22222

# The first example above, 2333133121414131402, represents these individual disk_map:

# 00...111...2...333.44.5555.6666.777.888899

# The amphipod would like to move file disk_map one at a time from the end of the disk to the leftmost free space block (until there are no gaps remaining between file disk_map). For the disk map 12345, the process looks like this:

# 0..111....22222
# 02.111....2222.
# 022111....222..
# 0221112...22...
# 02211122..2....
# 022111222......

# The first example requires a few more steps:

# 00...111...2...333.44.5555.6666.777.888899
# 009..111...2...333.44.5555.6666.777.88889.
# 0099.111...2...333.44.5555.6666.777.8888..
# 00998111...2...333.44.5555.6666.777.888...
# 009981118..2...333.44.5555.6666.777.88....
# 0099811188.2...333.44.5555.6666.777.8.....
# 009981118882...333.44.5555.6666.777.......
# 0099811188827..333.44.5555.6666.77........
# 00998111888277.333.44.5555.6666.7.........
# 009981118882777333.44.5555.6666...........
# 009981118882777333644.5555.666............
# 00998111888277733364465555.66.............
# 0099811188827773336446555566..............

# The final step of this file-compacting process is to update the filesystem checksum. To calculate the checksum, add up the result of multiplying each of these disk_map' position with the file ID number it contains. The leftmost block is in position 0. If a block contains free space, skip it instead.

# Continuing the first example, the first few disk_map' position multiplied by its file ID number are 0 * 0 = 0, 1 * 0 = 0, 2 * 9 = 18, 3 * 9 = 27, 4 * 8 = 32, and so on. In this example, the checksum is the sum of these, 1928.

# Compact the amphipod's hard drive using the process he requested. What is the resulting filesystem checksum? (Be careful copy/pasting the input for this puzzle; it is a single, very long line.)

# --- Part Two ---

# Upon completion, two things immediately become clear. First, the disk definitely has a lot more contiguous free space, just like the amphipod hoped. Second, the computer is running much more slowly! Maybe introducing all of that file system fragmentation was a bad idea?

# The eager amphipod already has a new plan: rather than move individual blocks, he'd like to try compacting the files on his disk by moving whole files instead.

# This time, attempt to move whole files to the leftmost span of free space blocks that could fit the file. Attempt to move each file exactly once in order of decreasing file ID number starting with the file with the highest file ID number. If there is no span of free space to the left of a file that is large enough to fit the file, the file does not move.

# The first example from above now proceeds differently:

# 00...111...2...333.44.5555.6666.777.888899
# 0099.111...2...333.44.5555.6666.777.8888..
# 0099.1117772...333.44.5555.6666.....8888..
# 0099.111777244.333....5555.6666.....8888..
# 00992111777.44.333....5555.6666.....8888..

# The process of updating the filesystem checksum is the same; now, this example's checksum would be 2858.

# Start over, now compacting the amphipod's hard drive using this new method instead. What is the resulting filesystem checksum?


from collections import deque
import sys

sys.path.append('.')
from util import get_input

def get_disk_map():
    s = get_input('2024/day9/input.txt')[0]
    disk_map = deque()
    file_id = 0
    for i in range(0, len(s), 2):
        disk_map.append([file_id, int(s[i])])
        file_id += 1

        if i + 1 < len(s) and s[i+1] != '0':
            disk_map.append([None, int(s[i+1])])
    while disk_map[-1][0] is None:
        disk_map.pop()
    return disk_map

def calculate_checksum(disk_map):
    checksum = 0
    position = 0
    for file_id, num_disk_map in disk_map:
        for n in range(num_disk_map):
            if file_id is None: continue
            checksum += file_id * (position + n)
        position += num_disk_map
    return checksum

def part1():
    disk_map = get_disk_map()

    compressed = []
    while disk_map:
        if not disk_map[0][0] is None:
            compressed.append(disk_map.popleft())
            continue
        
        num_disk_map = min(disk_map[0][1], disk_map[-1][1])
        compressed.append([disk_map[-1][0], num_disk_map])
        disk_map[0][1] -= num_disk_map
        if disk_map[0][1] <= 0: disk_map.popleft()
        disk_map[-1][1] -= num_disk_map
        if disk_map[-1][1] <= 0: disk_map.pop()

        while disk_map and disk_map[-1][0] is None:
            disk_map.pop()

    print(f'part 1: {calculate_checksum(compressed)}')

def part2():
    disk_map = get_disk_map()

    compressed = []
    while disk_map:
        next_span = disk_map.popleft()

        if not next_span[0] is None:
            compressed.append(next_span)
            continue
        
        while next_span[1] > 0:
            while disk_map and disk_map[-1][0] is None:
                disk_map.pop()

            shifted = False
            for i in range(len(disk_map) - 1, -1, -1):
                if disk_map[i][0] is None:
                    continue

                if disk_map[i][1] <= next_span[1]:
                    compressed.append([disk_map[i][0], disk_map[i][1]])
                    next_span[1] -= disk_map[i][1]
                    disk_map[i][0] = None
                    shifted = True
                    break
                    
            if not shifted:
                compressed.append(next_span)
                break

    print(f'part 2: {calculate_checksum(compressed)}')

if __name__ == '__main__':
    part1()
    part2()
