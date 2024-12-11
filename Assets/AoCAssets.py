import numpy as np

def read_file(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()
        lines = [x.strip() for x in lines]
    return lines


def read_file_cr(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()
        lines = [x.strip('\n') for x in lines]
    return lines

def read_matrix(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()
        lines = [x.strip() for x in lines]
    data = [[x for x in data_line] for data_line in lines]
    matrix = np.array(data)
    return matrix