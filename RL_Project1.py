import os
import gym
from stable_baselines3 import ppo
from stable_baselines3.common.vec_env import DummyVecEnv
from stable_baselines3.common.evaluation import evaluate_policy

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

file_setup()
environment_Name = "CartPole-v1"
# env = gym.make(environment_Name)
# print(env.action_space)
# print(env.observation_space)
# episodes = 10
# for episode in range(1, episodes + 1):
#     state = env.reset()
#     done = False
#     score = 0
#     while (not done):
#         env.render()
#         action = env.action_space.sample()
#         n_state, reward, done, info = env.step(action)
#         score += reward
#     print("Episode:{} Score:{}".format(episode, score))
# env.close()

log_path = "A:\VisualStudiosCode\PythonProjects\RL_Project\RL_Project1\Training\Logs"

env = gym.make(environment_Name)
env = DummyVecEnv([lambda: env])
# model = ppo('MlpPolicy', env, verbose=1, tensorboard_log = log_path)