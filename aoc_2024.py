from Assets import AoCAssets as aa
from collections import Counter
import numpy as np

def day1_a(filename):
    data = aa.read_file(filename)
    row1 = [int(x.split('  ')[0]) for x in data]
    row2 = [int(x.split('  ')[1]) for x in data]
    row1 = sorted(row1)
    row2 = sorted(row2)
    diff = [abs(r1-r2) for r1,r2 in zip(row1, row2)]
    return sum(diff)


def day1_b(filename):
    total = 0
    data = aa.read_file(filename)
    left_row = Counter([int(x.split('  ')[0]) for x in data])
    right_row = Counter([int(x.split('  ')[1]) for x in data])
    for k, v in left_row.items():
        total = (right_row.get(k, 0) * k * v) + total
    return total

def day2_a(filename):
    safe = 0
    data = aa.read_file(filename)
    for d in data:
        x = d.split()
        x = [int(z) for z in x]
        is_mono = monotonic(x)
        is_inRange = inRange(x)
        if  is_mono and is_inRange:
            safe = safe +1
        else:
            remove_outlier(x)
    return safe

def day2_b(filename):
    safe = 0
    data = aa.read_file(filename)
    for d in data:
        x = d.split()
        x = [int(z) for z in x]
        is_mono = monotonic(x)
        is_inRange = inRange(x)
        if is_mono and is_inRange:
            safe = safe + 1
        else:
            for i in range(len(x)):
                x_temp = x[:i] + x[i+1:]
                is_mono = monotonic(x_temp)
                is_inRange = inRange(x_temp)
                if is_mono and is_inRange:
                    safe = safe + 1
                    break
    return safe





print(f"day 1, part 1:  {day1_a('./data/day1_2024.txt')}")
print(f"day 1, part 2:  {day1_b('./data/day1_2024.txt')}")
print(f"day 2, part 1:  {day2_a('./data/day2_2024.txt')}")
print(f"day 2, part 2:  {day2_b('./data/day2_2024.txt')}")