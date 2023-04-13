import math
DWELL_TIME=400 #400ms
BIT_RATE= { #https://www.rfwireless-world.com/calculators/LoRa-Data-Rate-Calculator.html
    125 :{
            7:5470,
            8:3125,
            9:1760,
            10:980
},
    500 :{
        7:21900,
        8:12500,
        9:7000,
        10:3900,
        11:1760,
        12:980
}
}
DEVICE_DATA= 10*1000*8 #10KB in bitss
TIME_SLOT = 10
DEV_SELECTED_SCHEDULE={}
MIN_BIT_RATE= 11 #https://unsigned.io/understanding-lora-parameters/#:~:text=LoRa%20is%20a%20very%20flexible,mere%2011%20bits%20per%20second.
MIN_SCHEDULES = math.ceil(DEVICE_DATA / (MIN_BIT_RATE * TIME_SLOT))
nDevices=700
ALGO_NAME="DDPG"
READY_DEVICES=[]
TX_POW ={ #in dbm
    0:30,
    1:28,
    2:26,
    3:24,
    4:22,
    5:20,
    6:18,
    7:16,
    8:14,
    9:12,
    10:10,
    11:8,
    12:6,
    13:4,
    14:2
}
BANDWIDTH=[125, 500]
SF=[7,8,9,10,11,12]
CR = [1,2,3,4]
GATEWAY_DEVICE_LIMIT=10
NETWORK_AREA_MAX_X =1000
NETWORK_AREA_MAX_Y =1000
NETWORK_AREA_MIN_X =0
NETWORK_AREA_MIN_Y =0
GATEWAY_LOCX=50
GATEWAY_LOCY =40
RECEIVER_NOISE = 6
SNR =-20
SLEEP_CURRENT=1.27 * 10**-6 
TRANSMISSION_CURRENT= 117 * 10**-3
VOLTAGE= 3.0

#RSSI PARAMS
D0 =40.0
GAMMA = 2.08
LPLD0 = 127.41
VARIANCE=2.0


#Results
total_delay=0.0
total_energy=0

IS7 = [1, -8, -9, -9, -9, -9]
IS8 = [-11, 1, -11, -12, -13, -13]
IS9 = [-15, -13, 1, -13, -14, -15]
IS10 =[-19, -18, -17, 1, -17, -18]
IS11 = [-22, -22, -21, -20, 1, -20]
IS12 = [-25, -25, -25, -24, -23, 1]
IsoThresholds = [IS7, IS8, IS9, IS10, IS11, IS12]
OPTIMIZATION_TYPE = "ENERGY"  #{LATENCY, ENERGY, PDR}
