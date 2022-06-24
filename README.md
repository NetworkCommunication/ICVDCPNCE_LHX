# ICVDCPNCE_LHX
This code is used to do simulation experiments for vehicle Dew computing architecture. 
# Requirements
Python 3.5+
# How to use
    First, "My_test.py" is the main function file. 
    Second, "xy.tcl" is the vehicle track data. These data are got by using SUMO.
    Third, preparing an excel file as shown in the figure below, in which 1000 pieces of datas are needed to be prepared. The four columns of datas are: id, size, number of requestes and file type.
![image](https://github.com/NetworkCommunication/VDC_LHX/blob/main/fig.jpg?raw=true)
# Installation instructions
        File "Get_Move.py" is used to process the trajectory data of the vehicle.
        File "test.py" is the test file for vehicle clustering.
        File "Update_Cache.py" and "Cache.py" are the files for cache optimization algorithm.
        File "UCB1.py" is the file for Multi-armed bandit algorithm.
        File "Zipf.py" is the file request model.
