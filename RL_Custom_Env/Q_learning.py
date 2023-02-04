import numpy as np
import math
from gym import Env
import random

import mazeEscapeGame
from ClassesMazeEscape.LOCATIONS import LOCATIONS


def qTrain(environment:type[Env], numberOfEpisodes):
    """
    Algorithm for Q-learning
    Q_update(State, Action) = Q_old(State, Action) + alpha(r_t + gamma*maxQ(State_t+1, Action) - Q_old(State, Action))

    returns the trained Q-table
    """
    isFirstCall = True
    qTable = np.zeros(((environment.observation_space.high, environment.observation_space.high) + (environment.action_space.n,)))

    for episode in range(0, numberOfEpisodes):
        state = environment.reset()
        done = False
        while not done:
            if (isFirstCall):
                action = environment.action_space.sample()
                isFirstCall = False
            else:
                action = epsilonGreedyPolicy(qTable, episode, numberOfEpisodes, environment, state)
            newState, reward, done, info = environment.step(action)
            qTable = qLearn(qTable, episode, numberOfEpisodes, state, newState, reward, action)
            state = newState
    return qTable

def epsilonGreedyPolicy(qTable, episodeNumber, totalEpisodes, environment:type[Env], currentState):
    """
    epsilon-greedy-policy
    the function to determine if the agent will explore or exploit previous traning data
    this function requires randomness to choose between exploitation and exploration

    returns an action
    """
    randomValue = random.uniform(0.0, 1.0)
    # epsilon = epsilonDecay(episodeNumber, totalEpisodes)
    epsilon = 0.75
    if (randomValue < epsilon):
        # if random value is less than the epsilon value, then explore
        action = environment.action_space.sample()
    else:
        # if random value is greater than the epsilon value, then exploit previously known data
        action = np.argmax(qTable[currentState]) # gets the indices of the largest qValue in the current state's row
    return action
    
def alphaDecay(episodeNumber, totalEpisodes):
    """
    Decay function for alpha value with respect to episode number
    """
    minimumAlpha = 0.15
    maximumAlpha = 1.0
    timeConstant = 2 / (0.9 * totalEpisodes)
    alphaValue = (maximumAlpha - minimumAlpha) * math.exp((-1) * timeConstant * episodeNumber)
    return alphaValue

def gammaDecay(episodeNumber, totalEpisodes):
    """
    Decay function for gamma value with respect to episode number
    """
    minimumGamma = 0.1
    maximumGamma = 1.0
    timeConstant = 2 / (0.9 * totalEpisodes)
    gammaValue = (maximumGamma - minimumGamma) * math.exp((-1) * timeConstant * episodeNumber)
    return gammaValue

def epsilonDecay(episodeNumber, totalEpsiodes):
    """
    Decay function for epsilon value with respect to episode number
    """
    minimumEpsilon = 0.5
    maximumEpsilon = 0.8
    timeConstant = 2 / (0.8 * totalEpsiodes)
    epsilonValue = (maximumEpsilon - minimumEpsilon) * math.exp((-1) * timeConstant * episodeNumber)
    return epsilonValue

def qLearn(qTable, episodeNumber, totalEpisodes, currentState, newState, reward, action):
    """
    Function which holds the Q-learning algorithm, calls the 3 decay functions and returns the updated Q-table
    """
    alpha = 0.75
    gamma = 0.6
    # alpha = alphaDecay(episodeNumber, totalEpisodes)
    # gamma = gammaDecay(episodeNumber, totalEpisodes)
    qTable[currentState][action] = qTable[currentState][action] + alpha * (reward + gamma * np.max(qTable[newState]) - qTable[currentState][action])
    return qTable



test123 = LOCATIONS(6, 1280, 720).getMap()

test = mazeEscape(10)
episodes = 4

qTable = qTrain(test, 500)

for episode in range(0, episodes):
    state = test.reset()
    done = False
    score = 0
    while not done:
        test.render()
        action = np.argmax(qTable[state])
        state, reward, done, info = test.step(action)
        print("state:{}".format(state))
        time.sleep(0.1)
        score += reward
    print("Episode:{}, Score:{}".format(episode, score))
test.close()