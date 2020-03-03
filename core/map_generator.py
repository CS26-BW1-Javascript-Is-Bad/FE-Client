import random
from os import path
import numpy as np

from core.domain.room import *
from core.util.settings import *


class DisjointSet:
    
    def __init__(self, elements):
        self._set = {}
        for element in elements:
            self._set[element] = element

    def find(self, element):
        if self._set[element] == element:
            return element
        else:
            return self.find(self._set[element])

    def union(self, element1, element2):
        _set1 = self.find(element1)
        _set2 = self.find(element2)
        self._set[_set1] = _set2
        
        
    
class Room_Generator:
    
    def __init__(self, grid_size):
        self.grid_size = grid_size
        self.rooms = np.array([[Room() for x in range(grid_size)] for y in range(grid_size)])
        self.adj_list = dict()

        for x in range(0, grid_size):
            for y in range(0, grid_size):
                node = (x, y)
                self.adj_list[node] = list() 
        
        for node in self.adj_list.keys():
            x, y = node
            neighbours = list()

            if x > 0:
                neighbours.append((x - 1, y))

            if x < grid_size - 1:
                neighbours.append((x + 1, y))

            if y > 0:
                neighbours.append((x, y - 1))

            if y < grid_size - 1:
                neighbours.append((x, y + 1))
            
            self.adj_list[node] = neighbours
            
        
        
    def get_rooms(self):
        return self.rooms
        
    def set_rooms(self):
        counter = 0
        for i in self.spanning_tree_using_kruskal():
            x1 = i[0][0]
            y1 = i[0][1]
            x2 = i[1][0]
            y2 = i[1][1]
            room1 = self.rooms[x1][y1]
            room2 = self.rooms[x2][y2]
            
            if x1 == x2:
                if y1 < y2:
                    room1.e_to = room2
                    room2.w_to = room1
                else:
                    room1.w_to = room2
                    room2.e_to = room1
            elif x1 < x2:
                room1.s_to = room2
                room2.n_to = room1
            else:
                room1.n_to = room2
                room2.s_to = room1
                self.asset = ""
                
        flat_rooms = self.rooms.flatten()
        for i in flat_rooms:
            if i.n_to is not None:
                i.asset += "n"
            if i.s_to is not None:
                i.asset += "s"
            if i.e_to is not None:
                i.asset += "e"
            if i.w_to is not None:
                i.asset += "w"
            i.asset += "_1.tmx"
        
            i.asset = path.join(tilemap_folder, i.asset)
        return flat_rooms
            

 
    def spanning_tree_using_kruskal(self):
        tree_edges = list()
        graph_edges = list()

        for node in self.adj_list.keys():
            neighbours = self.adj_list[node]
            for neighbour in neighbours:
                if ((node, neighbour) not in graph_edges and
                    (neighbour, node) not in graph_edges):
                    graph_edges.append((node, neighbour))        
        
        disjoint_set = DisjointSet(self.adj_list.keys())
        
        while (len(tree_edges) < (len(self.adj_list.keys()) - 1)):
            rnd_edge = random.choice(graph_edges)
            node1, node2 = rnd_edge
            set1 = disjoint_set.find(node1)
            set2 = disjoint_set.find(node2)
            
            if (set1 != set2):
                disjoint_set.union(node1, node2)
                tree_edges.append(rnd_edge)

            graph_edges.remove(rnd_edge)

        return tree_edges
   