import threading
import time
import Utils as utils
import math
exitFlag = 0

class Transmission (threading.Thread):
    def __init__(self, threadId,device):
      threading.Thread.__init__(self)
      self.threadID = threadId
      self.device = device
      
    def prepareTransmission(self):
    #    print("preparing transmission......")
       if self.device.data > 0:
           used_up_channel = self.device.used_channels.get(self.device.channel.startfreq, 0)
           if used_up_channel < utils.DWELL_TIME:
                remaining_dwell_time = utils.DWELL_TIME - used_up_channel
                if remaining_dwell_time > self.device.time_slot:
                    time_to_transmit = self.device.time_slot
                else:
                    time_to_transmit = remaining_dwell_time
                if not self.checkPathLoss():
                    if self.CADRetry(self.device.CadRetry): #channel sensing
                        if self.checkCaptureEffect():
                            data_sent = self.getBitRate() * time_to_transmit
                            if data_sent > self.device.data:
                                data_sent = self.device.data
                            # print("data sent  by device "+str(self.device.deviceid)+" is :"+str(data_sent)+"having data "+str(self.device.data))
                            self.device.data = self.device.data - data_sent
                            # time.sleep(time_to_transmit)
                            self.device.energy = self.device.energy + (time_to_transmit * utils.TRANSMISSION_CURRENT * utils.VOLTAGE)
                            self.device.used_channels[self.device.channel.startfreq] = used_up_channel + time_to_transmit
                            self.resetCAD()
                            return 1 , True
                        else:
                            return 2 , False   
                    else:
                        return 5 ,False               
                else:
                    # print("Cannot transmit since RSSI < SENSITIVITY !!")
                    return 3, False               
           else:
               return 4, False
       else:
           return 1, True
    def getBitRate(self):
        #https://www.rfwireless-world.com/calculators/LoRa-Data-Rate-Calculator.html
        SF = self.device.trans_params.SF
        BW = self.device.trans_params.BW
        CR = self.device.trans_params.CR
        return SF * ((4/(4+CR))/(2**SF/BW))* 1000      
    def checkCaptureEffect(self): #CAD is not fully reliable, hence add capture effect https://www.mdpi.com/1424-8220/21/3/825
        for otherdevices in self.device.channel.devices_using_me:
            if self.checkBW_SF(otherdevices, self.device) and otherdevices.deviceid != self.device.deviceid :                
                if otherdevices.getRSSI() > self.device.getRSSI():
                    print("Other Already Transmitting device "+str(otherdevices.deviceid)+" has higher strength and that your device "+ str(self.device.deviceid))
                    return False
                if abs(otherdevices.getRSSI() - self.device.getRSSI()) < utils.IsoThresholds[otherdevices.trans_params.SF -7][self.device.trans_params.SF-7]:
                    return False
        return True
        
    def checkBW_SF(self, dev1, dev2):
        return (dev1.trans_params.BW == dev2.trans_params.BW and dev1.trans_params.SF == dev2.trans_params.SF)
        
    def checkPathLoss(self): #https://www.techplayon.com/lora-link-budget-sensitivity-calculations-example-explained/
        self.sensitivity = -174 +10 * math.log(self.device.trans_params.BW) + utils.RECEIVER_NOISE +utils.SNR
        return self.device.rssi < self.sensitivity #True : packet lost
        
    def getLinkBudget(self):
        return self.device.trans_params.TP - self.sensitivity
    
    def CADRetry(self, noOfRetry):
        cad_status_free = False
        while noOfRetry>0 and not cad_status_free:
            cad_status_free = self.CADOperation()
            noOfRetry -=1  
        return cad_status_free
    
    def CADOperation(self): #https://lora-developers.semtech.com/documentation/tech-papers-and-guides/channel-activity-detection-ensuring-your-lora-packets-are-sent/how-to-ensure-your-lora-packets-are-sent-properly/
        inoperableTime = (32.0/self.device.trans_params.BW) * 10**-3; #milliseconds
        # time.sleep(inoperableTime)
        self.device.energy = self.device.energy + (inoperableTime * utils.SLEEP_CURRENT * utils.VOLTAGE)
        cad_status_free = self.CADModeReady()
        self.CADProcess(cad_status_free)
        return cad_status_free

    def CADModeReady(self):
        valid_rssi_time = self.device.trans_params.getTsym()/10**3
        # time.sleep(valid_rssi_time)
        self.device.energy = self.device.energy + (valid_rssi_time * utils.SLEEP_CURRENT * utils.VOLTAGE)
        return not self.device.channel.taken
    
    def CADProcess(self, cad_status_free):
        process_time = self.device.trans_params.getTsym()/(175 * 10**6)
        # time.sleep(process_time)
        self.device.energy = self.device.energy + (process_time * utils.SLEEP_CURRENT * utils.VOLTAGE)
        self.device.CadDone=True
        self.device.CadDetected=cad_status_free
        if cad_status_free:
            self.device.channel.taken = cad_status_free

    def resetCAD(self):
        self.device.channel.taken=False
        self.device.CadDone=False
        self.device.CadDetected=False
        # print(str(self.device.deviceid)+" ", self.device.channel.devices_using_me," ",self.device)
        self.device.channel.devices_using_me.remove(self.device)

    def run(self):
        self.startTransmission()
        
    def startTransmission(self):
        timestart = time.time()
        print ("Transmitting Device.... " + str(self.threadID))
                
        returncode, transmitted_status = self.prepareTransmission()
        timeend= time.time()
        self.device.time_taken =self.device.time_taken + (timeend-timestart)
        if returncode !=4:
            utils.total_energy+=self.device.energy
            self.device.energy=0
            utils.total_delay+=self.device.time_taken
            self.device.time_taken=0
        if transmitted_status:
            utils.READY_DEVICES.remove(self.device)            
            if self.device.data >0:
                utils.READY_DEVICES.append(self.device)
            else:
                print ("Ending Transmission of device " + str(self.threadID))
                pass
        elif returncode ==2:
            print("Failed Transmission of device " + str(self.threadID) +" due to capture Effect")
        elif returncode ==3:
            print("Failed Transmission of device " + str(self.threadID) +" due to RSSI < SENSITIVITY !!")
        elif returncode ==4:
            print("Failed Transmission of device " + str(self.threadID) +" New Channel Required")
        elif returncode ==5:
            print("Failed Transmission of device " + str(self.threadID) +" Out of CAD Retries.")
