
import Utils as utils
import numpy as np

from SchedulingAlgorithms.DDPG.DDPGCore import DDPGCore as ddpgcore
from SchedulingAlgorithms.DDPG import parameters
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
            print("episode "+str(i))
            s = self.getState(self)
            s_= self.getEndState(self)
            # Add exploration noise
            a = ddpg.choose_action(s)
            a = np.clip(np.random.normal(a, var), *a_bound)    
            a_send= a.reshape((utils.MIN_SCHEDULES, self.ndevices,5))     
            # print(a_send)    
            r,s_ = environment.transmitToGateway(a_send,3)
            # r = self.fakeSimulator(self, a_send, 3)
            print(r)
            ep_reward_list.append(r)
            ddpg.store_transition(s, a, r,s_)  
            if min_r==0 or min_r<r:
                min_r =r
            
            if ddpg.pointer > parameters.MEMORY_CAPACITY:
                ddpg.learn()
            environment = Environment() 
            self.device_list = utils.READY_DEVICES
            
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
    
    def fakeSimulator(self, a_send, noTries):
        import math
        reward =0
        for schedule  in a_send:    
            for device in schedule:
                
                tp = utils.TX_POW[int(device[0] * 14)]
                cf= int(device[1] * 71)
                cr = utils.CR[math.ceil(device[2] * 3)]
                sf = utils.SF[int(device[3] *5)]
                bw = utils.BANDWIDTH[math.ceil(device[4]) ] 
                reward = reward + (tp+cf+cr+sf+bw)*0.01
        return reward
    



    