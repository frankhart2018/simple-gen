# ReinforceModel class for REINFORCE RL algorithm

# Import required libraries
import torch
import torch.optim as optim

# Import the NN
from .agent import Agent


class ReinforceModel:
    """
    ReinforceModel class for the model - REINFORCE
    Data members
    ============
    state_size      (int)
        : Size of state (variables) that the agent experiences in environment
    action_size     (int)
        : Number of possible actions an agent can take
    device          (torch.device)
        : Device on which NN will be trained
    agents          (list)
        : List of all the Agent class' objects (i.e. NNs)
    optimizers      (list)
        : List of optimizers for individual agent
    scores          (dict)
        : Cummulative rewards of each individual agent over all trajectories
    saved_log_probs (dict)
        : Log probabilities of each agent for each trajectory
    rewards         (dict)
        : Rewards of agent at each trajectory
    policy_loss     (dict)
        : Loss function used for each individual agent
    """

    def __init__(self, initial_population, state_size, action_size):
        """
        Initializer for ReinforceModel class
        Params
        ======
        initial_population (int)
            : Number of player in the environment
        state_size         (int)
            : Size of state (variables) that the agent experiences in environment
        action_size        (int)
            : Number of possible actions an agent can take
        """

        self.state_size = state_size
        self.action_size = action_size
        self.device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
        self.agents = []
        self.optimizers = []
        self.scores = []
        self.saved_log_probs = {}
        self.rewards = {}
        self.policy_loss = {}

        # Initialize agents
        self.init(initial_population)

    def init(self, initial_population):
        """
        Initialize agents
        Params
        ======
        initial_population (int)
            : Number of player in the environment
        """

        # Loop through the entire population count
        for idx in range(initial_population):
            # Create NN for the player
            self.agents.append(
                Agent(self.state_size, self.action_size, self.device).to(self.device)
            )

            # Create optimizer for the agent
            self.optimizers.append(optim.Adam(self.agents[-1].parameters(), lr=1e-3))

            # Initialize each agents score with 0
            self.scores.append(0)

            # Create entries for each agent in log_probs, loss, and rewards dict
            self.saved_log_probs[idx] = []
            self.policy_loss[idx] = []
            self.rewards[idx] = []

    def predict_action(self, idx, state):
        """
        Predict action using NN
        Params
        ======
        idx   (int)
            : Id of agent for whom action is to be predicted
        state (numpy.ndarray)
            : State that the agent is experiencing in environment
        Returns
        =======
        action (numpy.ndarray)
            : Action taken at current state
        embed  (torch.Tensor)
            : Embedding computed from NN
        """

        # Compute action, lob probability of action and embedding from NN
        action, log_prob, embed = self.agents[idx].act(state)
        self.saved_log_probs[idx].append(log_prob)

        return action, embed

    def update_reward(self, idx, reward):
        """
        Update reward of an agent
        Params
        ======
        idx    (int)
            : Index of the agent whose reward is to be updated
        reward (int)
            : Reward that environment gave for taking certain action at a particular state
        """

        # Append the current reward to rewards list for this agent
        self.rewards[idx].append(reward)

    def update_single_agent(self, idx):
        """
        Update an agent
        Params
        ======
        idx (int)
            : Id of the agent to be updated
        """

        # If agent is alive and has experienced someting (i.e. taken some action in lifetime) then
        if type(self.agents[idx]) != int and len(self.saved_log_probs[idx]) > 0:
            # Set policy loss to an empty list
            self.policy_loss[idx] = []

            # Compute log_probs[i] * rewards[i] for current agent
            for j in range(len(self.saved_log_probs[idx])):
                self.policy_loss[idx].append(
                    -(self.saved_log_probs[idx][j] * self.rewards[idx][j])
                )

            self.saved_log_probs[idx] = []
            self.rewards[idx] = []

            # Sum all the products
            self.policy_loss[idx] = torch.cat(self.policy_loss[idx]).sum()

            # Backpropagate through the network
            self.optimizers[idx].zero_grad()
            self.policy_loss[idx].backward(retain_graph=True)
            self.optimizers[idx].step()

    def update_all_agents(self, start_pos):
        """
        Update all agent (i.e. backward propagation)
        """

        # Loop through all agents
        for idx in range(start_pos, len(self.agents)):
            self.update_single_agent(idx)