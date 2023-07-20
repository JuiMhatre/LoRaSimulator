from Environment.Envsetup import Environment
import numpy as np
import Utils as utils
import random

class RandomScheduling:
    def __init__(self):
        pass
    def RandomSchedule(self):
        environment = Environment()  
        schedule = np.zeros((utils.MIN_SCHEDULES, utils.nDevices, 5))
        for time_slot in range(utils.MIN_SCHEDULES):
            for device in range(utils.nDevices):
                schedule[time_slot][device][0] = random.random()
                schedule[time_slot][device][4] = random.random()
                schedule[time_slot][device][3] = random.random()
                schedule[time_slot][device][2] = random.random() 
                schedule[time_slot][device][1]= random.random()
        # print(schedule)
        environment.transmitToGateway(schedule,3)