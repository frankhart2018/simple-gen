import torch

from .agent import Agent

class DDPGModel:

    def __init__(self, initial_population, state_size, action_size):
        self.state_size = state_size
        self.action_size = action_size
        self.device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
        self.agents = []
        self.current_state = {}
        self.current_action = {}
        self.current_reward = {}

        if torch.cuda.is_available():
            print("Found GPU, training in GPU!")

        self.init(initial_population)

    def init(self, initial_population):
        for idx in range(initial_population):
            self.agents.append(
                Agent(self.state_size, self.action_size, self.device)
            )

            self.current_reward[idx] = 0

    def predict_action(self, idx, state):
        action, action_probs = self.agents[idx].act(state)

        self.current_state[idx] = state
        self.current_action[idx] = action_probs.detach().cpu()

        return action, []

    def update_reward(self, idx, reward):
        self.current_reward[idx] = reward

    def update_next_state(self, idx, next_state):
        self.agents[idx].step(self.current_state[idx], self.current_action[idx], self.current_reward[idx], next_state)

        self.current_state[idx] = 0
        self.current_action[idx] = 0
        self.current_reward[idx] = 0