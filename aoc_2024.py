from Assets import AoCAssets as aa
from collections import Counter

def day1_a(filename):
    data = aa.read_file(filename)
    row1 = [int(x.split('  ')[0]) for x in data]
    row2 = [int(x.split('  ')[1]) for x in data]
    row1 = sorted(row1)
    row2 = sorted(row2)
    diff = [abs(r1-r2) for r1,r2 in zip(row1, row2)]
    print(sum(diff))


def day1_b(filename):
    total = 0
    data = aa.read_file(filename)
    left_row = Counter([int(x.split('  ')[0]) for x in data])
    right_row = Counter([int(x.split('  ')[1]) for x in data])
    for k, v in left_row.items():
        total = (right_row.get(k, 0) * k * v) + total
    print(total)


day1_b('./data/day1_2024.txt')


    