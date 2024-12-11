from Assets import AoCAssets as aa
import numpy as np

class day10:

    def __init__(self, filename):
        self.data = aa.read_matrix(filename)
        self.data = self.data.astype(int)
        self.starting_points = self.find_starting_points()
        self.paths= self.find_paths()
        self.solution1 = self.part1()
        self.solution2 = len(self.paths)


    def find_starting_points(self):
        start = np.where(self.data == 0)
        return list(zip(start[0], start[1]))
        
        

    def check_all_directions(self, p, p_value):
        moves = []
        try:
            if self.data[p[0], p[1]+1] == p_value +1:
                moves.append((p[0], p[1]+1))
        except IndexError:
            pass
        try:
            if (p[1]-1 > -1) and (self.data[p[0], p[1]-1] == p_value +1):
                moves.append((p[0], p[1]-1))
        except IndexError:
            pass
        try:
            if self.data[p[0]+1, p[1]] == p_value +1:
                moves.append((p[0]+1, p[1]))
        except IndexError:
            pass
        try:
            if (p[0]-1 > -1) and self.data[p[0]-1, p[1]] == p_value +1:
                moves.append((p[0]-1, p[1]))
        except IndexError:
            pass
        return moves
    
    def find_paths(self):
        paths = [[x] for x in self.starting_points]
        complete_paths = []
        while paths:
            path = paths.pop()
            current_point = path[-1]
            current_elevation = self.data[current_point]
            if current_elevation == 9:
                complete_paths.append(path)
            else:
                moves = self.check_all_directions(current_point, current_elevation)
                for move in moves:
                    paths.append(path + [move])
        return complete_paths
    
    def part1(self):
        start_end = [(x[0], x[-1]) for x in self.paths]
        return len(list(set(start_end)))

                
            
                