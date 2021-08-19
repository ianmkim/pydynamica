# PyDynamica
PyDynamica is a pure python implementation of Sociodynamica, a virtual environment to simulate a simple economy with minimal dependencies.


# Installation
`
pip3 install -r requirements.txt
`

`
python3 visualizer.py or python3 run_cli.py
`

## Visualizer
<img src="https://github.com/parvusvox/pydynamica/blob/master/docs/stats1.png?raw=true" width="100%">
<img src="https://github.com/parvusvox/pydynamica/blob/master/docs/stats2.png?raw=true" width="100%">

## How good of a model is this?
Not very. But even so, we can still learn a lot from this simple model, testing different economic hypotheses. A full economic analysis is coming soon.

It's easy to think of each agent as a "person" but really, it's more accurate to think of them as corporations. Here's why...

# How does it work?
Sociodynamica is a freely available agent-based simulation model.

### Resources
The grid world is filled with resources of three kinds: food, minerals, and empty. Each grid also keeps track of resource abundance.

Resources are generated by first creating three individual grids representing the abundance of each resource using perlin noise. At each grid, we choose the resource with highest abundance since each cell can only have one resource.

Minerals are a limited resource and therefore cannot regenerate. However, food regenerates at a constant rate.

### Agent
There are four types of agents: omnipotent, trader, farmer, and miner. A miner can only mine minerals and trade with the trader. A farmer can only gather food and trade with the trader. A trader can trade with anybody. An omnipotent agent can, as the name implies, perform every action.

At the start of each turn, the agents move according to brownian motion except when they encounter an edge. After they move, they are given a chance to look for someone to trade with under the max trade per step contraint. An agent may choose who to trade with randomly as long as they are within the "contact horizon." Contact horizon represents how integrated an economy is.

The agents then collect resources if they are standing on a tile with resources they can collect. They then consume resources at a constant rate and adjust the internal value of each commodity.

The internal value represents how much an agent is willing to sell/buy a product for. The average sum of the internal value of all agents represents the "true market value" of products.

If the agent run out of food the agent dies. There is also a random chance that an agent may die (to simulate natural disasters, accidents, disease, etc). An agent can decrease the chance of this random death by accumulating minerals. Sudden death is determined through mineral_wealth < random[0,1] * danger. 

### Bartering / Trading mechanism
Each agent has a risk property which determines how much of their stockpile they want to sell off at each timestep. The amount to purchase is determined by the minimum of either the maximum amount the trading partner wants to sell or the amount of money the agent currently has.

If the agent values a resource more than its tradnig partner, a purchase will be made accordingly.

After each trading period comes a value adjustment period. If the resources sold in the previous trading round is less than the minerals the agent wanted to sell, the agent will decrease it's internal perceived value of that resource by a certain percentage. Otherwise, it will increase its internal perceived value.

### Environment
An environment is defined by its terrestrial dimensions as well as the number of agents. Unlike other simulators which imbue agents with genetics and heredity, PyDynamica chooses to randomly generate agents at each step to replace dead agents.

This is more like how corporations work in free market capitalism. New companies don't inherit properties of the fallen ones (for the most part). In fact, people don't even try to replicate behaviors of successful companies (for the most part). 

### Statistics
The provided visualizer can show a couple interesting statistics about the economy: 
 - GDP per capita: the sum of wealth of all agents divided by the number of agents.
 - Avg internal values: Price of food and price of minerals
 - Resources: the wealth of the richest agent and the wealth of the poorest agent and the wealth disparity

### Todo
 - [x] Mineral efficiency increase (innovation in capitalism)
 - [x] More statistics about wealth disparities and the top 10% (See if bernie is right)
 - [x] Implement "innovation" (increase extraction efficienties and extraction difficulties)
 - [ ] Implement replenishing resources
 - [ ] Make visualizer pretty
 - [ ] Implement Stalin
 - [ ] Implement income tax & wealth tax at different rates
 

### Bugs & Qs
Feel free to report bugs and issues on github. Also feel free to email me at ian@ianmkim.com 
 

