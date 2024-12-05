from Assets import AoCAssets as aa
from collections import Counter
import re
import numpy as np
from collections import defaultdict
import math


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

class day4:
    def __init__(self, filename):
        self.data = aa.read_file(filename)
        self.data_matrix = self.data_to_matrix()
        self.rotated_data = self.rotate_matrix()
        self.letter_coords = self.get_letter_coords()
        self.matches1 = self.matches()
        self.matches2 = self.matches_part2()

    def data_to_matrix(self):
        data = [[x for x in data_line] for data_line in self.data]
        matrix = np.array(data)
        return matrix

    def read_right(self):
        matches = 0
        for line in self.data:
            matches = matches + len(re.findall('XMAS', line))
        return matches

    def read_left(self):
        matches = 0
        for line in self.data:
            matches = matches + len(re.findall('SAMX', line))
        return matches

    def read_up(self):
        matches = 0
        for line in self.rotated_data:
            matches = matches + len(re.findall('XMAS', line))
        return matches

    def read_down(self):
        matches = 0
        for line in self.rotated_data:
            matches = matches + len(re.findall('SAMX', line))
        return matches

    def get_letter_coords(self):
        letter_coords = {}
        for letter in ['X', 'M', 'A', 'S']:
            ii = np.where(self.data_matrix == letter)
            letter_coords[letter] = list(zip(ii[0].tolist(), ii[1].tolist()))
        return letter_coords

    def read_diag(self, xchange, ychange):
        M_coords = [(c[0]+ychange, c[1]+xchange) for c in self.letter_coords['X']]
        found_M_coords = [x for x in M_coords if x in self.letter_coords['M']]
        A_coords = [(c[0]+ychange, c[1]+xchange) for c in found_M_coords]
        found_A_coords = [x for x in A_coords if x in self.letter_coords['A']]
        S_coords = [(c[0]+ychange, c[1]+xchange) for c in found_A_coords]
        found_S_coords = [x for x in S_coords if x in self.letter_coords['S']]
        return found_S_coords

    def read_down_right(self):
        return self.read_diag(1, 1)

    def read_down_left(self):
        return self.read_diag(1, -1)

    def read_up_right(self):
        return self.read_diag(-1, 1)

    def read_up_left(self):
        return self.read_diag(-1, -1)

    def rotate_matrix(self):
        rotated_data = [''.join(line) for line in self.data_matrix.T]
        return rotated_data

    def matches(self):
        matches = (len(self.read_down_right())
                   + len(self.read_up_right())
                   + len(self.read_down_left())
                   + len(self.read_up_left())
                   + self.read_right()
                   + self.read_left()
                   + self.read_up()
                   + self.read_down()
                   )
        return matches


    def matches_part2(self):
        # find MAS \
        #find the up\left coords from all the A coords
        up_left = [(c[0]-1, c[1]-1) for c in self.letter_coords['A']]
        #See if there is an m in any of those coords
        M_found = [x for x in up_left if x in self.letter_coords['M']]
        # See if there is an S two down and two right from those M coords
        S_coords = [(x[0]+2, x[1]+2) for x in M_found]
        S_found = [x for x in S_coords if x in self.letter_coords['S']]
        # Keep the A coords for each
        MAS_decending_A_coord = [(x[0]-1, x[1]-1) for x in S_found]

        # find MAS /
        #find the up\left coords from all the A coords
        up_right = [(c[0]-1, c[1]+1) for c in self.letter_coords['A']]
        #See if there is an m in any of those coords
        M_found = [x for x in up_right if x in self.letter_coords['M']]
        # See if there is an S two down and two left from those M coords
        S_coords = [(x[0]+2, x[1]-2) for x in M_found]
        S_found = [x for x in S_coords if x in self.letter_coords['S']]
        # Keep the A coords for each
        MAS_ascending_A_coord = [(x[0]-1, x[1]+1) for x in S_found]

        # find SAM \
        # find the up\left coords from all the A coords
        up_left = [(c[0] - 1, c[1] - 1) for c in self.letter_coords['A']]
        # See if there is an S in any of those coords
        S_found = [x for x in up_left if x in self.letter_coords['S']]
        # See if there is an M two down and two right from those S coords
        M_coords = [(x[0] + 2, x[1] + 2) for x in S_found]
        M_found = [x for x in M_coords if x in self.letter_coords['M']]
        # Keep the A coords for each
        SAM_decending_A_coord = [(x[0] - 1, x[1] - 1) for x in M_found]

        # find SAM /
        # find the up\right coords from all the A coords
        up_right = [(c[0] - 1, c[1] + 1) for c in self.letter_coords['A']]
        # See if there is an m in any of those coords
        S_found = [x for x in up_right if x in self.letter_coords['S']]
        # See if there is an S two down and two left from those M coords
        M_coords = [(x[0] + 2, x[1] - 2) for x in S_found]
        M_found = [x for x in M_coords if x in self.letter_coords['M']]
        # Keep the A coords for each
        SAM_ascending_A_coord = [(x[0] - 1, x[1] + 1) for x in M_found]

        combos = []
        # find mas\ + mas/
        combos.extend([x for x in MAS_decending_A_coord if x in MAS_ascending_A_coord])
        # find mas\ + sam/
        combos.extend([x for x in MAS_decending_A_coord if x in SAM_ascending_A_coord])
        # find sam\ + sam/
        combos.extend([x for x in SAM_decending_A_coord if x in SAM_ascending_A_coord])
        # find sam\ + mas/
        combos.extend([x for x in SAM_decending_A_coord if x in MAS_ascending_A_coord])
        return len(combos)

class day5:
    def __init__(self, filename):
        self.data = aa.read_file(filename)
        self.instructions, self.pages = self.divide_data()
        self.page_order = self.parse_instructions()
        self.solution1, self.incorrect = self.parse_page(self.pages)
        self.corrected = self.fix_incorrect()
        self.solution2, self.still_incorrect = self.parse_page(self.corrected)


    def divide_data(self):
        blank_line = self.data.index('')
        instructions = self.data[:blank_line]
        pages = self.data[blank_line+1:]
        return instructions, pages

    def parse_instructions(self):
        page_order = defaultdict(dict)
        for i in self.instructions:
            [num1, num2] = i.split("|")
            num1_after = page_order.get(num1, {}).get('after', [])
            num2_before = page_order.get(num2, {}).get('before', [])
            num1_after.append(num2)
            num2_before.append(num1)
            page_order[num1]['after'] = num1_after
            page_order[num2]['before'] = num2_before
        return page_order

    def parse_page(self, input_data):
        incorrect_orders = []
        middle_total = 0
        for pages in input_data:
            nums = pages.split(",")
            for num in nums:
                before_nums = nums[:nums.index(num)]
                after_nums = nums[nums.index(num)+1:]
                # make sure that none of the before nums are supposed to be after and visa-versa
                wrong_place = [x for x in before_nums if x in self.page_order.get(num).get('after', [])]
                wrong_place.extend([x for x in after_nums if x in self.page_order.get(num).get('before', [])])
                if len(wrong_place)>0:
                    incorrect_orders.append(nums)
                    break
            if len(wrong_place) == 0:
                assert len(nums)%2 == 1
                middle_total = middle_total + int(nums[math.floor(len(nums)/2)])
        return middle_total, incorrect_orders

    def fix_incorrect(self):
        corrected = []
        for item in self.incorrect:
            new_order = item.copy()
            for num in item:
                new_order = [x for x in new_order if x in self.page_order[num].get('before', [])] \
                            + [num] \
                                + [x for x in new_order if x in self.page_order[num].get('after', [])]
            corrected.append(",".join(new_order))
        return corrected



d5 = day5('./data/day5_2024.txt')
print(f"day 5, part 1:  {d5.solution1}")
print(f"day 5, part 1:  {d5.solution2}")
