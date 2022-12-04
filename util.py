def get_input(filename):
    lines = []
    with open(filename, 'r') as file:
        for line in file: lines.append(line.strip())
        file.close()
    return lines
