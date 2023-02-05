import os
import gym
from stable_baselines3 import PPO
from stable_baselines3.common.vec_env import DummyVecEnv
from stable_baselines3.common.evaluation import evaluate_policy
from stable_baselines3.common.callbacks import EvalCallback, StopTrainingOnRewardThreshold
from stable_baselines3.common.env_checker import check_env
import math
import numpy as np

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

def setup_environment(environment_name):
    env = gym.make(environment_name)
    return env

def setup_agent(environment, log_path):
    env = DummyVecEnv([lambda: environment])
    model = PPO('MlpPolicy', env, verbose=1, tensorboard_log = log_path)
    return model

def setup_agent_w_policy_change(environment, log_path):
    neural_net_architecture = [dict(pi=[128,128,128,128], vf=[128,128,128,128])]
    env = DummyVecEnv([lambda: environment])
    model = PPO('MlpPolicy', env, verbose=1, tensorboard_log=log_path, policy_kwargs={'net_arch':neural_net_architecture})
    return model

def train_model_basic(agent:type[PPO], savePath, total_timesteps_value = 50000):
    print("Basic Training of Agent:")
    agent.learn(total_timesteps=total_timesteps_value)
    agent.save(savePath)

def train_model_w_callback(agent:type[PPO], environment, savePath, total_timesteps_value = 50000):
    print("Training Agent with Callback:")
    stop_callback = StopTrainingOnRewardThreshold(reward_threshold=500, verbose=1)
    eval_callback = EvalCallback(environment, callback_on_new_best=stop_callback, eval_freq=10000, best_model_save_path=savePath, verbose=1)
    agent.learn(total_timesteps=total_timesteps_value, callback=eval_callback)
    
def testing_model(model: type[PPO], environment, number_of_steps=10):
    for step in range(1, number_of_steps + 1):
        obs = environment.reset()
        done = False
        score = 0
        while (not done):
            action, _states = model.predict(obs) # now using the model
            obs, reward, done, info = environment.step(action)
            environment.render()
            score += reward
        print("Episode:{} Score:{}".format(step, round(score, 3)))

def main():
    learning = False
    testing = True
    environment_name = "CartPole-v1"
    PPO_Path = os.path.join(os.path.dirname(__file__), "Training", "Models", "Model_" + environment_name)
    save_path = os.path.join(os.path.dirname(__file__), "Training", "Models")
    log_path = "A:\VisualStudiosCode\PythonProjects\RL_Project\RL_Project1\Training\Logs"

    file_setup()
    environment = setup_environment(environment_name)
    environment.reset()
    testAction = environment.action_space.sample()
    obs, reward, done, info = environment.step(testAction)

    if (learning):
        print("Training with PPO Model With Callback:")
        agent = setup_agent(environment, log_path)
        train_model_w_callback(agent, environment, savePath=save_path, total_timesteps_value=35000)
        agentWithPolicyChange = setup_agent_w_policy_change(environment, log_path)
        train_model_basic(agent, PPO_Path, 35000)
        train_model_w_callback(agentWithPolicyChange, environment, savePath=save_path, total_timesteps_value=35000)
    else:
        agent = PPO.load(PPO_Path)

    if (testing):
        print("testing the model:")
        testing_model(agent, environment, 10)
    environment.close()

if (__name__ == "__main__"):
    main()