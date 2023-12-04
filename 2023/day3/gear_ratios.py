# --- Day 3: Gear Ratios ---

# You and the Elf eventually reach a gondola lift station; he says the gondola lift will take you up to the water source, but this is as far as he can bring you. You go inside.

# It doesn't take long to find the gondolas, but there seems to be a problem: they're not moving.

# "Aaah!"

# You turn around to see a slightly-greasy Elf with a wrench and a look of surprise. "Sorry, I wasn't expecting anyone! The gondola lift isn't working right now; it'll still be a while before I can fix it." You offer to help.

# The engineer explains that an engine part seems to be missing from the engine, but nobody can figure out which one. If you can add up all the part numbers in the engine schematic, it should be easy to work out which part is missing.

# The engine schematic (your puzzle input) consists of a visual representation of the engine. There are lots of numbers and symbols you don't really understand, but apparently any number adjacent to a symbol, even diagonally, is a "part number" and should be included in your sum. (Periods (.) do not count as a symbol.)

# Here is an example engine schematic:

# 467..114..
# ...*......
# ..35..633.
# ......#...
# 617*......
# .....+.58.
# ..592.....
# ......755.
# ...$.*....
# .664.598..

# In this schematic, two numbers are not part numbers because they are not adjacent to a symbol: 114 (top right) and 58 (middle right). Every other number is adjacent to a symbol and so is a part number; their sum is 4361.

# Of course, the actual engine schematic is much larger. What is the sum of all of the part numbers in the engine schematic?


import sys

sys.path.append(".")
from util import get_input

def is_part_number(engine_schematic, i, j):
    directions = [
        (0, 1), (1, 0), (0, -1), (-1, 0),
        (1, 1), (1, -1), (-1, 1), (-1, -1)
    ]
    for d in directions:
        x = i + d[0]
        y = j + d[1]

        if (
            0 <= x < len(engine_schematic)
            and 0 <= y < len(engine_schematic[x])
            and not engine_schematic[x][y].isnumeric()
            and engine_schematic[x][y] != "."
        ):
            return True
        
    return False

def get_part_numbers(engine_schematic):    
    part_numbers = []
    for i in range(len(engine_schematic)):
        j = 0
        while j < len(engine_schematic[i]):
            if engine_schematic[i][j].isnumeric():
                part_number = []
                is_part = False
                for k in range(j, len(engine_schematic[i])):
                    if not engine_schematic[i][k].isnumeric():
                        break
                    
                    if not is_part and is_part_number(engine_schematic, i, k):
                        is_part = True

                    part_number.append(engine_schematic[i][k])

                if is_part:
                    part_numbers.append(int("".join(part_number)))

                j = k
            
            j += 1

    return part_numbers

def part1(engine_schematic):
    part_numbers = get_part_numbers(engine_schematic)
    return sum(part_numbers)

if __name__ == "__main__":
    engine_schematic = get_input("2023/day3/input.txt")

    print(f"part 1: {part1(engine_schematic)}")
