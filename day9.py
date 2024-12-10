from Assets import AoCAssets as aa

class day9:

    def __init__(self, filename):
        self.data = aa.read_file(filename)[0]
        self.dataString = self.parse_input()
        self.ordered_dataString = self.reorder_data()
        self.solution1 = self.part1()
        self.dataString2 = self.parse_input2()
        self.ordered_dataString2 = self.reorder_data2()
        self.solution2 = self.part2()

    def parse_input(self):
        filesizes = [x for x in self.data[::2]]
        # need to add a zero at the end to get the zip right
        freespace = [x for x in self.data[1::2]] + [0]
        ids = [i for i in range(len(filesizes))]
        dataString = []
        for a, b, idn in list(zip(filesizes, freespace, ids)):
            dataString = dataString + [str(idn)] * int(a) + ["."] * int(b)
        return dataString

    def reorder_data(self):
        new_dataString = self.dataString
        while '.' in new_dataString:
        # while new_dataString.find(".") > -1:
            bit_to_move = new_dataString.pop()
            while bit_to_move == '.':
                bit_to_move = new_dataString.pop()
            move_location = new_dataString.index(".")
            new_dataString[move_location] = bit_to_move
        print("REORDERED")
        return new_dataString
        
            
    def part1(self):
        total = 0
        for i, val in enumerate(self.ordered_dataString):
            total = total + (i*int(val))
        return total

    def parse_input2(self):
        filesizes = [x for x in self.data[::2]]
        # need to add a zero at the end to get the zip right
        freespace = [x for x in self.data[1::2]] + [0]
        ids = [i for i in range(len(filesizes))]
        dataString = []
        for a, b, idn in list(zip(filesizes, freespace, ids)):
            dataString = dataString + [(a, idn), (b, '.')]
        return dataString

    def reorder_data2(self):
        new_dataString = self.dataString2
        ds = [str(x[1]) * int(x[0]) for x in new_dataString] 
        for i in range(len(new_dataString)-1, -1, -1):
            l = new_dataString[i]
            if l[1] != ".":
                # Find the first place this chunk can fit
                place = next((x for x in new_dataString if (int(x[0]) >= int(l[0])) and x[1] == '.'), False)
                    # if we find a place
                if place:
                    # fine the index of that place
                    place_index = new_dataString.index(place)
                    if place_index < i: #We only want to move bits to the left
                    #determine what's going into that index location
                    # If the number of empty spots is equal to the number of bits we can just swap them
                        if place[0] == l[0]:
                            new_dataString[i] = place
                            new_dataString[place_index] = l
                            ds = [str(x[1]) * int(x[0]) for x in new_dataString]
                        #if not we need to split the empty space into what is going 
                        # to be swapped and what is going to remain
                        else:
                            split_freespace_remaining = (str(int(place[0]) - int(l[0])), '.')
                            split_freespace_to_move = (l[0], '.')
                            
                            # swap the freespace to move and the bits
                            new_dataString[i] = split_freespace_to_move
                            new_dataString[place_index] = l
                            # then insert the freespace remaining after the bits you just moved
                            new_dataString.insert(place_index+1, split_freespace_remaining)
        ordered_string = [[x[1]] * int(x[0]) for x in new_dataString]
        return [x for xs in ordered_string for x in xs]
    
    def part2(self):
        total = 0
        for i, val in enumerate(self.ordered_dataString2):
            if val != ".":
                total = total + i*val
        return total



        