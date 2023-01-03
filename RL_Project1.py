import os
import gym
from stable_baselines3 import PPO
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

def setup_environment(environment_name, debug=False):
    environment_Name = "CartPole-v1"
    env = gym.make(environment_Name)
    if (debug):
        print(env.action_space)
        print(env.observation_space)
        episodes = 10
        for episode in range(1, episodes + 1):
            state = env.reset()
            done = False
            score = 0
            while (not done):
                env.render()
                action = env.action_space.sample()
                n_state, reward, done, info = env.step(action)
                score += reward
            print("Episode:{} Score:{}".format(episode, score))
        env.close()
    return env

def setup_agent(environment_name, log_path):
    env = setup_environment(environment_name)
    env = DummyVecEnv([lambda: env])
    model = PPO('MlpPolicy', env, verbose=1, tensorboard_log = log_path)
    return model

def save_model(environment_name):
    

def main():
    environment_name = "CartPole-v1"
    log_path = "A:\VisualStudiosCode\PythonProjects\RL_Project\RL_Project1\Training\Logs"
    file_setup()
    agent = setup_agent(environment_name, log_path)
    agent.learn(total_timesteps=10000)



if (__name__ == "__main__"):
    main()