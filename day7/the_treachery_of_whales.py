# --- Day 7: The Treachery of Whales ---
# A giant whale has decided your submarine is its next meal, and it's much faster than you are. There's nowhere to run!

# Suddenly, a swarm of crabs (each in its own tiny submarine - it's too deep for them otherwise) zooms in to rescue you! They seem to be preparing to blast a hole in the ocean floor; sensors indicate a massive underground cave system just beyond where they're aiming!

# The crab submarines all need to be aligned before they'll have enough power to blast a large enough hole for your submarine to get through. However, it doesn't look like they'll be aligned before the whale catches you! Maybe you can help?

# There's one major catch - crab submarines can only move horizontally.

# You quickly make a list of the horizontal position of each crab (your puzzle input). Crab submarines have limited fuel, so you need to find a way to make all of their horizontal positions match while requiring them to spend as little fuel as possible.

# For example, consider the following horizontal positions:

# 16,1,2,0,4,2,7,1,2,14
# This means there's a crab with horizontal position 16, a crab with horizontal position 1, and so on.

# Each change of 1 step in horizontal position of a single crab costs 1 fuel. You could choose any horizontal position to align them all on, but the one that costs the least fuel is horizontal position 2:

# Move from 16 to 2: 14 fuel
# Move from 1 to 2: 1 fuel
# Move from 2 to 2: 0 fuel
# Move from 0 to 2: 2 fuel
# Move from 4 to 2: 2 fuel
# Move from 2 to 2: 0 fuel
# Move from 7 to 2: 5 fuel
# Move from 1 to 2: 1 fuel
# Move from 2 to 2: 0 fuel
# Move from 14 to 2: 12 fuel
# This costs a total of 37 fuel. This is the cheapest possible outcome; more expensive outcomes include aligning at position 1 (41 fuel), position 3 (39 fuel), or position 10 (71 fuel).

# Determine the horizontal position that the crabs can align to using the least fuel possible. How much fuel must they spend to align to that position?

def calculate_fuel1(positions: 'list[int]', target: int) -> int:
        fuel = 0
        for position in positions:
            distance = abs(target - position)
            fuel += distance
        return fuel

def calculate_fuel2(positions: 'list[int]', target: int) -> int:
        fuel = 0
        for position in positions:
            distance = abs(target - position)
            fuel += (distance * (distance + 1)) // 2
        return fuel

def calculate_min_total_fuel(positions: 'list[int]', calculate_fuel: 'function') -> int:
    start = min(positions)
    end = max(positions)
    while True:
        x = (start + end) // 2
        mid = calculate_fuel(positions, x)
        left = calculate_fuel(positions, x - 1)
        right = calculate_fuel(positions, x + 1)

        if left > mid < right: return mid
        elif left < mid: end = x
        else: start = x + 1

if __name__ == '__main__':
    positions = []
    f = open('input.txt', 'r')
    positions =  list(map(int, f.readline().strip().split(',')))
    f.close()

    print(f'part 1: {calculate_min_total_fuel(positions, calculate_fuel1)}')
    print(f'part 2: {calculate_min_total_fuel(positions, calculate_fuel2)}')
