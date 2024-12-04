# --- Day 3: Mull It Over ---

# "Our computers are having issues, so I have no idea if we have any Chief Historians in stock! You're welcome to check the warehouse, though," says the mildly flustered shopkeeper at the North Pole Toboggan Rental Shop. The Historians head out to take a look.

# The shopkeeper turns to you. "Any chance you can see why our computers are having issues again?"

# The computer appears to be trying to run a program, but its memory (your puzzle input) is corrupted. All of the instructions have been jumbled up!

# It seems like the goal of the program is just to multiply some numbers. It does that with instructions like mul(X,Y), where X and Y are each 1-3 digit numbers. For instance, mul(44,46) multiplies 44 by 46 to get a result of 2024. Similarly, mul(123,4) would multiply 123 by 4.

# However, because the program's memory has been corrupted, there are also many invalid characters that should be ignored, even if they look like part of a mul instruction. Sequences like mul(4*, mul(6,9!, ?(12,34), or mul ( 2 , 4 ) do nothing.

# For example, consider the following section of corrupted memory:

# xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))

# Only the four highlighted sections are real mul instructions. Adding up the result of each instruction produces 161 (2*4 + 5*5 + 11*8 + 8*5).

# Scan the corrupted memory for uncorrupted mul instructions. What do you get if you add up all of the results of the multiplications?


from functools import reduce
import sys

sys.path.append('.')
from util import get_input

def part1(memory):
    mul_sum = 0
    for line in memory:
        i = 0
        while i < len(line) - 4:
            if line[i:i+4] != 'mul(':
                i += 1
                continue
            
            start = i + 4
            end = start
            while end < len(line):
                if line[end] == ')':
                    break
                
                if (
                    line[end].isnumeric()
                    or (line[end] == ',' and line[end-1] != ',')
                ):
                    end += 1
                    continue
                
                end = start
                break
            if start < end:
                factors = list(map(int, line[start:end].split(',')))                
                if len(factors) > 1:
                    product = reduce(lambda a, b: a * b, factors)
                    print(line[i:end + 1], factors, product)
                    mul_sum += product
            i = end + 1
    
    print(f'part 1: {mul_sum}')

if __name__ == '__main__':
    memory = get_input('2024/day3/input.txt')
    part1(memory)
