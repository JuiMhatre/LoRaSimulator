from  Utils.TransmissionParameters import TransmissionParameter as trans_params
import Utils as utils
import random
class Scheduler:
    def __init__(self):
        pass
    def inputToScheduler(self,devlist_ready_to_transmit):
        self.devlist=devlist_ready_to_transmit
        pass
    def sendtransmissionschedule(self):
        self.dev_wise_params={}
        self.RL_SchedulerDemo(self)
        return self.dev_wise_params, self.noOfRetry 
    
    def RL_SchedulerDemo(self):
        for dev in self.devlist:
            tp = utils.TX_POW[random.randint(0,14)]
            bw = utils.BANDWIDTH[random.randint(0,1)]
            sf = utils.SF[random.randint(0,5)]
            cr = utils.CR[random.randint(0,3)]
            cf= random.randint(0,71)
            self.dev_wise_params[dev]= trans_params(tp,cf,cr,sf,bw) #get from algorithm
        self.noOfRetry=3