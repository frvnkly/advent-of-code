# --- Day 4: Ceres Search ---

# "Looks like the Chief's not here. Next!" One of The Historians pulls out a device and pushes the only button on it. After a brief flash, you recognize the interior of the Ceres monitoring station!

# As the search for the Chief continues, a small Elf who lives on the station tugs on your shirt; she'd like to know if you could help her with her word search (your puzzle input). She only has to find one word: XMAS.

# This word search allows words to be horizontal, vertical, diagonal, written backwards, or even overlapping other words. It's a little unusual, though, as you don't merely need to find one instance of XMAS - you need to find all of them. Here are a few ways XMAS might appear, where irrelevant characters have been replaced with .:

# ..X...
# .SAMX.
# .A..A.
# XMAS.S
# .X....

# The actual word search will be full of letters instead. For example:

# MMMSXXMASM
# MSAMXMSMSA
# AMXSXMAAMM
# MSAMASMSMX
# XMASAMXAMM
# XXAMMXXAMA
# SMSMSASXSS
# SAXAMASAAA
# MAMMMXMMMM
# MXMXAXMASX

# In this word search, XMAS occurs a total of 18 times; here's the same word search again, but where letters not involved in any XMAS have been replaced with .:

# ....XXMAS.
# .SAMXMS...
# ...S..A...
# ..A.A.MS.X
# XMASAMX.MM
# X.....XA.A
# S.S.S.S.SS
# .A.A.A.A.A
# ..M.M.M.MM
# .X.X.XMASX

# Take a look at the little Elf's word search. How many times does XMAS appear?

# --- Part Two ---

# The Elf looks quizzically at you. Did you misunderstand the assignment?

# Looking for the instructions, you flip over the word search to find that this isn't actually an XMAS puzzle; it's an X-MAS puzzle in which you're supposed to find two MAS in the shape of an X. One way to achieve that is like this:

# M.S
# .A.
# M.S

# Irrelevant characters have again been replaced with . in the above diagram. Within the X, each MAS can be written forwards or backwards.

# Here's the same example from before, but this time all of the X-MASes have been kept instead:

# .M.S......
# ..A..MSMS.
# .M.S.MAA..
# ..A.ASMSM.
# .M.S.M....
# ..........
# S.S.S.S.S.
# .A.A.A.A..
# M.M.M.M.M.
# ..........

# In this example, an X-MAS appears 9 times.

# Flip the word search from the instructions back over to the word search side and try again. How many times does an X-MAS appear?


import sys

sys.path.append('.')
from util import get_input

def search(word_search, x, y, dx, dy, s):
    found = True
    for i in range(len(s)):
        if (
            not 0 <= x + dx * i < len(word_search)
            or not 0 <= y + dy * i < len(word_search[x + dx * i])
            or word_search[x + dx * i][y + dy * i] != s[i]
        ):
            found = False
            break
    return found

def part1(word_search):
    num_xmas = 0
    for x in range(len(word_search)):
        for y in range(len(word_search)):
            for dx, dy in [
                (0, 1), (1, 0),
                (0, -1), (-1, 0),
                (1, 1), (1, -1),
                (-1, 1), (-1, -1)
            ]:
                if search(word_search, x, y, dx, dy, 'XMAS'):
                    num_xmas += 1

    print(f'part 1: {num_xmas}')

def part2(word_search):
    num_xmas = 0
    for x in range(1, len(word_search) - 1):
        for y in range(1, len(word_search) - 1):
            if (
                (
                    search(word_search, x - 1, y - 1, 1, 1, 'MAS')
                    or search(word_search, x - 1, y - 1, 1, 1, 'SAM')
                ) and (
                    search(word_search, x - 1, y + 1, 1, -1, 'MAS')
                    or search(word_search, x - 1, y + 1, 1, -1, 'SAM')
                )
            ):
                num_xmas += 1

    print(f'part 2: {num_xmas}')

if __name__ == '__main__':
    word_search = get_input('2024/day4/input.txt')
    part1(word_search)
    part2(word_search)
