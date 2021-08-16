from env import Env
import time

env = Env()

while True:
    time.sleep(0.2)
    env.step()

