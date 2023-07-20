import Utils as utils
import time
timestart = time.time()
if utils.ALGO_NAME == "DDPG":
    from SchedulingAlgorithms.DDPG import LoRaDDPG as loraddpg
    loraddpg.LoRaDDPGScheduler.DDPGSchedule(loraddpg.LoRaDDPGScheduler)
if utils.ALGO_NAME == "DDPG_UPDT":
    from SchedulingAlgorithms.DDPG_UPDT import LoRaDDPG as loraddpg_updt
    loraddpg_updt.LoRaDDPGScheduler.DDPGSchedule(loraddpg_updt.LoRaDDPGScheduler)
if utils.ALGO_NAME == "Random":
    from SchedulingAlgorithms.Random import RandomScheduling as random
    random.RandomScheduling.RandomSchedule(random.RandomScheduling)
if utils.ALGO_NAME == "DQN":
    from SchedulingAlgorithms.DQN import DQN as loradqn
    loradqn.DQNScheduler.schedule(loradqn.DQNScheduler)
    # loraddpg.LoRaDDPGScheduler.DDPGSchedule(loraddpg.LoRaDDPGScheduler)
    
print("Total time: "+str(time.time()- timestart))
    

