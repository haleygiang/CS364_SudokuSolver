import sys
import copy
import time 

"""
Class Node
"""
class Node:
    def __init__(self):
        self.val = None
        self.domain = []
        self.neighbors = []
        self.row = None
        self.col = None
        self.square_num = None

class Solution: 
    """
    Function to create node for each cell in line 
    """
    def createNode(self, sudoku):
        row = 0
        col = 0
        row_map = {}    # hashmap for rows {row: [node]}
        col_map = {}    # hashmap for cols {col: [node]}
        sq_map = {}     # hashmap for squares {(r,c): [node]}

        node_list = [] # list to store all nodes for each line

        for val in sudoku:
            node = Node()
            node.val = val

            # reset col and increment row every 9 cells
            if col == 9:
                col = 0
                row += 1
            
            # set node's row and col 
            node.row = row
            node.col = col

            # set node's square position 
            square = (row//3, col//3)
            node.square_num = square

            # add node to hashmaps
            if row in row_map:
                row_map[row].append(node)
            else:
                row_map[row] = [node]

            if col in col_map:
                col_map[col].append(node)
            else:
                col_map[col] = [node]

            if square in sq_map:
                sq_map[square].append(node)
            else:
                sq_map[square] = [node]

            # increment col every cell 
            col += 1
            
            # add node to node_list
            node_list.append(node)
        

        # add node's neighbors
        self.add_neighbors(row_map, col_map, sq_map, node_list)

        # initialize node's domain
        self.initialize_domain(node_list)

        # call ac3 and backtrack  
        self.ac3(node_list)
        result = self.backtrack(node_list)

        # print results
        self.print_result(result)


    """
    Function to add neighbors (constraints) to each node 
    """
    def add_neighbors(self, row_map, col_map, sq_map, node_list):
        for cell in node_list:
            for neighbor in row_map.get(cell.row):
                if neighbor != cell:
                    cell.neighbors.append(neighbor)
            for neighbor in col_map.get(cell.col):
                if neighbor != cell:
                    cell.neighbors.append(neighbor)
            for neighbor in sq_map.get(cell.square_num):
                if neighbor != cell:
                    cell.neighbors.append(neighbor)
            
    """
    Function to add domain (possible values) for each node 
    """
    def initialize_domain(self, node_list):
        for cell in node_list:
            if cell.val == '.':
                cell.domain = [1, 2, 3, 4, 5, 6, 7, 8, 9]
            else:
                cell.domain = [int(cell.val)]
            # print(cell.domain)

    """
    Function to implement arc consistency algorithm 
    """
    def ac3(self, node_list):
        # add all edges to queue 
        arcs = []

        for i in range(len(node_list)):
            node_i = node_list[i]
            for node_j in node_i.neighbors:
                arcs.append((node_i, node_j))
        
        # consider each constraint
        while arcs:
            (node_i, node_j) = arcs.pop(0)
            if self.revise(node_i, node_j):
                if len(node_i.domain) == 0: return False

                for node_k in node_i.neighbors:
                    arcs.append((node_k, node_i))

        return True 
    
    """
    Revise function for AC3
    """
    def revise(self, node_i, node_j):
        revised = False

        # check to see if we should remove val_i from domain of node_i
        for val_i in node_i.domain:
            satisfied = False

            for val_j in node_j.domain:
                if val_i != val_j: 
                    satisfied = True    # val_i and val_j consistent with the constraints
            
            # if val_i is not valid, remove it from domain list of node_i
            if not satisfied:           
                node_i.domain.remove(val_i)
                revised = True

        return revised
    
    """
    Function to backtrack
    """
    def backtrack(self, node_list):
        # check if assignment is complete. return node list if it is
        done = True
        min_domain = 2**32
        min_domain_node = None

        for node in node_list:
            if len(node.domain) != 1:
                done = False
            if len(node.domain) < min_domain and len(node.domain) > 1:
                min_domain = len(node.domain)
                min_domain_node = node

        if done: return node_list

        # explore min_domain_node's domain
        for val in min_domain_node.domain:
            node_list_copy = copy.deepcopy(node_list)

            # find node (aka new assignment) in node_list_copy (aka new csp)
            new_node = None
            for var in node_list_copy:
                if var.row == min_domain_node.row and var.col == min_domain_node.col:
                    new_node = var

            # update new node's val and domain                
            new_node.val = val
            new_node.domain = [val]

            # propagate constraints 
            self.ac3(node_list_copy) 

            # check domain in each node
            invalid_domain = False
            for node in node_list_copy:
                if len(node.domain) == 0:
                    invalid_domain = True

            # if no domain is empty in new csp, call backtrack
            if not invalid_domain: 
                result = self.backtrack(node_list_copy)
                if result:           
                    return result
        
        return 

    """
    Function to print out the solutions to sudokus
    """
    def print_result(self, result):
        for node in result:
            print(node.domain[0], end="")
        print()

    """
    Main function to open and read file and process each line in input file 
    """
    def main(self):
        start_time = time.time()
        try:
            # open and read file
            file = open(sys.argv[1], 'r')
            lines = file.readlines()

            # create nodes for cells 
            for line in lines:
                self.createNode(line.strip())
    
            # close file at the end of the program
            file.close() 
        except: 
            print("Invalid text file. Please put a valid text file as an argument.")
        print("Run time:", time.time() - start_time)

if __name__ == "__main__":
    Solution().main()