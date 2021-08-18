from env import Env
import time

env = Env(num_agents=100, dim=(100,100))
env.step()

while True:
    #time.sleep(0.2)
    outcome = env.step()

