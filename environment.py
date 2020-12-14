from recordtype import recordtype
import random
import numpy as np
import time

class Environment:

    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.boxes = []

        self.pos = recordtype('pos', 'rownum colnum')

        for i in range(rows):
            row_box = []
            for j in range(cols):
                row_box.append(self.pos(i, j))
            self.boxes.append(row_box)

        self.current_pos = self.pos(random.randint(0, self.rows - 1), random.randint(0, self.cols - 1))

        self.food = self.pos(random.randint(0, self.rows - 1), random.randint(0, self.cols - 1))

    def render(self, reward=None):
        if reward != None:
            print("-" * self.rows)
            print(f"Reward: {reward}")
            print("-" * self.rows)
        for i in range(self.rows):
            for j in range(self.cols):
                if self.boxes[i][j] == self.current_pos:
                    print("\033[94mX\033[m", end=" ")
                elif self.boxes[i][j] == self.food:
                    print("\033[91mF\033[m", end=" ")
                else:
                    print("O", end=" ")
            print()
        print()

    def compute_abs_xy_distance(self, rownum=None, colnum=None):
        if rownum == None and colnum == None:
            return -(abs(self.food.rownum - self.current_pos.rownum) + (abs(self.food.colnum - self.current_pos.colnum)))

        return -(abs(self.food.rownum - rownum) + (abs(self.food.colnum - colnum)))

    def move_up(self):
        if self.current_pos.rownum > 0:
            self.current_pos.rownum -= 1
        return int(self.current_pos == self.food)

    def move_down(self):
        if self.current_pos.rownum < self.rows - 1:
            self.current_pos.rownum += 1
        return int(self.current_pos == self.food)

    def move_left(self):
        if self.current_pos.colnum > 0:
            self.current_pos.colnum -= 1
        return int(self.current_pos == self.food)
    
    def move_right(self):
        if self.current_pos.colnum < self.cols - 1:
            self.current_pos.colnum += 1
        return int(self.current_pos == self.food)

    def is_possible_location(self, rownum, colnum):
        return (rownum >= 0 and rownum < self.rows) and (colnum >= 0 and colnum < self.cols)

    def get_state(self):
        states = []
        direction_movement = [[1, 0], [-1, 0], [0, 1], [0, -1], [1, 1], [1, -1], [-1, 1], [-1, -1]]

        for i in range(8):
            new_pos = self.pos(self.current_pos.rownum + direction_movement[i][0], 
                               self.current_pos.colnum + direction_movement[i][1])

            # if self.is_possible_location(new_pos.rownum, new_pos.colnum) and new_pos == self.food:
            #     states.append(1)
            # else:
            #     states.append(0)

            states.append(self.compute_abs_xy_distance(new_pos.rownum, new_pos.colnum))

        # states.append(self.compute_abs_xy_distance())

        return np.array(states)

    def is_done(self):
        if self.current_pos == self.food:
            return True
        return False
