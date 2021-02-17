import socket
import time 
from threading import Thread, Event
import matplotlib.pyplot as plt
import numpy as np
import time
event = Event()

def printingFunc(xs_prim,ys_prim,zs_prim,gyroZ,currAngle,lastReceiveTime):
    while True:
        # fig.canvas.draw()
        # fig.clf()
        # plt.plot(xs_prim)
        R=10
        fig.canvas.draw()
        fig.clf()
        if(len(gyroZ)>1):
            currAngle+=gyroZ[-1]
            x_pos=R*np.cos(currAngle)
            y_pos=R*np.sin(currAngle)
            allXs=np.arange(-30,30,1)
            allYs=np.arange(-30,30,1)
            plt.plot(allXs,allYs)
            plt.plot([0,x_pos],[0,y_pos])


    
def serverFunc(xs,ys,zs,gyroZ,lastReceiveTime):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('192.168.0.187', 65432 ))
    s.listen(0)                 

    print('server started')
    counter=0
    gyroMean=0
    while True:
        client, addr = s.accept()
        client.settimeout(50)
        if(client and counter !=1):
            print('client connected')
            counter=1
        while True:
            content = client.recv(2024)
            if len(content) ==0:
                break
            if str(content,'utf-8') == '\r\n':
                continue
            else:
                mystr=str(content,'utf-8')
                mystr=mystr.replace('\r',' ')
                mystr=mystr.replace('Acceleration',' ')
                mystr=mystr.replace('Rotation',' ')
                mystr=mystr.replace('Temperature',' ')
                splited=mystr.split(' ')
                splited = [a for a in splited if a!='']
                print(splited)
                xs.append(float(splited[1]))
                
                if abs(float(splited[5]))>0.05 and lastReceiveTime!=0:
                    dt=time.time_ns()/10**9-lastReceiveTime
                    gyroZ.append(float(splited[5])*dt)
                else:
                    gyroZ.append(0)
                gyroMean=np.mean(gyroZ)
                lastReceiveTime=time.time_ns()/10**9
                # ys.append(float(splited[2]))
                # zs.append(float(splited[3]))
                if len(xs)>100:
                    xs.pop(0)
                    gyroZ.pop(0)
                client.send(b'Hello From Python')
                event.set()
        client.close()
xs = []
ys = []
zs = []
gyroZ=[]
currAngle=0
lastReceiveTime=0
fig = plt.figure()
ax = fig.add_subplot(111)
line1, = ax.plot(xs) # Returns a tuple of line objects, thus the comma
plt.xlim(-10, 10)
plt.ylim(-10, 10)
serv = Thread(target=serverFunc, args=(xs,ys,zs,gyroZ,lastReceiveTime, ))
printi = Thread(target=printingFunc, args=(xs,ys,zs,gyroZ,currAngle,lastReceiveTime, ))
serv.start()
printi.start()


# Don't mess with the limits!
plt.autoscale(False)
plt.show()