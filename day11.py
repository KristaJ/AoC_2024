from Assets import AoCAssets as aa
from collections import Counter

class day11:

    def __init__(self, filename):
        self.data = [int(x) for x in aa.read_file(filename)[0].split(" ")]
        self.solution1 = self.part2(25)
        self.solution2 = self.part2(75)

    def blink(self, input_data):
        temp_data = input_data.copy()
        for i, stone in enumerate(input_data):
            current_stone_index_temp = temp_data.index(stone)
            if stone == 0: #change the value to 1
                temp_data[current_stone_index_temp] = 1
            elif len(str(stone))%2 == 0: #split into two stones
                stone1 = int(str(stone)[:len(str(stone))//2])
                stone2 = int(str(stone)[len(str(stone))//2:])
                # replace current stone with stone 1
                temp_data[current_stone_index_temp ] = stone1
                # insert stone 2 after the stone just changed
                temp_data.insert(current_stone_index_temp +1, stone2)
            else:
                temp_data[current_stone_index_temp ] = stone*2024 
        return temp_data

    def part1(self, blinks):
        input_data = self.data
        for i in range(blinks):
            print(i)
            input_data = self.blink(input_data)
        print(f'blink {i+1} - {len(input_data)}')
        return len(input_data)

    def part2(self, blinks):
        # we are going to need to be smarter here since I don't have a quantum computer 
        # we are doing the same calculations a lot, so maybe try to only do calcs for each number once
        input_data = self.data
        input_counter = Counter(input_data)
        # print(input_counter)
        for i in range(blinks):
            temp_counter = {}
            for k, v in input_counter.items():
                new_nums = self.blink([k])
                new_counter = Counter(new_nums)
                for k_new, v_new in new_counter.items():
                    # currently there are {v_new} copies of {k_new} in the new num list
                    # I want to calculate the numer of times that num appears in new_counter 
                    # times the number of times the original number occured in the 
                    # input counter
                    k_new_total_count = v_new * v
                    # Now I want to check how many times I've seen this number already during this blink
                    k_new_previous_count = temp_counter.get(k_new, 0)
                    # add the new count to the previous count
                    temp_counter[k_new] = k_new_total_count + k_new_previous_count
            #once the whole blink is calculated we can reassign the temp_counter
            # to the input counter
            input_counter = temp_counter
        # print(f'blink {i+1} - {input_counter}')
        return sum(input_counter.values())
        
        