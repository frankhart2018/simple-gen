import time
import random
import torch
import os

from environment import Environment
from reinforce.model import ReinforceModel

model = ReinforceModel(initial_population=1, state_size=2, action_size=4)
model.agents[0].load_state_dict(torch.load('experiment-3-5k.pth'))

def test(max_steps, speed=0.5, agent_pos=None, food_pos=None, render=True):
    env = Environment(rows=16, cols=16, scope=10)

    if agent_pos != None:
        env.current_pos = env.pos(agent_pos[0], agent_pos[1])

    if food_pos != None:
        env.food = env.pos(food_pos[0], food_pos[1])

    i = 0
    success = True
    while (not env.is_done()):
        if i == max_steps:
            success = False
            break

        state = env.get_state()
        print(state)
        action, _ = model.predict_action(0, state)

        reward = 0
        if action == 0:
            reward = env.move_up()
        elif action == 1:
            reward = env.move_down()
        elif action == 2:
            reward = env.move_left()
        elif action == 3:
            reward = env.move_right()

        if render:
            env.render()

        i += 1

        time.sleep(speed)

    return success

if __name__ == "__main__":
    num_experiments = 100

    clear = lambda: os.system('clear')

    success_count = 0
    for i in range(num_experiments):
        success = test(max_steps=100, speed=100, render=True)
        if success:
            success_count += 1

        print(f"\rSuccess ratio: {success_count/num_experiments}")
