import os
import gymnasium as gym
from stable_baselines3 import A2C
from stable_baselines3.common.callbacks import EvalCallback, StopTrainingOnRewardThreshold
from stable_baselines3.common.vec_env import VecFrameStack
from stable_baselines3.common.evaluation import evaluate_policy
from stable_baselines3.common.env_util import make_atari_env
from ale_py.roms import Breakout
from ale_py import ALEInterface

def file_setup():
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


def main():
    train = True
    testing = True
    file_setup()

    a2c_path = os.path.join(os.path.dirname(__file__), "Training", "Models", "A2C_Breakout_Model")

    # ale = ALEInterface()
    # ale.loadROM(Breakout)
    environment_name = 'ALE/Breakout-v5'
    environment = gym.make(environment_name, render_mode = 'human')

    print(environment.action_space)
    print(environment.observation_space)

    episodes = 5
    for episode in range(1, episodes+1):
        done = False
        obs = environment.reset()
        score = 0
        while not done:
            action = environment.action_space.sample()
            obs, reward, done, truncated, info = environment.step(action=action)
            score += reward
            
        print("Episode:{} Score:{}".format(episode, score))


if __name__ == "__main__":
    main()