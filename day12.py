from Assets import AoCAssets as ac
import numpy as np
import networkx as nx
import pandas as pd

class day12:
    def __init__(self, filename):
        self.data = ac.read_matrix(filename)
        self.plots = self.find_plots()
        self.solution1 = self.part1()
        


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
        G = nx.from_pandas_edgelist(edges)
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
        for plot in self.plots:
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
        return total
            