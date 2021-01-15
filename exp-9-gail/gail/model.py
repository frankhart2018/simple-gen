# ReinforceModel class for REINFORCE RL algorithm

# Import required libraries
import torch
import torch.optim as optim
import torch.nn as nn
import numpy as np

# Import the NN
from .nn import Actor, Discriminator


class GAIL:

    def __init__(self, s_size, a_size, h_size=64, batch_size=32):
        self.s_size = s_size
        self.a_size = a_size
        self.h_size = h_size
        self.batch_size = batch_size
        self.device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

        self.actor = Actor(s_size=s_size, a_size=a_size, h_size=h_size, device=self.device).to(self.device)
        self.discriminator = Discriminator(s_size=s_size, a_size=a_size, h_size=h_size, device=self.device).to(self.device)

        self.actor_optim = optim.Adam(self.actor.parameters(), lr=1e-3)
        self.discriminator_optim = optim.Adam(self.discriminator.parameters(), lr=1e-3)

        self.loss_fn = nn.BCELoss()

    def forward_pass(self, state):
        action = self.actor(state)
        _, action = torch.max(action, 1)

        return action.float()

    def forward_discrimination(self, state, action):
        probs = self.discriminator(state, action)

        return probs

    def backward_pass(self, state, expert_actions):
        # Discriminator backprop
        self.discriminator_optim.zero_grad()

        state = state.float().to(self.device)
        expert_actions = expert_actions.float().to(self.device)

        actor_action = self.forward_pass(state)
        actor_action = actor_action.unsqueeze(1)

        expert_label = torch.full((len(state), 1), 1, device=self.device)
        actor_label = torch.full((len(state), 1), 0, device=self.device)

   
        expert_probability = self.forward_discrimination(state, expert_actions)
        loss = self.loss_fn(expert_probability, expert_label)

        actor_probability = self.forward_discrimination(state, actor_action)
        loss += self.loss_fn(actor_probability, actor_label)

        loss.backward()
        self.discriminator_optim.step()

        # Actor backprop
        self.actor_optim.zero_grad()

        loss_actor = -self.forward_discrimination(state, actor_action)
        loss_actor.mean().backward()
        self.actor_optim.step()

        return loss.item(), -loss_actor.mean().item()