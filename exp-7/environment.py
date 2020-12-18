from recordtype import recordtype
import random
import numpy as np
import time

class Environment:

    def __init__(self, rows, cols, scope=10, num_food=5, max_pad=10):
        self.rows = rows
        self.cols = cols
        self.scope = scope
        self.num_food = num_food
        self.max_pad = max_pad
        self.boxes = []

        self.pos = recordtype('pos', 'rownum colnum')

        for i in range(rows):
            row_box = []
            for j in range(cols):
                row_box.append(self.pos(i, j))
            self.boxes.append(row_box)

        self.current_pos = self.pos(random.randint(0, self.rows - 1), random.randint(0, self.cols - 1))

        self.foods = [self.pos(random.randint(0, self.rows - 1), random.randint(0, self.cols - 1)) for _ in range(self.num_food)]

    def pos_is_food(self, current_pos, return_idx=False):
        for i, food in enumerate(self.foods):
            if current_pos == food:
                if return_idx:
                    return True, i
                return True
        
        if return_idx:
            return False, -1
        return False

    def render(self, reward=None):
        if reward != None:
            print("-" * self.rows)
            print(f"Reward: {reward}")
            print("-" * self.rows)
        for i in range(self.rows):
            for j in range(self.cols):
                if self.boxes[i][j] == self.current_pos:
                    print("\033[94mX\033[m", end=" ")
                elif self.pos_is_food(self.boxes[i][j]):
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
        return int(self.pos_is_food(self.current_pos))

    def move_down(self):
        if self.current_pos.rownum < self.rows - 1:
            self.current_pos.rownum += 1
        return int(self.pos_is_food(self.current_pos))

    def move_left(self):
        if self.current_pos.colnum > 0:
            self.current_pos.colnum -= 1
        return int(self.pos_is_food(self.current_pos))
    
    def move_right(self):
        if self.current_pos.colnum < self.cols - 1:
            self.current_pos.colnum += 1
        return int(self.pos_is_food(self.current_pos))

    def pad_state(self, state):
        for i in range(self.max_pad - len(state)):
            state.append(0)

        return state

    def get_state(self):
        states = []

        for food in self.foods:
            distance_x = self.current_pos.rownum - food.rownum
            distance_y = self.current_pos.colnum - food.colnum
            distance = abs(distance_x) + abs(distance_y)

            if distance < self.scope:
                states += [distance_x, distance_y]
            else:
                states += [0] * 2
       
        if len(states) < self.max_pad:
           states = self.pad_state(states)

        return np.array(states)

    def is_done(self):
        if self.num_food > 0:
            is_food, food_idx = self.pos_is_food(self.current_pos, return_idx=True)
            if is_food:
                self.num_food -= 1
                del self.foods[food_idx]
            
            return False

        return False


if __name__ == "__main__":
    env = Environment(16, 16, 10)
    env.current_pos = env.pos(10, 1)

    env.foods = [env.pos(1, 11), env.pos(10, 2)]

    print(env.pos_is_food(env.current_pos))