import numpy as np
import math
from gym import Env

def qTrain(environment:type[Env], numberOfEpisodes):
    """
    Algorithm for Q-learning
    Q_update(State, Action) = Q_old(State, Action) + alpha(r_t + gamma*maxQ(State_t+1, Action) - Q_old(State, Action))
    """
    alpha = 0.5
    gamma = 0.5
    q_table = np.zeros((pow(environment.observation_space.high, 2), environment.action_space.n))

    for i in range(0, numberOfEpisodes):
        state = environment.reset()

        done = False

        while not done:
            qLearn(q_table, )

    return q_table, maxReward

def epsilonGreedyPolicy():
    """
    epsilon-greedy-policy
    the function to determine if the agent will explore or exploit previous traning data
    this function requires randomness to choose between exploitation and exploration
    """
    epsilon = 0.5
    
def alphaDecay(episodeNumber):
    """
    Decay function for alpha value with respect to step number
    """
    pass

def gammaDecay(episodeNumber):
    """
    Decay function for gamma value with respect to step number
    """
    pass

def qLearn(table, episodeNumber):
    """
    Function which holds the Q-learning algorithm
    """
    alpha = alphaDecay(episodeNumber)
    gamma = gammaDecay(episodeNumber)
    epsilonGreedyPolicy()