# ReinforceModel class for REINFORCE RL algorithm

# Import required libraries
import torch
import torch.optim as optim
import numpy as np

# Import the NN
from .nn import Actor, Discriminator


class GAIL:

    def __init__(self, s_size, a_size, h_size=64, batch_size=32):
        self.s_size = s_size
        self.a_size = a_size
        self.h_size = h_size
        self.batch_size = batch_size

        self.actor = Actor(s_size=s_size, a_size=a_size, h_size=h_size)
        self.discriminator = Discriminator(s_size=s_size, a_size=a_size, h_size=h_size)

        self.actor_optim = optim.Adam(actor.parameters(), lr=1e-3)
        self.discriminator_optim = optim.Adama(discriminator.parameters(), lr=1e-3)

        self.loss_fn = nn.BCELoss()

    def forward_pass(self, state):
        action = self.actor(state)

        return action

    def forward_discrimination(self, state, action):
        probs = self.discriminator(state, action)

        return probs

    def backward_pass(self, state, expert_actions):
        # Discriminator backprop
        self.discriminator_optim.zero_grad()

        actor_action = self.forward_pass(state)

        expert_label = torch.full((self.batch_size, 1), 1)
        actor_label = torch.full((self.batch_size, 1), 0)

        expert_ probability = self.forward_discrimination(state, expert_actions)
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