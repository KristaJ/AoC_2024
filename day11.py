from Assets import AoCAssets as aa

class day11:

    def __init__(self, filename):
        self.data = [int(x) for x in aa.read_file(filename)[0].split(" ")]
        self.part1()

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

    def part1(self):
        input_data = self.data
        for i in range(25):
            input_data = self.blink(input_data)
            print(f'blink {i+1} - {len(input_data)}')