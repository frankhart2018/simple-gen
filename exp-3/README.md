# Experiment 3

**Number of agents**: 1
<br><br>
**Number of food particle(s)**: 1
<br><br>
**World Size**: 16 x 16
<br><br>
**Scope**: 10
<br><br>
**State Size**: 2
<br><br>
**Action Size**: 4
<br><br>
**Algorithm**: REINFORCE
<br><br>
**NN**: 2 Layer FC [2 -> 16 (ReLU) -> 4 (Softmax)]
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
**Cell Representation when not in scope**: O (None)
<br><br>
**Cell Representation when in scope**: O (Light Blue)

## Solving the environment

The environment is solved when the agent eats the food partcle.

## Scope 

Distance to which an agent can perceive the world. Distance here is Manhattan Distance.

## State Description

The state consists of two zeroes if food particle is outside scope, otherwise it consists of the distance vector (x, y) to the food particle.

![State](images/state.png)

In this position the state is [1, 1] which corresponds to the distance in x, y, to the food particle.

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
**Training success ratio**: 0.7434
<br><br>
**Testing success ratio**: 0.7606

