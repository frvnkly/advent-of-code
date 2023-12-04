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

# --- Part Two ---

# The engineer finds the missing part and installs it in the engine! As the engine springs to life, you jump in the closest gondola, finally ready to ascend to the water source.

# You don't seem to be going very fast, though. Maybe something is still wrong? Fortunately, the gondola has a phone labeled "help", so you pick it up and the engineer answers.

# Before you can explain the situation, she suggests that you look out the window. There stands the engineer, holding a phone in one hand and waving with the other. You're going so slowly that you haven't even left the station. You exit the gondola.

# The missing part wasn't the only issue - one of the gears in the engine is wrong. A gear is any * symbol that is adjacent to exactly two part numbers. Its gear ratio is the result of multiplying those two numbers together.

# This time, you need to find the gear ratio of every gear and add them all up so that the engineer can figure out which gear needs to be replaced.

# Consider the same engine schematic again:

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

# In this schematic, there are two gears. The first is in the top left; it has part numbers 467 and 35, so its gear ratio is 16345. The second gear is in the lower right; its gear ratio is 451490. (The * adjacent to 617 is not a gear because it is only adjacent to one part number.) Adding up all of the gear ratios produces 467835.

# What is the sum of all of the gear ratios in your engine schematic?


import sys

sys.path.append(".")
from util import get_input

def get_full_part_number(engine_schematic, row, column):
    start = column
    while start > 0:
        if engine_schematic[row][start-1].isnumeric():
            start -= 1
        else:
            break

    end = column
    while end < len(engine_schematic[row]) - 1:
        if engine_schematic[row][end+1].isnumeric():
            end += 1
        else:
            break

    return int(engine_schematic[row][start:end+1])

def get_adjacent_part_numbers(engine_schematic, row, column):
    part_numbers = []

    # left part number
    if column > 0 and engine_schematic[row][column-1].isnumeric():
        part_numbers.append(
            get_full_part_number(engine_schematic, row, column - 1)
        )

    # right part number
    if (
        column < len(engine_schematic[row]) - 1
        and engine_schematic[row][column+1].isnumeric()
    ):
        part_numbers.append(
            get_full_part_number(engine_schematic, row, column + 1)
        )

    # previous row part numbers
    if row > 0:
        if column > 0 and engine_schematic[row-1][column-1].isnumeric():
            part_numbers.append(
                get_full_part_number(engine_schematic, row - 1, column - 1)
            )

        if (
            (column == 0 or engine_schematic[row-1][column-1] == ".")
            and engine_schematic[row-1][column].isnumeric()
        ):
            part_numbers.append(
                get_full_part_number(engine_schematic, row - 1, column)
            )

        if (
            column < len(engine_schematic[row-1]) - 1
            and engine_schematic[row-1][column] == "."
            and engine_schematic[row-1][column+1].isnumeric()
        ):
            part_numbers.append(
                get_full_part_number(engine_schematic, row - 1, column + 1)
            )

    # next row part numbers
    if row < len(engine_schematic) - 1:
        if column > 0 and engine_schematic[row+1][column-1].isnumeric():
            part_numbers.append(
                get_full_part_number(engine_schematic, row + 1, column - 1)
            )

        if (
            (column == 0 or engine_schematic[row+1][column-1] == ".")
            and engine_schematic[row+1][column].isnumeric()
        ):
            part_numbers.append(
                get_full_part_number(engine_schematic, row + 1, column)
            )

        if (
            column < len(engine_schematic[row+1]) - 1
            and engine_schematic[row+1][column] == "."
            and engine_schematic[row+1][column+1].isnumeric()
        ):
            part_numbers.append(
                get_full_part_number(engine_schematic, row + 1, column + 1)
            )

    return part_numbers

def get_part_numbers(engine_schematic):    
    part_numbers = []
    for i in range(len(engine_schematic)):
        for j in range(len(engine_schematic[i])):
            if (
                not engine_schematic[i][j].isnumeric()
                and engine_schematic[i][j] != "."
            ):
                part_numbers.extend(
                    get_adjacent_part_numbers(engine_schematic, i, j)
                )

    return part_numbers

def get_gear_ratio(engine_schematic, row, column):
    part_numbers = get_adjacent_part_numbers(engine_schematic, row, column)

    if len(part_numbers) == 2:
        return part_numbers[0] * part_numbers[1]
    
    return None

def get_gear_ratios(engine_schematic):
    gear_ratios = []

    for i in range(len(engine_schematic)):
        for j in range(len(engine_schematic[i])):
            if engine_schematic[i][j] == "*":
                gear_ratio = get_gear_ratio(engine_schematic, i, j)
                if not gear_ratio is None:
                    gear_ratios.append(gear_ratio)

    return gear_ratios

def part1(engine_schematic):
    part_numbers = get_part_numbers(engine_schematic)
    return sum(part_numbers)

def part2(engine_schematic):
    gear_ratios = get_gear_ratios(engine_schematic)
    return sum(gear_ratios)

if __name__ == "__main__":
    engine_schematic = get_input("2023/day3/input.txt")

    print(f"part 1: {part1(engine_schematic)}")
    print(f"part 2: {part2(engine_schematic)}")
