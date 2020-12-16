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

    def compute_xy_distance_to_food(self, rownum, colnum):
        return abs(rownum - self.food.rownum) + abs(colnum - self.food.colnum)

    def get_state(self):
        states = []
        direction_movement = [[0, 1], [1, 0], [0, -1], [-1, 0], [1, 1], [1, -1], [-1, 1], [-1, -1]]

        for direction in direction_movement:
            newpos = self.pos(self.current_pos.rownum + direction[0], self.current_pos.colnum + direction[1])

            states.append(self.compute_xy_distance_to_food(newpos.rownum, newpos.colnum))

        return np.array(states)

    def is_done(self):
        if self.current_pos == self.food:
            return True
        return False


if __name__ == "__main__":
    env = Environment(16, 16, 10)
    env.current_pos = env.pos(0, 0)
    env.food = env.pos(8, 0)

    print(env.get_state())