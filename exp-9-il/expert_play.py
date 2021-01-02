import numpy as np
import getch
import time

from environment import Environment

env = Environment(rows=16, cols=16, scope=10)

num_moves = 250
current_move_num = 0

states_actions = []
action_char_to_num = {"w": 0, "a": 1, "s": 2, "d": 3, "x": 4}
action_to_action_num = {"w": env.move_up, "a": env.move_left, "s": env.move_down, "d": env.move_right,
                            "x": env.ingest}

while current_move_num < num_moves:
    env.render(blind_mode=True)

    state = env.get_state()
    action = getch.getch()
    
    if action in action_to_action_num.keys():
        states_actions.append([state, action_char_to_num[action]])

        action_to_action_num[action]()
        current_move_num += 1
    else:
        print(f"Invalid move {action}")

getch.getch()

states_actions = np.asarray(states_actions, dtype=object)
np.save(str(int(time.time())) + ".npy", states_actions)