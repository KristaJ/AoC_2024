from Assets import AoCAssets as aa
from collections import Counter

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
        _, is_mono = monotonic(x)
        is_inRange = inRange(x)
        if  is_mono and is_inRange:
            safe = safe +1
    return safe

def day2_b(filename):
    safe = 0
    data = aa.read_file(filename)
    for d in data:
        x = d.split()
        x_orig = x.copy()
        x, is_mono = monotonic(x, damp = True)
        is_inRange = inRange(x)
        if  is_mono and is_inRange:
            safe = safe + 1
        if not is_mono:
            print(x_orig, x, is_mono)
    return safe

def inRange(x):
    diffs = [int(x[i - 1]) - int(x[i]) for i in range(1, len(x))]
    if any([abs(x) < 1 for x in diffs]) or any([abs(x) > 3 for x in diffs]):
        return False
    else:
        return True

def monotonic(x, damp = False):
    diffs = [int(x[i - 1]) - int(x[i]) for i in range(1, len(x))]
    if not(all([x<0 for x in diffs]) or all([x>0 for x in diffs])):
        if damp:
            return dampen(x)
        else:
            return (x, False)
    else:
        return (x, True)

def dampen(x):
    print(x)
    diffs = [int(x[i - 1]) - int(x[i]) for i in range(1, len(x))]
    print(diffs)
    # # print(diffs)
    # # if a diff is 0 that is where the plateau is:
    # try:
    #     prob_index = diffs.index(0)
    # except ValueError:
    trend = max(set(['inc' if x<0 else'dec' for x in diffs]), key=['inc' if x<0 else'dec' for x in diffs].count)
    print(f"__{trend}__")
    if trend == 'inc':
        temp_x = [x[i] for i in range(len(x)-1) if x[i] < x[i+1]]
        temp_x.append(x[-1])
    else:
        temp_x = [x[i] for i in range(len(x)-1) if x[i] > x[i+1]]
        temp_x.append(x[-1])
    print(temp_x)
    #     most_common = max(set([x<0 for x in diffs]), key=[x<0 for x in diffs].count)
    #     prob_index = [x<0 for x in diffs].index(not(most_common))
    # del x[prob_index+1]
    x, mono = monotonic(temp_x)
    return x, mono



print(f"day 1, part 1:  {day1_a('./data/day1_2024.txt')}")
print(f"day 1, part 2:  {day1_b('./data/day1_2024.txt')}")
print(f"day 2, part 1:  {day2_a('./data/day2_2024.txt')}")
# print(f"day 2, part 2:  {day2_b('./data/day2_2024.txt')}")

    