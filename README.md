# LoRaSimulator
LoRa Simulator with CAD functionality

Main features include:
1. Gateway Load: Number of connections supported by gateway are specified in properties file beyond which no load is supported.
2. CAD Repeatitions: Number of times CAD is repeated to check idleness of channel before transmission finally starts.

# Modules

![image](https://github.com/JuiMhatre/LoRaSimulator/assets/43512209/2a58bab3-2c6b-4517-82b3-72830f759c85)

Important modules include:
1. Network Server : Responsible for running the algorithm
2. Gateway: It collects the information for devices and sends to network server as input to algorithm
3. Device: Does transmission

## Important Files
1. src/Utils/__init__.py : Environment Setup parameters
2. src/__init__.py: Specifies how to call the required algorithm


## Links
Related reference and documentations:
https://digitalcommons.kennesaw.edu/cs_etd/59/
