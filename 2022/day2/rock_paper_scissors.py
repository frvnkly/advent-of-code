import sys

sys.path.append('.')
from util import make_input_iterator

def play(a, b):
    score = 0

    points = { 'A': 1, 'B': 2, 'C': 3 }
    score += points[b]

    if a == b: score += 3
    elif a == 'A':
        if b == 'B': score += 6
    elif a == 'B':
        if b == 'C': score += 6
    elif a == 'C':
        if b == 'A': score += 6

    return score

def determine_move(opponent, outcome):
    moves = ['A', 'B', 'C']

    i = moves.index(opponent)

    offset = 0
    if outcome == 'X': offset = 2
    elif outcome == 'Z': offset = 1

    j = (i + offset) % len(moves)
    return moves[j]

def part1(turns):
    move = { 'X': 'A', 'Y': 'B', 'Z': 'C' }

    total_score = 0
    for turn in turns:
        a, b = turn.strip().split(' ')
        total_score += play(a, move[b])

    return total_score

def part2(turns):
    total_score = 0
    for turn in turns:
        a, outcome = turn.strip().split(' ')
        b = determine_move(a, outcome)
        total_score += play(a, b)

    return total_score

if __name__ == '__main__':
    turns = list(make_input_iterator('./2022/day2/input.txt'))

    print(f'part 1: {part1(turns)}')
    print(f'part 2: {part2(turns)}')
