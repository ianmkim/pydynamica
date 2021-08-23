from pydynamica.env import Env
from pydynamica.utils import log

class TaxedEnv(Env):
    def __init__(self, 
            num_agents=100, 
            dim = (100, 100),
            taxation_rate=0.2):
        self.taxation_rate = taxation_rate
        super().__init__(num_agents = num_agents, dim=dim)

    def step(self):
        sorted_agents = sorted(self.agents, key=lambda a:a.money)
        top_percentile = int(len(self.agents) * 0.25)

        wealth_collected = 0
        
        for agent in sorted_agents[-top_percentile:]:
            amount = agent.money * self.taxation_rate
            wealth_collected += amount
            agent.money -= amount

        bottom_agents = sorted_agents[:top_percentile]
        amount_individual = wealth_collected/(len(bottom_agents))
        for agent in bottom_agents:
            agent.money += amount_individual

        log(f"Total Wealth Taxed: {wealth_collected}")

        return super().step()
            
