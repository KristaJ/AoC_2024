from Assets import AoCAssets as ac
import numpy as np




class day15:
    def __init__(self, filename):
        self.data = ac.read_file(filename)
        self.grid, self.instructions = self.parse_data()
        self.starting_point = self.get_starting_point()
        self.mm = self.move_map()
        # self.move()
        # self.solution1 = self.part1()
        self.solution2 = self.part2()

    def parse_data(self):
        grid = []
        instructions = []
        for l in self.data:
            if l.startswith("#"):
                grid.append([x for x in l])
            elif l.startswith("<") or l.startswith(">") or l.startswith("^") or l.startswith("v"):
                instructions.append(l)
        instructions = "".join(instructions)
        return np.array(grid), instructions

    def move_map(self):
        return {'<': [0, -1], '>':[0, 1], '^': [-1, 0], 'v': [1, 0]}
    
    def get_starting_point(self):
        start = np.where(self.grid == "@")
        return(start[0].item(), start[1].item())
        
    def move(self):
        current_loc = self.starting_point
        self.grid[current_loc] = "."
        #1.  check to see if you can move the block
        #2.  If you can't pass
        #3.  If you can move the block(s) and update the grid
            #3a.  update the current loc
        for move in self.instructions:
            delta = self.mm[move]
            y = current_loc[0]+delta[0]
            x = current_loc[1]+delta[1]
            next_block = self.grid[y][x]
            
            if next_block == '#':
                pass
            elif next_block == '.':
                current_loc = (y,x)
            elif next_block == "O":
                is_movable, final_block_loc = self.movable_block((y,x), move)
                if is_movable:
                    current_loc = (y,x)
                    self.do_block_moving(current_loc, final_block_loc)  
        self.grid[current_loc] = "@"

    def movable_block(self, next_block_loc, direction):
        next_block = self.grid[next_block_loc]
        i = 0
        while (next_block == "O") and (i < 10): #if the block on the other side of the O 
            i = i +1                   #is another O we need to keep checking
            d = self.mm[direction]
            y = next_block_loc[0] + d[0]
            x = next_block_loc[1] + d[1]
            next_block = self.grid[y][x]
            next_block_loc = (y,x)
        if next_block == ".":
            return True, next_block_loc
        elif next_block == "#":
            return False, 0
        elif i >=10:
            print("LOOP AVERTED")
        else:
            print("unexpected symbol")

    def do_block_moving(self, current_loc, final_block_loc):
        #current loc becomes . and final loc become O
        self.grid[current_loc] = "."
        self.grid[final_block_loc] = "O"

    def part1(self):
        box_locations = np.where(self.grid == "O")
        scores = [box_locations[0][i] * 100 + box_locations[1][i] for i in range(len(box_locations[0]))]
        return (sum(scores))
    
    def part2(self):
        self.new_grid = self.rescale_grid()

    def rescale_grid(self):
        new_grid = []
        for l in self.data:
            if l.startswith("#"):
                new_line = ""
                for char in l:
                    if char == "#":
                        new_line += "##"
                    if char == '.':
                        new_line += ".."
                    if char == "O":
                        new_line += "[]"
                    if char == "@":
                        new_line += "@."
            new_grid.append([x for x in new_line])
        new_grid = np.array(new_grid)
        return new_grid

        