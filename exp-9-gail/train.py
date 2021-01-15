import numpy as np
from IPython.display import clear_output
import glob
import os

import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader

from gail.model import GAIL

ENVIRONMENT_SIZE = 16
BATCH_SIZE = 32

class BCDataset(Dataset):
    
    def __init__(self, npy_dir):
        files = glob.glob(os.path.join(npy_dir, "*.npy"))
        self.trajectories = []
        
        for file in files:
            self.trajectories.append(np.load(file, allow_pickle=True))
        
        self.trajectories = np.vstack(self.trajectories)
        
    def __len__(self):
        return len(self.trajectories)
    
    def __getitem__(self, idx):
        state, action = self.trajectories[idx]
        
        return np.array(state, dtype=np.float32), action

training_dataset = BCDataset("expert-dir")

from collections import Counter, OrderedDict

def get_training_distribution(dataset):
    actions = Counter([dataset[i][1] for i in range(len(dataset))])
    actions = {action:1/count for action, count in actions.items()}
    actions = OrderedDict(sorted(actions.items()))
    return torch.tensor(list(actions.values()))

training_dataloader = DataLoader(training_dataset, batch_size=BATCH_SIZE, shuffle=True, num_workers=0)

STATE_SIZE = 20
ACTION_SIZE = 5

model = GAIL(s_size=STATE_SIZE, a_size=ACTION_SIZE, batch_size=BATCH_SIZE)

from tqdm import tqdm, trange

EPISODES = 2000

episode_losses = []
episode_losses_actor = []

t = trange(EPISODES, desc="Episode")
for current_episode_num in t:
    current_episode_loss = 0
    current_episode_loss_actor = 0
    
    for i, data in enumerate(training_dataloader):
        states, actions = data
        actions = actions.unsqueeze(1)
        
        loss, loss_actor = model.backward_pass(states, actions)
        current_episode_loss += loss
        current_episode_loss_actor += loss_actor
        
    t.set_description(f"Loss {current_episode_loss / len(training_dataloader)}, Loss Actor {current_episode_loss_actor / len(training_dataloader)}")
    t.refresh()
       
    episode_losses.append(current_episode_loss / len(training_dataloader))
    episode_losses_actor.append(current_episode_loss_actor / len(training_dataloader))

import time

from environment import Environment

def test(max_steps, speed=0.5, agent_pos=None, food_pos=None, render=True):
    model.actor.eval()
    
    env = Environment(rows=16, cols=16, scope=10)

    if agent_pos != None:
        env.current_pos = env.pos(agent_pos[0], agent_pos[1])

    if food_pos != None:
        env.food = env.pos(food_pos[0], food_pos[1])

    i = 0
    success = True
    while (not env.is_done()):
        clear_output(wait=True)
        print(f"Step: {i+1}, Food: {env.consumed_count}")
        if i == max_steps or env.num_food == 0:
            success = False
            break

        state = env.get_state()
        state = torch.from_numpy(state).unsqueeze(0)
        
        with torch.no_grad():
            action = int(model.forward_pass(state.float())[0].item())
            print(f"Action: {action}")

        reward = 0
        if action == 0:
            reward = env.move_up()
        elif action == 1:
            reward = env.move_left()
        elif action == 2:
            reward = env.move_down()
        elif action == 3:
            reward = env.move_right()
        elif action == 4:
            reward = env.ingest()

        if render:
            env.render()

        i += 1

        time.sleep(speed)

    return success, env.consumed_count

test()