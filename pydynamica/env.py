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
        self.num_agents = num_agents
        self.contact_horizon = contact_horizon
        for id in range(num_agents):
            position = [int(random.random() * dim[0]), int(random.random() * dim[1])]
            self.agents.append(Agent(id,
                pos=position,
                speed = speed,
                consume_rate = consume_rate,
                money = starting_money,
                max_trades_per_step = max_trades_per_step,
                collection_rate = collection_rate))

        self.speed = speed
        self.consume_rate = consume_rate
        self.starting_money = starting_money
        self.max_trades_per_step = max_trades_per_step
        self.collection_rate = collection_rate

        self.iters = 0

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
            gdp += agent.wealth_food + agent.wealth_minerals + agent.money
        gdp /= len(self.agents)
        return gdp
            
    def step(self):
        next_gen = []

        avg_age = 0
        avg_food_value = 0
        avg_mineral_value = 0
        max_age = 0

        max_wealth = self.agents[0].money
        min_wealth = self.agents[0].money

        for (i, agent) in enumerate(self.agents):
            within_radius = self.find_within_radius(agent, self.agents)
            death = agent.step(within_radius, self.terrain[agent.position[0]][agent.position[1]], self.dim)

            avg_food_value += agent.internal_food_value
            avg_mineral_value += agent.internal_mineral_value

            if not death:
                avg_age += agent.age
                if agent.age > max_age:
                    max_age = agent.age
                if agent.money > max_wealth:
                    max_wealth = agent.money
                if agent.money < min_wealth:
                    min_wealth = agent.money
                next_gen.append(agent)

        self.agents = next_gen

        for _ in range(self.num_agents - len(self.agents)):
            position = [int(random.random() * self.dim[0]), int(random.random() * self.dim[1])]
            self.agents.append(Agent(0,
                pos=position,
                speed = self.speed,
                consume_rate = self.consume_rate,
                money = self.starting_money,
                max_trades_per_step = self.max_trades_per_step,
                collection_rate = self.collection_rate))

        avg_age /= self.num_agents
        avg_food_value /= self.num_agents
        avg_mineral_value /= self.num_agents

        gdp_per_cap = self.calculate_gdp_per_capita()

        self.iters += 1
        print(f"------------ Step {self.iters} ------------")
        print(f"Number of agent remaining: {len(self.agents)}")
        print(f"Average age of agent: {avg_age}")
        print(f"Age of oldest agent: {max_age}")
        print(f"GDP per Capita: {gdp_per_cap}")
        print(f"Average value of food: {avg_food_value}")
        print(f"Average value of minerals: {avg_mineral_value}")
        print(f"Wealth of wealthiest agent: {max_wealth}" )
        print(f"Wealth of poorest agent: {min_wealth}" )
        print()

        return {"avg_age": avg_age,
                "max_age": max_age,
                "gdp_per_cap": gdp_per_cap,
                "avg_food_value": avg_food_value,
                "avg_mineral_value": avg_mineral_value,
                "max_wealth": max_wealth,
                "min_wealth": min_wealth}
        
