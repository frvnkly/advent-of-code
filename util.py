def make_input_iterator(filename):
    with open(filename, 'r') as file:
        for line in file: yield line
        file.close()
