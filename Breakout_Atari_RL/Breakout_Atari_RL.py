import os
import gym
import numpy as np
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.layers import Dense, Flatten, Conv2D
from tensorflow.keras.models import Sequential

from rl.agents import DQNAgent
from rl.memory import SequentialMemory
from rl.policy import EpsGreedyQPolicy, LinearAnnealedPolicy

from ale_py.roms import Breakout
from ale_py import ALEInterface
ale = ALEInterface()
ale.loadROM(Breakout)

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
    model.add(Dense(512, activation="relu", name="dense1"))
    model.add(Dense(256, activation="relu", name="dense2"))
    model.add(Dense(actions, activation="linear", name = "dense3"))
    return model

def build_agent(model, actions):
    policy = LinearAnnealedPolicy(EpsGreedyQPolicy(), attr="eps", value_max=1., value_min=.1, value_test=.2, nb_steps=10000) # Degradation of learning rate, epsilon and discount rate as we get nearer to the goal
    memory = SequentialMemory(limit=1000, window_length=3) # letting the agent read from memory
    dqn = DQNAgent(model=model, memory=memory, policy=policy, enable_dueling_network=True, dueling_type="avg", nb_actions=actions, nb_steps_warmup=10000)
    return dqn

def main():
    train = True
    testing = True
    file_setup()

    environment_name = 'Breakout-v4'
    environment = gym.make(environment_name, render_mode = "human")

    height, width, channels = environment.observation_space.shape
    actions = environment.action_space.n

    model = build_model(height, width, channels, actions)

    dqn = build_agent(model, actions)
    dqn.compile(Adam(learning_rate=0.001))
    dqn.fit(env=environment, nb_steps=1000, visualize=False, verbose=2)
    
    scores = dqn.test(environment, nb_episodes=10, visualize=False)
    print(np.mean(scores.history["episode reward"]))

    episodes = 5
    for episode in range(1, episodes+1):
        done = False
        obs = environment.reset()
        score = 0
        while not done:
            action = environment.action_space.sample()
            obs, reward, done, info = environment.step(action=action)
            score += reward
        print("Episode:{} Score:{}".format(episode, round(score, 3)))


if __name__ == "__main__":
    main()