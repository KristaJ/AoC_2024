from Assets import AoCAssets as ac
import numpy as np
import math
from PIL import Image
import imageio
import matplotlib.pyplot as plt



class day14:
    def __init__(self, filename):
        self.data = ac.read_file(filename)
        self.robot_data = self.parse_data()
        self.grid_dims = [101, 103] # x, y
        # self.grid_dims = [11,7]
        self.final_positions = self.move_robots()
        self.quads = self.get_quads()
        self.solution1 = self.part1()
        self.find_line()
        # self.plot_robots()

    def parse_data(self):
        robot_data = []
        for line in self.data:
            p,v = line.split(' ')
            position = p.split("=")[-1].split(",")
            velocity = v.split("=")[-1].split(",")
            robot_data.append(((int(position[0]), int(position[1])),
                               (int(velocity[0]), int(velocity[1]))
                              ))
        return(robot_data)

    def move_robots(self, num_sec: int = 100):
        final_positions = []
        for robot in self.robot_data:
            initial_pos = robot[0]
            movement = robot[1]
            final_pos_x = (initial_pos[0] + (num_sec * movement[0]))%self.grid_dims[0]
            final_pos_y = (initial_pos[1] + (num_sec * movement[1]))%self.grid_dims[1]
            final_positions.append((final_pos_x, final_pos_y))
        return final_positions

    def get_quads(self):
        mid_y = self.grid_dims[1]//2
        mid_x = self.grid_dims[0]//2
        q1 = []
        for i in  range(0, mid_x):
            for j in range(0, mid_y):
                q1.append((i,j)) # upper-left
        q2 = [(c[0] + mid_x+1, c[1]) for c in q1] #lower-left
        q3 = [(c[0], c[1]+mid_y+1) for c in q1] #upper-right
        q4 = [(c[0] + mid_x+1, c[1]+mid_y+1) for c in q1] #lower-right
        return [q1, q2, q3, q4]
    
    def part1(self):
        q1_total = 0
        q2_total = 0
        q3_total = 0
        q4_total = 0
        quad_totals = [q1_total, q2_total, q3_total, q4_total]
        for fp in self.final_positions:
            for i, quad in enumerate(self.quads):
                if fp in quad:
                    quad_totals[i] += 1
        return math.prod(quad_totals)
        
    def part2(self):
        pass

    def plot_robots(self, elapsed_time):
        grid = np.zeros((self.grid_dims[1], self.grid_dims[0]))
        pos = self.move_robots(elapsed_time)
        for p in pos: 
            grid[p[1], p[0]] = 1
        plt.imsave(f'./day14_{elapsed_time}.png', grid, cmap='gray') 

    def find_line(self):
        potential = []
        for i in range(4000, 7000):
            if i%100 == 0:
                print(f'elapsed time: {i}')
            pos = self.move_robots(i)
            vert_vals = list(set([x[0] for x in pos if x[0] > 50]))
            # if we are looking for the verrtical bottom of the tree 
            # it's probably more than half way down
            for y in vert_vals:
                consec = 0
                pts = sorted([x for x in pos if x[0] == y])
                pt = pts.pop()
                while pts:
                    if pt[1] == pts[-1][1]+1:
                        consec = consec +1
                    else:
                        consec = 0
                    pt = pts.pop()
                if consec > 5:
                    print(f"====={i}=====")
                    print(sorted([x for x in pos if x[0] == y]))
                    
                
        
 


