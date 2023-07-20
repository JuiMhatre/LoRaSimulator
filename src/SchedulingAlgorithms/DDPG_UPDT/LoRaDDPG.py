
import Utils as utils
import numpy as np
import time
from SchedulingAlgorithms.DDPG_UPDT.DDPGCore import DDPGCore as ddpgcore
from SchedulingAlgorithms.DDPG_UPDT import parameters
from Environment.Envsetup import Environment
import matplotlib.pyplot as plt
class LoRaDDPGScheduler():
    def __init__(self):
        pass
    def DDPGSchedule(self):
        environment = Environment()      
        self.device_list = utils.READY_DEVICES
        self.ndevices = len(self.device_list)
        s = self.getState(self)
        a_dim = utils.MIN_SCHEDULES * self.ndevices* 5 #
        a_bound = [0,1]
        s_dim = len(s)
        
        ddpg=ddpgcore(a_dim, s_dim, a_bound)
        var = 1  # control exploration
        # var = 0.01  # control exploration
        min_r =0
        ep_reward_list=[]
        for i in range(parameters.MAX_EPISODES):
            epi_start_time = time.time()
            print("episode "+str(i))
            s = self.getState(self)
            s_= self.getEndState(self)
            # Add exploration noise
            a = ddpg.choose_action(s) 
            a_send = a.reshape(5,(utils.MIN_SCHEDULES*self.ndevices))  
            a_send = np.transpose(a_send)
            a_send= a_send.reshape((utils.MIN_SCHEDULES, self.ndevices,5))     
               
            r,s_ = environment.transmitToGateway(a_send,30)
            ep_reward_list.append(r)
            ddpg.store_transition(s, a, r,s_)  
            if min_r==0 or min_r<r:
                min_r =r
            print("Reward is "+str(r))
            if ddpg.pointer > parameters.MEMORY_CAPACITY:
                ddpg.learn()
            environment = Environment() 
            self.device_list = utils.READY_DEVICES
            print("This episode ended in ", (time.time()-epi_start_time))
           

        plt.plot(ep_reward_list)
        plt.xlabel("Episode")
        plt.ylabel("Reward")
        plt.show()
            

        
    def getState(self):
        state=np.zeros(0)
        for i in range(self.ndevices):
            state= np.append(state,self.device_list[i].data)
            # devInfor[1]= self.device_list[i].locX
            # devInfor[2]= self.device_list[i].locY
          
        return state

    def getEndState(self):
        state=np.zeros(self.ndevices,dtype=float)
        # for i in range(self.ndevices):
        #     state.append(0)
        return state
    

    



    