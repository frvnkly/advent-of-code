def gcd(a, b):
    dividend = max(a, b)
    divisor = min(a, b)
    while True:
        remainder = dividend % divisor

        if not remainder: return divisor

        dividend = divisor
        divisor = remainder

def get_input(filename):
    lines = []
    with open(filename, 'r') as file:
        for line in file: lines.append(line.strip())
        file.close()
    return lines

def lcm(a, b):
    return int(a * b / gcd(a, b))
