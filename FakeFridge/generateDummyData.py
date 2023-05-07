
from random import randint,uniform
from time import sleep
from datetime import datetime


DATA_PATH = "../TestData"

def genDataLine():
    contents = []#["01-01-21"]#,"11:50:35"] #format: "01-01-21,11:50:35,2.880740E+2"
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    current_date = now.strftime("%d-%m-%y")
    contents.append(current_date)
    contents.append(current_time)
    contents.append(str(uniform(-3.6,5.8)))
    return ",".join(contents)+"\n"
def launchFridge():
    while True:
        sleep(randint(1,5)) # Sleep a random number of seconds (between 1 and 5)
        data=""
        for i in range(randint(1,5)):#generate random number of line
            data+=genDataLine()
        print("Generated lines:")
        print(data)
        f=open(DATA_PATH+"/21-01-01/generated.txt","a")
        f.write(data)
        f.close()
        
if __name__ == "__main__":
    print("Starting fake fridge")
    launchFridge()
