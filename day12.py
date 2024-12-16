from Assets import AoCAssets as ac
import numpy as np
import networkx as nx
import pandas as pd
from collections import Counter

class day12:
    def __init__(self, filename):
        self.data = ac.read_matrix(filename)
        self.plots = self.find_plots()
        self.solution1, self.all_edges = self.part1()
        self.solution2 = self.part2()
        


    def find_plots(self):
        crops = np.unique(self.data)
        edges = pd.DataFrame(columns = ['source', 'target', 'crop'])
        total_locs = 0
        for crop in crops:
            x,y = np.where(self.data == crop)
            locs = list(zip(x,y))
            for loc in locs:
                adjacent = self.check_all_directions(loc, crop)
                if len(adjacent) == 0:
                    crop_frame = [[loc, loc, crop]]
                else:
                    crop_frame = [[loc, a, crop] for a in adjacent]
                edges = pd.concat([pd.DataFrame(crop_frame, columns = ['target', 'source', 'crop']),
                                  edges], ignore_index=True)
        G = nx.from_pandas_edgelist(edges, edge_attr = True)
        plots = [G.subgraph(x) for x in nx.connected_components(G)]
        return plots

    def check_all_directions(self, p, p_value):
        moves = []
        try:
            if self.data[p[0], p[1]+1] == p_value:
                moves.append((p[0], p[1]+1))
        except IndexError:
            pass
        try:
            if (p[1]-1 > -1) and (self.data[p[0], p[1]-1] == p_value):
                moves.append((p[0], p[1]-1))
        except IndexError:
            pass
        try:
            if self.data[p[0]+1, p[1]] == p_value:
                moves.append((p[0]+1, p[1]))
        except IndexError:
            pass
        try:
            if (p[0]-1 > -1) and self.data[p[0]-1, p[1]] == p_value:
                moves.append((p[0]-1, p[1]))
        except IndexError:
            pass
        return moves

    def part1(self):
        total = 0
        all_edges = []
        for plot in self.plots:
            crop = next(iter(plot.edges(data=True)))[2].get('crop')
            pts = plot.nodes()
            edges = []
            for p in sorted(pts):
                moves = [(p[0], p[1]+1), 
                         (p[0], p[1]-1), 
                         (p[0]+1, p[1]),
                         (p[0]-1, p[1])]
                edges.extend([x for x in moves if x not in pts])
            plot_cost = len(pts) * len(edges)
            total = total + plot_cost

            all_edges.append((crop, edges, len(pts)))
        return total, all_edges

    def part2(self):
        total = 0
        for plot in self.plots:
            right_edges = []
            left_edges = []
            top_edges = []
            bottom_edges = []
            edges = [right_edges, left_edges, top_edges, bottom_edges]
            crop = next(iter(plot.edges(data=True)))[2].get('crop')
            pts = plot.nodes()
            for p in pts:
                moves = [(p[0], p[1]+1),  #right
                         (p[0], p[1]-1),  #left
                         (p[0]+1, p[1]),  #up
                         (p[0]-1, p[1])]  #down
                for i in range(4):
                    if self.get_crop(moves[i]) != crop:
                        edges[i].append(p)
            
            num_sides_total = 0
            ys = list(set([x[1] for x in right_edges]))
            for y in ys:
                e = sorted([x[0] for x in right_edges if x[1] == y])
                num_sides = self.is_consec(e)
                num_sides_total += num_sides
            ys = list(set([x[1] for x in left_edges]))
            for y in ys:
                e = sorted([x[0] for x in left_edges if x[1] == y])
                num_sides = self.is_consec(e)
                num_sides_total += num_sides
            ys = list(set([x[0] for x in top_edges]))
            for y in ys:
                e = sorted([x[1] for x in top_edges if x[0] == y])
                num_sides = self.is_consec(e)
                num_sides_total += num_sides
            ys = list(set([x[0] for x in bottom_edges]))
            for y in ys:
                e = sorted([x[1] for x in bottom_edges if x[0] == y])
                num_sides = self.is_consec(e)
                num_sides_total += num_sides
            total += (num_sides_total * len(pts))
        return (total)
        
                
    def is_consec(self, points):
        num_consec = 1
        p0 = points.pop()
        while points:
            p1 = points.pop()
            if p0 == p1+1:
                pass
            else:
                num_consec = num_consec+1
            p0 = p1
        return num_consec
                

    def get_crop(self, point):
        try:
            return self.data[point]
        except IndexError:
            return " "
        
   

    def get_crop(self, point):
        if (point[0] < 0) or (point[1]<0):
            return None
        try:
            return self.data[point]
        except IndexError:
            return None

                     


