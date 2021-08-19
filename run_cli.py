from pydynamica.env import Env
import time

env = Env(num_agents=100, dim=(100,100))
env.step()

while True:
    time.sleep(0.2)
    outcome = env.step()
    sorted_list = sorted(env.agents, key=lambda a: a.calculate_score())

    print("Top 10")
    avg = sum([a.risk for a in sorted_list[-10:]]) / 10
    print(f"average risk: {avg} | wealth: {sorted_list[-10:][0].calculate_score()}")

    '''
    for agent in sorted_list[10:]:
        print(f"Agent {agent.id}:\n\tScore: {agent.calculate_score()}\n\tRisk Factor: {agent.risk}")
    '''

    print("Bottom 10")
    avg = sum([a.risk for a in sorted_list[:10]]) / 10
    avg_food = sum([a.wealth_food for a in sorted_list[:10]]) / 10
    avg_mineral = sum([a.wealth_minerals for a in sorted_list[:10]]) / 10
    avg_money = sum([a.money for a in sorted_list[:10]]) / 10
    print(f"average risk: {avg} | food {avg_food}, mineral {avg_mineral}, money {avg_money}")
    '''
    for agent in sorted_list[:10]:
        print(f"Agent {agent.id}:\n\tScore: {agent.calculate_score()}\n\tRisk Factor: {agent.risk}")
    '''
