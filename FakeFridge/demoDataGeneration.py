
from random import randint,uniform
from time import sleep
from datetime import datetime
import numpy as np


DATA_PATH = "../TestData"

def genDataLine_T(value,i):
    contents = []#["01-01-21"]#,"11:50:35"] #format: "01-01-21,11:50:35,2.880740E+2"
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    current_date = now.strftime("%d-%m-%y")
    contents.append(current_date)
    contents.append(current_time)
    value = 0.01 + np.sin(value/10)*0.0025 + 0.005 * i**2
    value += 0.015 * value/20
    value += np.random.normal(0,0.0005,1)[0]
    
    contents.append(str(value))
    return ",".join(contents)+"\n"

def genDataLine_P(value,i):
    contents = []#["01-01-21"]#,"11:50:35"] #format: "01-01-21,11:50:35,2.880740E+2"
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    current_date = now.strftime("%d-%m-%y")
    contents.append(current_date)
    contents.append(current_time)
    value = 10.54e-9 + np.sin(value/10)*10.54e-9/2
    value += 10.54e-9 * value/50
    value += np.random.normal(0,10.54e-9 / 20,1)[0]
    
    contents.append(str(value))
    return ",".join(contents)+"\n"

def launchFridge():
    t = 0
    while True:
        t+=1.5
        sleep(3) # Sleep a random number of seconds (between 1 and 5)
        for i in range(4):
            T_data=genDataLine_T(t + i*10,i)
            P_data=genDataLine_P(t/(i+1) + i*542,i)
            print("Generated lines:" + T_data + " and " + P_data)
            f_T=open(DATA_PATH+"/21-01-01/demo_T T" + str(i) + " date.txt","a")
            f_T.write(T_data)
            f_T.close()
            f_P=open(DATA_PATH+"/21-01-01/demo_P P" + str(i) + " date.txt","a")
            f_P.write(P_data)
            f_P.close()
        
if __name__ == "__main__":
    print("Starting fake fridge")
    launchFridge()
