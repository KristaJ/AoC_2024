from Assets import AoCAssets as aa
from collections import Counter
import re
import numpy as np
from collections import defaultdict
import math
import itertools


class day1:

    def __init__(self, filename):
        self.solution1 = self.day1_a
        self.solution2 = self.day1_b

    def day1_a(self):
        data = aa.read_file(filename)
        row1 = [int(x.split('  ')[0]) for x in self.data]
        row2 = [int(x.split('  ')[1]) for x in self.data]
        row1 = sorted(row1)
        row2 = sorted(row2)
        diff = [abs(r1-r2) for r1,r2 in zip(row1, row2)]
        return sum(diff)

    def day1_b(self):
        total = 0
        left_row = Counter([int(x.split('  ')[0]) for x in self.data])
        right_row = Counter([int(x.split('  ')[1]) for x in self.data])
        for k, v in left_row.items():
            total = (right_row.get(k, 0) * k * v) + total
        return total

class day2:
    def __init__(self, filename):
        self.data = aa.read_file(filename)
        self.solution1 = self.day2_a()
        self.solution2 = self.day2_b()
    
    def day2_a(self):
        safe = 0
        for d in self.data:
            x = d.split()
            x = [int(z) for z in x]
            if self.monotonic(x) and self.inRange(x):
                safe = safe +1
        return safe
    
    def day2_b(self):
        safe = 0
        for d in self.data:
            x = d.split()
            x = [int(z) for z in x]
            if self.monotonic(x) and self.inRange(x):
                safe = safe + 1
            else:
                for i in range(len(x)):
                    x_temp = x[:i] + x[i+1:]
                    if self.monotonic(x_temp) and self.inRange(x_temp):
                        safe = safe + 1
                        break
        return safe
    
    def inRange(self, x):
        diffs = [int(x[i - 1]) - int(x[i]) for i in range(1, len(x))]
        if any([abs(x) < 1 for x in diffs]) or any([abs(x) > 3 for x in diffs]):
            return False
        else:
            return True
    
    def monotonic(self, x):
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

class day6:
    def __init__(self, filename):
        self.data = aa.read_file(filename)
        self.data = self.data_to_matrix()
        self.start_point, self.starting_direction =self.find_starting_point()
        self.obstacles = self.find_obstacle()
        self.current_location, self.current_direction = self.start_point, self.starting_direction
        self.new_direction_map = self.new_direction_map()
        self.coords_traversed, self.movement_dir = self.move()
        self.solution1 = len(list(set(self.coords_traversed)))
        self.potential_obstacles = []
        self.part2()
        self.solution2 = len(list(set(self.potential_obstacles)))

    def data_to_matrix(self):
        '''
        transform the data into a matrix for easier traversal
        '''
        data = [[x for x in data_line] for data_line in self.data]
        matrix = np.array(data)
        return matrix

    def find_starting_point(self):
        '''
        Find the starting point and the starting direction
        :return:
        '''
        for char in ['^', '<', '>', 'v']:
            if np.where(self.data == char)[0].size > 0:
                return((np.where(self.data == char)[0].tolist()[0],
                        np.where(self.data == char)[1].tolist()[0]), char)

    def find_obstacle(self):
        '''
        create a list of th coordinates of all obstacles
        :return:
        '''
        return(list(zip(np.where(self.data == "#")[0].tolist(),
                        np.where(self.data == "#")[1].tolist())))

    def move_up(self):
        return [(self.current_location[0]-i,
                 self.current_location[1]) for i in range(self.current_location[0]+1)]

    def move_down(self):
        return [(self.current_location[0]+i,
                 self.current_location[1]) for i in range((self.data.shape[0]-1) - self.current_location[0]+1)]

    def move_right(self):
        return [(self.current_location[0],
                 self.current_location[1]+i) for i in range((self.data.shape[1]-1) - self.current_location[1]+1)]

    def move_left(self):
        return [(self.current_location[0],
                 self.current_location[1]-i) for i in range(self.current_location[1]+1)]

    def new_direction_map(self):
        return  ({'^': '>',
                 '>': 'v',
                 'v': '<',
                 '<': '^'})

    def move(self):
        on_map = True
        coords_traversed = []
        movement_dir = []
        while on_map:
            if self.current_direction == "^":
                potential_path = self.move_up()
            elif self.current_direction == ">":
                potential_path = self.move_right()
            elif self.current_direction == "<":
                potential_path = self.move_left()
            elif self.current_direction == "v":
                potential_path = self.move_down()
            stop = [x for x in potential_path if x in self.obstacles]
            if len(stop)>0:
                actual_path = potential_path[: potential_path.index(stop[0])]
                coords_traversed.extend(actual_path)
                movement_dir.extend([self.current_direction] * len(actual_path))
                self.current_location = actual_path[-1]
                self.current_direction = self.new_direction_map[self.current_direction]
            else:
                coords_traversed.extend(potential_path)
                movement_dir.extend([self.current_direction] * len(potential_path))
                on_map = False

        return coords_traversed, movement_dir

    def get_path(self, location, direction):
        if direction == "^":
            path = [(location[0]-i,
                     location[1]) for i in range(location[0]+1)]
        elif direction == "v":
            path = [(location[0]+i,
                     location[1]) for i in range(self.data.shape[0] - location[0])]
        elif direction == ">":
            path = [(location[0], 
                     location[1]+i) for i in range((self.data.shape[1]-location[1]))]
        elif direction == "<":
            path = [(location[0], 
                     location[1]-i) for i in range(location[1]+1)]
        return path

    def output_matrix(self, final_path, temp_obstacles):
        temp_matrix = self.data.copy()
        temp_matrix[temp_obstacles[-1][0], temp_obstacles[-1][1]] = "O"
        # print(final_path)
        for x in final_path[1:]:
            current_symbol = temp_matrix[x[0][0], x[0][1]]
            if current_symbol == "#":
                print("ERROR")
            if temp_matrix[x[0][0], x[0][1]] == x[1]:
                temp_matrix[x[0][0], x[0][1]] = "*"
            elif current_symbol  == "*" or current_symbol  == "X":
                temp_matrix[x[0][0], x[0][1]] = "X"
                # print('repeat')
            else:
                temp_matrix[x[0][0], x[0][1]] = x[1]
        np.savetxt(f'matrix_{temp_obstacles[-1]}.txt', temp_matrix, delimiter = '', fmt='%s')
    
    def move_from_test_location(self, test_location, test_direction, temp_obstacles):
        on_map = True
        final_path = []
        turn_locations = []
        # print("=======")
        # print(test_location, test_direction)
        while on_map:
            potential_path = self.get_path(test_location, test_direction)
            stop = [x for x in potential_path if x in temp_obstacles]
            if len(stop) > 0:
                actual_path = potential_path[: potential_path.index(stop[0])]
                actual_path = [(x, test_direction) for x in actual_path]
                final_path.extend(actual_path)
                turn_locations.append((actual_path[-1], test_direction))
                test_location = actual_path[-1][0]
                test_direction = self.new_direction_map[test_direction]
                try:
                    turnIndex = turn_locations[:-1].index(turn_locations[-1])
                except ValueError:
                    pass
                if turn_locations[-1] in turn_locations[:-1]:
                    self.potential_obstacles.append(temp_obstacles[-1])  
                    return 0
            else:
                # print("OUT")
                on_map = False
                
    def part2(self):
        self.loops = 0
        # As the guard walks, is there anywhere she would run into a obsacle is she turned right?
        locations = list(zip(self.coords_traversed, self.movement_dir))
        ll = 0
        # for each location and direction combo, see if there is a obstacle to the right
        for loc, direction in locations:
            #for each place the guard has been, if we place an obsticle in front of her will
            # she enter a loop
            ll = ll+1
            if ll%500 == 0: 
                print(ll)
            if direction == '^':
                new_obstacle = (loc[0]-1, loc[1])
            if direction == 'v':
                new_obstacle = (loc[0]+1, loc[1])
            if direction == '>':
                new_obstacle = (loc[0], loc[1]+1)
            if direction == '<':
                new_obstacle = (loc[0], loc[1]-1)
            temp_obstacles = self.obstacles + [new_obstacle]
            # Place the new obstacle and THEN start moving!!!!!!!
            # Don't start moving from the location of the obstacle.
            self.move_from_test_location(self.start_point, self.starting_direction, temp_obstacles)

class day7:
    def __init__(self, filename):
        self.data = aa.read_file(filename)
        self.solution1 = self.part1()
        self.solution2 = self.part2()

    def parse_input(self, line):
        target_value = int(line.split(':')[0])
        numbers = line.split(':')[1].split(' ')[1:]
        numbers = [int(x) for x in numbers]
        return numbers, target_value


    def part1(self):
        total = 0
        for line in self.data:
            self.nums, self.target = self.parse_input(line)
            total = total + self.brute_force()
        return total

    def part2(self):
        total = 0
        for line in self.data:
            self.nums, self.target = self.parse_input(line)
            total = total + self.brute_force(concat = True)
        return total
            
    def brute_force(self, concat:bool = False):
        temp_nums = self.nums.copy()
        equations = [(self.nums[0], self.nums[1:])]
        while len(equations) > 0:
            cur_equation = equations.pop()
            cur_sol = cur_equation[0]
            nums = cur_equation[1]

            added = cur_sol + nums[0]
            mult = cur_sol * nums[0]
            if concat:
                concated = int(str(cur_sol)+str(nums[0]))

            # if this is that last number in the list of numbers
            if len(nums) == 1:
                if (added == self.target or mult == self.target):
                    return self.target
                elif concat:
                    if concated == self.target:
                        return self.target
                else:
                    continue
                    
            #if we still have numbers to go
            #if added is still less than the target
            if len(nums) > 1:
                if added <= self.target:
                    equations.append((added, nums[1:]))
                if mult <= self.target:
                    equations.append((mult, nums[1:]))
                if concat:
                    if concated <= self.target:
                        equations.append((concated, nums[1:]))
                
        return 0
 
class day8:
    def __init__(self, filename):
        self.data = aa.read_file(filename)
        self.data_matrix = self.data_to_matrix() 
        self.y_dim, self.x_dim = self.data_matrix.shape
        self.anti_node_matrix = np.full(self.data_matrix.shape, '.')
        self.unique_antenna = self.get_unique_antenna()
        self.antenna_map = self.map_antennas()
        self.solution1 = self.part1()
        self.solution2 = self.part2()

    def data_to_matrix(self):
        data = [[x for x in data_line] for data_line in self.data]
        matrix = np.array(data)
        return matrix

    def get_unique_antenna(self):
        return [x for x in np.unique(self.data_matrix) if x != '.']

    def map_antennas(self):
        ant_map = {}
        for a in self.unique_antenna:
            ant_map[a] = list(zip(np.where(self.data_matrix == a)[0],
                                  np.where(self.data_matrix == a)[1]))
        return ant_map

    def part1(self):
        '''
        0.  Identify all pairs of matching nodes
        1.  find the delta x and delta y between the pair
        2.  place an anti node at an additiona delta x and delta y each node
        '''
        for k, v in self.antenna_map.items():
            nn = 0
            pairs = list(itertools.combinations(v, 2))
            for p in pairs:
                dy = p[0][0]-p[1][0]
                dx = p[0][1]-p[1][1]
                new_antinode1 = ((p[1][0] - dy), (p[1][1] - dx))
                new_antinode2 = ((p[0][0] + dy), (p[0][1] + dx))
                if (new_antinode1[0] > -1) and (new_antinode1[1] > -1):
                    try:
                        self.anti_node_matrix[new_antinode1[0], new_antinode1[1]] = "X"
                        # print(f'{new_antinode1} = {nn}')
                        # nn = nn+1
                    except IndexError:
                        pass
                if (new_antinode2[0] > -1) and (new_antinode2[1] > -1):
                    try:
                        self.anti_node_matrix[new_antinode2[0], new_antinode2[1]] = "X"
                        # print(f'{new_antinode2} = {nn}')
                        # nn = nn+1
                    except IndexError:
                        pass
        # print(self.anti_node_matrix)
        return np.count_nonzero(self.anti_node_matrix == "X")
 
    def part2(self):
        '''
        0.  Identify all pairs of matching nodes
        1.  find the delta x and delta y between the pair
        2.  place an anti node at an additional delta x and delta y each node
        3.  Keep placing antinodes until either the new x or new y is out of range
        '''
        for k, v in self.antenna_map.items():
            nn = 0
            pairs = list(itertools.combinations(v, 2))
            for p in pairs:
                dy = p[0][0]-p[1][0]
                dx = p[0][1]-p[1][1]
                new_y1 = p[1][0]
                new_x1 = p[1][1]
                new_antinodes1 = []
                while (new_y1 < self.y_dim and
                       new_y1 > -1 and
                       new_x1 < self.x_dim and
                       new_x1 > -1):
                    new_antinodes1.append((new_y1, new_x1))
                    new_y1 = new_y1 - dy
                    new_x1 = new_x1 - dx
                new_y2 = p[1][0]
                new_x2 = p[1][1]
                new_antinodes2 = []
                while (new_y2 < self.y_dim and
                       new_y2 > -1 and
                       new_x2 < self.x_dim and
                       new_x2 > -1):
                    new_antinodes2.append((new_y2, new_x2))
                    new_y2 = new_y2 + dy
                    new_x2 = new_x2 + dx

                for node in new_antinodes1 + new_antinodes2:
                    self.anti_node_matrix[node[0], node[1]] = "X"

        # print(self.anti_node_matrix)
        return np.count_nonzero(self.anti_node_matrix == "X")                


class day9:

    def __init__(self, filename):
        self.data = aa.read_file(filename)
        self.parse_input()

    def parse_input(self):
        filesizes = self.data[::2]
        freespace = self.data[1:2]
        ids = [i for i in range(filesizes)]
        print(filesizes, freespace, ids)
        
                    
                    
    