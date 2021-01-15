# Agent class representing the NN for REINFORCE algorithm

# Import required libraries
import torch
import torch.nn as nn
from torch.distributions import Categorical
import torch.nn.functional as F


class Actor(nn.Module):
   
    def __init__(self, s_size, a_size, device=torch.device('cpu'), h_size=64):
        super(Actor, self).__init__()
        self.device = device

        self.fc1 = nn.Linear(s_size, h_size)
        self.leaky_relu = nn.LeakyReLU()
        self.fc2 = nn.Linear(h_size, a_size)

    def forward(self, state):
        x = self.fc1(state)
        x = self.leaky_relu(x)
        x = self.fc2(x)

        return F.softmax(x, dim=1)

class Discriminator(nn.Module):
   
    def __init__(self, s_size, a_size, device=torch.device('cpu'), h_size=64):
        super(Discriminator, self).__init__()
        self.device = device

        self.fc1 = nn.Linear(s_size+1, h_size)
        self.leaky_relu = nn.LeakyReLU()
        self.fc2 = nn.Linear(h_size, 1)

    def forward(self, state, action):
        state_action = torch.cat([state, action], 1)
        x = self.fc1(state_action)
        x = self.leaky_relu(x)
        x = self.fc2(x)

        return torch.sigmoid(x)