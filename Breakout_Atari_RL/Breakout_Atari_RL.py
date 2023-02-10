import os
import gymnasium as gym
import numpy as np
from tensorflow.python.keras.models import Sequential
from tensorflow.python.keras.layers import Dense, Flatten, Conv2D
from tensorflow.python.keras.optimizers import adam_v2

from rl.agents import DQNAgent
from rl.memory import SequentialMemory
from rl.policy import EpsGreedyQPolicy, LinearAnnealedPolicy

from ale_py.roms import Breakout
from ale_py import ALEInterface

def file_setup():
    """
    Basic file setup, creating the parent and sub directories to store logss and models
    """
    parentFolder = "Training"
    logsFolder = "Logs"
    modelsFolder = "Models"
    currentPath = os.path.abspath(os.path.dirname(__file__))
    parentPath = os.path.normpath(os.path.join(currentPath, parentFolder))
    logsPath = os.path.normpath(os.path.join(parentPath, logsFolder))
    modelsPath = os.path.normpath(os.path.join(parentPath, modelsFolder))
    if (not os.path.exists(parentPath)):
        os.mkdir(parentPath)
        if (not os.path.exists(logsPath)):
            os.mkdir(logsPath)
        if (not os.path.exists(modelsPath)):
            os.mkdir(modelsPath)

def build_model(height, width, channels, actions):
    model = Sequential()
    model.add(Conv2D(32, (8,8), strides=(4,4), activation="relu", input_shape=(3, height, width, channels))) # convolution neural net with 32 filters of size 8x8
    model.add(Conv2D(64, (4,4), strides=(2,2), activation="relu")) # convolution neural net with 64 filters of size 4x4
    model.add(Conv2D(64, (3,3), activation="relu")) # convolution neural net with 64 filters of size 3x3
    model.add(Flatten())
    model.add(Dense(512, activation="relu"))
    model.add(Dense(256, activation="relu"))
    model.add(Dense(actions, activation="linear"))
    return model

def build_agent(model, actions):
    policy = LinearAnnealedPolicy(EpsGreedyQPolicy(), attr="eps", value_max=1., value_min=.1, value_test=.2, nb_steps=10000) # Degradation of learning rate, epsilon and discount rate as we get nearer to the goal
    memory = SequentialMemory(limit=1000, window_length=3) # letting the agent read from memory
    dqn = DQNAgent(model=model, memory=memory, policy=policy, enable_double_dqn=True, dueling_type="avg", nb_actions=actions, nb_steps_warmup=10000)
    return dqn

def main():
    train = True
    testing = True
    file_setup()

    environment_name = 'ALE/Breakout-v5'
    environment = gym.make(environment_name, render_mode = 'human')

    height, width, channels = environment.observation_space.shape
    actions = environment.action_space.n

    model = build_model(height, width, channels, actions)

    model.summary()

    episodes = 5
    for episode in range(1, episodes+1):
        done = False
        obs = environment.reset()
        score = 0
        while not done:
            action = environment.action_space.sample()
            obs, reward, done, truncated, info = environment.step(action=action)
            score += reward
            
        print("Episode:{} Score:{}".format(episode, round(score, 3)))


if __name__ == "__main__":
    main()