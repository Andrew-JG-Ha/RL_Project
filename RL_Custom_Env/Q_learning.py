import numpy as np

def Q_learn():
    """
    Algorithm for Q-learning
    Q_update(State, Action) = Q_old(State, Action) + alpha(r_t + gamma*maxQ(State_t+1, Action) - Q_old(State, Action))
    """
    alpha = 0.5
    gamma = 0.5

    pass

def epsilon_greedy_policy():
    """
    epsilon-greedy-policy
    the function to determine if the agent will explore or exploit previous traning data
    """
    epsilon = 0.5
    pass