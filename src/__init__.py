import Utils as utils

if utils.ALGO_NAME == "DDPG":
    from SchedulingAlgorithms.DDPG import LoRaDDPG as loraddpg
    loraddpg.LoRaDDPGScheduler.DDPGSchedule(loraddpg.LoRaDDPGScheduler)
if utils.ALGO_NAME == "Random":
    from SchedulingAlgorithms.Random import RandomScheduling as random
    random.RandomScheduling.RandomSchedule(random.RandomScheduling)
    

