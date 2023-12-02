# --- Day 1: Trebuchet?! ---

# Something is wrong with global snow production, and you've been selected to take a look. The Elves have even given you a map; on it, they've used stars to mark the top fifty locations that are likely to be having problems.

# You've been doing this long enough to know that to restore snow operations, you need to check all fifty stars by December 25th.

# Collect stars by solving puzzles. Two puzzles will be made available on each day in the Advent calendar; the second puzzle is unlocked when you complete the first. Each puzzle grants one star. Good luck!

# You try to ask why they can't just use a weather machine ("not powerful enough") and where they're even sending you ("the sky") and why your map looks mostly blank ("you sure ask a lot of questions") and hang on did you just say the sky ("of course, where do you think snow comes from") when you realize that the Elves are already loading you into a trebuchet ("please hold still, we need to strap you in").

# As they're making the final adjustments, they discover that their calibration document (your puzzle input) has been amended by a very young Elf who was apparently just excited to show off her art skills. Consequently, the Elves are having trouble reading the values on the document.

# The newly-improved calibration document consists of lines of text; each line originally contained a specific calibration value that the Elves now need to recover. On each line, the calibration value can be found by combining the first digit and the last digit (in that order) to form a single two-digit number.

# For example:

# 1abc2
# pqr3stu8vwx
# a1b2c3d4e5f
# treb7uchet

# In this example, the calibration values of these four lines are 12, 38, 15, and 77. Adding these together produces 142.

# Consider your entire calibration document. What is the sum of all of the calibration values?

# --- Part Two ---

# Your calculation isn't quite right. It looks like some of the digits are actually spelled out with letters: one, two, three, four, five, six, seven, eight, and nine also count as valid "digits".

# Equipped with this new information, you now need to find the real first and last digit on each line. For example:

# two1nine
# eightwothree
# abcone2threexyz
# xtwone3four
# 4nineeightseven2
# zoneight234
# 7pqrstsixteen

# In this example, the calibration values are 29, 83, 13, 24, 42, 14, and 76. Adding these together produces 281.

# What is the sum of all of the calibration values?


import sys

sys.path.append('.')
from util import get_input

NUMBERS = [
    "one",
    "two",
    "three",
    "four",
    "five",
    "six",
    "seven",
    "eight",
    "nine"
]

class TrieNode:
    def __init__(self):
        self.word = None
        self.next = {}

def get_calibration_value(line):
    for c in line:
        if c.isnumeric():
            first_digit = c
            break
    
    for i in range(len(line) - 1, -1, -1):
        c = line[i]
        if c.isnumeric():
            last_digit = c
            break
    
    return int(first_digit + last_digit)

def part1(calibration_document):
    calibration_sum = 0
    for line in calibration_document:
        calibration_sum += get_calibration_value(line)
    
    return calibration_sum

def build_trie(strings):
    trie = TrieNode()
    for string in strings:
        ptr = trie
        for c in string:
            if not ptr.next.get(c):
                ptr.next[c] = TrieNode()
            ptr = ptr.next[c]
        ptr.word = string

    return trie

def find_spelled_out_digit(string, i, trie):
    j = i
    ptr = trie
    while j < len(string):
        c = string[j]

        if not ptr.next.get(c): break
        
        ptr = ptr.next[c]
        if ptr.word:
            return str(NUMBERS.index(ptr.word) + 1)

        j += 1

    return None

def get_correct_calibration_value(line, numbers_trie):
    digits = [None, None]
    for i in range(len(line)):
        c = line[i]

        digit = None
        if c.isnumeric():
            digit = c
        else:
            digit = find_spelled_out_digit(line, i, numbers_trie)

        if digit:
            if not digits[0]: digits[0] = digit
            digits[1] = digit
    
    return int("".join(digits))

def part2(calibration_document):
    numbers_trie = build_trie(NUMBERS)
    calibration_sum = 0
    for line in calibration_document:
        calibration_sum += get_correct_calibration_value(line, numbers_trie)

    return calibration_sum

if __name__ == "__main__":
    calibration_document = get_input("2023/day1/input.txt")
    print(f'part 1: {part1(calibration_document)}')
    print(f'part 2: {part2(calibration_document)}')
