from pydynamica.agent import Agent
from pydynamica.terrain import Resources, create_grid_world_parallel
import numpy as np
import random

from pydynamica.utils import log

# default configs
# collection_rate = 2
class Env():
    def __init__(self,
            num_agents =500,
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
        self.terrain, self.abundance = create_grid_world_parallel(dim[0], dim[1])
        self.initial_abundance = self.calculate_abundance()

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

    def calculate_abundance(self) -> float:
        total = sum([sum(row) for row in self.abundance])
        return total 
            
    def step(self):
        next_gen = []

        avg_age = 0
        avg_food_value = 0
        avg_mineral_value = 0
        max_age = 0

        for (i, agent) in enumerate(self.agents):
            agent_x, agent_y= agent.position[0], agent.position[1]
            within_radius = self.find_within_radius(agent, self.agents)
            death, collected = agent.step(within_radius, self.terrain[agent_x][agent_y], self.abundance[agent_x][agent_y], self.dim)
            self.abundance[agent_x][agent_y] -= collected

            avg_food_value += agent.internal_food_value
            avg_mineral_value += agent.internal_mineral_value

            if not death:
                avg_age += agent.age
                if agent.age > max_age:
                    max_age = agent.age
                next_gen.append(agent)

        self.agents = next_gen
        death_rate = ((self.num_agents - len(self.agents))/self.num_agents) * 100
        collection_rate = sum([a.collection_rate for a in self.agents]) / len(self.agents)
        collection_rate_increase = (collection_rate/15 * 100)

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

        sorted_agents = sorted(self.agents, key=lambda a:a.money)
        top_10_pc = int(len(self.agents) * 0.1)
        max_wealth = sum([a.money for a in sorted_agents[-top_10_pc:]]) / top_10_pc
        min_wealth = sum([a.money for a in sorted_agents[:top_10_pc]])  / top_10_pc

        self.iters += 1
        abundance = self.calculate_abundance()
        abundance_increase = (abundance / self.initial_abundance) * 100
        log(f"------------ Step {self.iters} ------------")
        log(f"Number of agent remaining: {len(self.agents)}")
        log(f"Average age of agent: {avg_age}")
        log(f"Age of oldest agent: {max_age}")
        log(f"GDP per Capita: {gdp_per_cap}")
        log(f"Average value of food: {avg_food_value}")
        log(f"Average value of minerals: {avg_mineral_value}")
        log(f"Wealth of wealthiest 10%: {max_wealth}" )
        log(f"Wealth of poorest 10%: {min_wealth}" )
        log(f"Resource abundance: {abundance}")
        log(f"Death rate: {death_rate}%")
        log(f"Average collection rate increase: {collection_rate}")
        log("")

        return {"avg_age": avg_age,
                "max_age": max_age,
                "gdp_per_cap": gdp_per_cap,
                "avg_food_value": avg_food_value,
                "avg_mineral_value": avg_mineral_value,
                "max_wealth": max_wealth,
                "min_wealth": min_wealth,
                "death_rate": death_rate,
                "collection_rate": collection_rate_increase,
                "abundance": abundance_increase}
        
