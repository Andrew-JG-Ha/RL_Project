import numpy as np

def Q_learn(state, action):
    """
    Algorithm for Q-learning
    Q_update(State, Action) = Q_old(State, Action) + alpha(r_t + gamma*maxQ(State_t+1, Action) - Q_old(State, Action))
    """
    alpha = 0.5
    gamma = 0.5
    Q_value = Q_old(state, action) + alpha(r_t + gamma*maxarg(state_t+1, action) - Q_old(state, action))
    return Q_value

def epsilon_greedy_policy():
    """
    epsilon-greedy-policy
    the function to determine if the agent will explore or exploit previous traning data
    this function requires randomness to choose between exploitation and exploration
    """
    epsilon = 0.5
    