from terrain import Resources
import random

class Agent():
    def __init__(self, 
            pos = [0,0],
            speed=10, 
            food_consume_rate=0.1,
            money = 10):
        self.speed = speed
        self.food_consume_rate = food_consume_rate
        self.wealth_food= 0
        self.wealth_minerals = 0

        self.money = money

    def check_death(self):
        if self.wealth_food <= 0 or self.wealth_minerals <= 0:
            return True
        return False

    def move(self) -> list:
        xdir = round(random.random() * 2 - 1)
        ydir = round(random.random() * 2 - 1)
        
        self.position[0] += xdir * self.speed
        self.position[1] += ydir * self.speed

       


