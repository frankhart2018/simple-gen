# Experiment 1

**Number of agents**: 1
<br><br>
**Number of food particle(s)**: 1
<br><br>
**World Size**: 16 x 16
<br><br>
**State Size**: 8
<br><br>
**Action Size**: 4
<br><br>
**Algorithm**: REINFORCE
<br><br>
**NN**: 2 Layer FC [8 -> 16 (ReLU) -> 4 (Softmax)]
<br><br>
**Optimizer**: Adam (LR=1e-2)
<br><br>
**Model Updates**: At the end of episode
<br><br>
**Starting position of Agent**: Random 
<br><br>
**Position of food particle(s)**: Random
<br><br>
**Agent Representation**: X (Indigo)
<br><br>
**Food Representation**: F (Red)
<br><br>
**Cell Representation**: O (Green)

## State Description

The state is the distance of the food particle from the agent when it moves one place in 8 directions (N, E, S, W, NE, NW, SE, SW in order).

![State](images/state.png)

In this position the state is [2, 2, 4, 4, 1, 3, 3, 5] which corresponds to the Manhattan Distance when the agent moves one position to N, E, S, W, NE, NW, SE, SW direction respectively.

## Actions

The agent can take **four** different actions:-

1) Action 0 - Move up
2) Action 1 - Move down
3) Action 2 - Move left
4) Action 3 - Move right

## Results

**Number of training episodes**: 5000
<br><br>
**Maximum number of steps**: 100
<br><br>
**Number of testing episodes**: 5000
<br><br>
**Training success ratio**: 0.8504
<br><br>
**Testing success ratio**: 1.0

