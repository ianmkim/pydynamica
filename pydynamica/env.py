from agent import Agent
from terrain import Resources, create_grid_world_parallel
import numpy as np
import random

class Env():
    def __init__(self,
            num_agents = 500,
            contact_horizon = 200,
            consume_rate = 0.1,
            collection_rate = 2,
            max_trades_per_step = 10,
            speed = 10,
            dim = (500,500),
            starting_money = 10):
        self.agents = []
        self.contact_horizon = contact_horizon
        for id in range(num_agents):
            position = [int(random.random() * 500), int(random.random() * 500)]
            self.agents.append(Agent(id,
                pos=position,
                speed = speed,
                consume_rate = consume_rate,
                money = starting_money,
                max_trades_per_step = max_trades_per_step,
                collection_rate = collection_rate))

        self.dim = dim
        self.terrain = create_grid_world_parallel(dim[0], dim[1])

    def find_within_radius(self, current, remaining):
        """
        Bruteforce implementation because I'm lazy and don't have time atm
        as long as it stays below 1000 agents, seems to perform fine
        TODO benchmark and reimplement
        """
        within = []
        for agent in remaining:
            if agent != current:
                dist = np.linalg.norm(np.array(agent.position) - np.array(current.position))
                if dist < self.contact_horizon:
                    within.append(agent)
        return within

    def calculate_gdp_per_capita(self) -> float:
        gdp = 0
        for agent in self.agents:
            print(agent.age)
            gdp += agent.wealth_food + agent.wealth_minerals + agent.money
        gdp /= len(self.agents)
        return gdp
            
    def step(self):
        for (i, agent)in enumerate(self.agents):
            within_radius = self.find_within_radius(agent, self.agents)
            agent.step(within_radius, self.terrain[agent.position[0]][agent.position[1]], self.dim)
        print(f"Number of agent remaining: {len(self.agents)}")
        gdp_per_cap = self.calculate_gdp_per_capita()
        print(f"GDP per Capita: {gdp_per_cap}")

        print()
        
