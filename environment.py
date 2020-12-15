from recordtype import recordtype
import random
import numpy as np
import time

class Environment:

    def __init__(self, rows, cols, scope):
        self.rows = rows
        self.cols = cols
        self.scope = scope
        self.boxes = []

        self.pos = recordtype('pos', 'rownum colnum')

        for i in range(rows):
            row_box = []
            for j in range(cols):
                row_box.append(self.pos(i, j))
            self.boxes.append(row_box)

        self.current_pos = self.pos(random.randint(0, self.rows - 1), random.randint(0, self.cols - 1))

        self.food = self.pos(random.randint(0, self.rows - 1), random.randint(0, self.cols - 1))
        self.food_1 = self.pos(random.randint(0, self.rows - 1), random.randint(0, self.cols - 1))

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
                elif self.boxes[i][j] == self.food_1:
                    print("\033[91mF\033[m", end=" ")
                else:
                    distance = (abs(i - self.current_pos.rownum) + (abs(j - self.current_pos.colnum)))

                    if distance <= self.scope:
                        print("\033[96mO\033[m", end=" ")
                    else:
                        print("O", end=" ")
            print()
        print()

    def move_up(self):
        if self.current_pos.rownum > 0:
            self.current_pos.rownum -= 1
        return int(self.current_pos == self.food or self.current_pos == self.food_1)

    def move_down(self):
        if self.current_pos.rownum < self.rows - 1:
            self.current_pos.rownum += 1
        return int(self.current_pos == self.food or self.current_pos == self.food_1)

    def move_left(self):
        if self.current_pos.colnum > 0:
            self.current_pos.colnum -= 1
        return int(self.current_pos == self.food or self.current_pos == self.food_1)
    
    def move_right(self):
        if self.current_pos.colnum < self.cols - 1:
            self.current_pos.colnum += 1
        return int(self.current_pos == self.food or self.current_pos == self.food_1)

    def get_state(self):
        states = []

        distance = (abs(self.food.rownum - self.current_pos.rownum) + (abs(self.food.colnum - self.current_pos.colnum)))
        distance_1 = (abs(self.food_1.rownum - self.current_pos.rownum) + (abs(self.food_1.colnum - self.current_pos.colnum)))

        if distance <= self.scope:
            rowdistance = self.current_pos.rownum - self.food.rownum
            coldistance = self.current_pos.colnum - self.food.colnum

            rowdistance_normalized = 1 if rowdistance > 0 else -1 if rowdistance < 0 else 0
            coldistance_normalized = 1 if coldistance > 0 else -1 if coldistance < 0 else 0

            states.append(self.current_pos.rownum - self.food.rownum)
            states.append(self.current_pos.colnum - self.food.colnum)
        else:
            states.append(0)
            states.append(0)

        if distance_1 <= self.scope:
            rowdistance_1 = self.current_pos.rownum - self.food_1.rownum
            coldistance_1 = self.current_pos.colnum - self.food_1.colnum

            rowdistance_normalized_1 = 1 if rowdistance_1 > 0 else -1 if rowdistance_1 < 0 else 0
            coldistance_normalized_1 = 1 if coldistance_1 > 0 else -1 if coldistance_1 < 0 else 0

            states.append(self.current_pos.rownum - self.food_1.rownum)
            states.append(self.current_pos.colnum - self.food_1.colnum)
        else:
            states.append(0)
            states.append(0)
        
        if len(states) == 0:
            states = [0] * 4

        return np.array(states)

    def is_done(self):
        if self.current_pos == self.food or self.current_pos == self.food_1:
            return True
        return False


if __name__ == "__main__":
    env = Environment(16, 16, 10)
    env.current_pos = env.pos(0, 0)
    env.food = env.pos(8, 0)

    print(env.get_state())