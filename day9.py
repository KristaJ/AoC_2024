from Assets import AoCAssets as aa

class day9:

    def __init__(self, filename):
        self.data = aa.read_file(filename)[0]
        self.dataString = self.parse_input()
        self.ordered_dataString = self.reorder_data()
        self.solution1 = self.part1()

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
            bit_to_move = new_dataString[-1]
            new_dataString = new_dataString[:-1]
            while bit_to_move == '.':
                bit_to_move = new_dataString[-1]
                new_dataString = new_dataString[:-1]
            move_location = new_dataString.index(".")
            new_dataString[move_location] = bit_to_move
        print("REORDERED")
        return new_dataString
            
    def part1(self):
        total = 0
        for i, val in enumerate(self.ordered_dataString):
            total = total + (i*int(val))
        return total
            
  

        