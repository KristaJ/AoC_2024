from Assets import AoCAssets as aa
from collections import Counter
import re

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
        if monotonic(x) and inRange(x):
            safe = safe +1
    return safe

def day2_b(filename):
    safe = 0
    data = aa.read_file(filename)
    for d in data:
        x = d.split()
        x = [int(z) for z in x]
        if monotonic(x) and inRange(x):
            safe = safe + 1
        else:
            for i in range(len(x)):
                x_temp = x[:i] + x[i+1:]
                if monotonic(x_temp) and inRange(x_temp):
                    safe = safe + 1
                    break
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
        return False
    else:
        return True

class day3:
    def __init__(self, filename):
        self.data = aa.read_file(filename)
        self.matches = self.parse_input()
        self.matches2 = self.parse_input_part2()
        self.total1 = self.parse_matches()
        self.total2 = self.parse_matches_part2()

    def parse_input(self):
        reg_ex = r'mul\([0-9]{1,3},[0-9]{1,3}\)'
        matches = []
        for l in self.data:
            matches.extend(re.findall(reg_ex, l))
        return matches

    def parse_matches(self):
        total = 0
        for match in self.matches:
            nums = match.split("(")[1].split(")")[0].split(",")
            total = total + (int(nums[0]) * int(nums[1]))
        return total

    def parse_input_part2(self):
        reg_ex1 = r'mul\([0-9]{1,3},[0-9]{1,3}\)'
        reg_ex2 = r'do\(\)'
        reg_ex3 = r'don\'t\(\)'
        all_reg_ex = '|'.join(f'(?:{x})' for x in ([reg_ex1, reg_ex2, reg_ex3]))
        matches = []
        for l in self.data:
            matches.extend(re.findall(all_reg_ex, l))
        return matches

    def parse_matches_part2(self):
        total = 0
        do_mult = True
        for match in self.matches2:
            if (match == 'don\'t()') & (do_mult):
                do_mult = False
            elif (match == 'do()') & (not do_mult):
                do_mult = True
            elif match.startswith('mul'):
                if do_mult:
                    nums = match.split("(")[1].split(")")[0].split(",")
                    total = total + (int(nums[0]) * int(nums[1]))
        return total


# print(f"day 1, part 1:  {day1_a('./data/day1_2024.txt')}")
# print(f"day 1, part 2:  {day1_b('./data/day1_2024.txt')}")
# print(f"day 2, part 1:  {day2_a('./data/day2_2024.txt')}")
# print(f"day 2, part 2:  {day2_b('./data/day2_2024.txt')}")
d3 = day3('./data/day3_2024.txt')
print(f"day 2, part 1:  {d3.total1}")
print(f"day 2, part 2:  {d3.total2}")

