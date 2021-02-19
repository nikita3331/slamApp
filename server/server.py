import socket
import time 
from threading import Thread, Event
import matplotlib.pyplot as plt
import numpy as np
import time
event = Event()

def printingFunc(xs_prim,ys_prim,zs_prim,gyroZ,currAngle,lastReceiveTime,angles,distances):
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
            plt.plot(angles)
            # plt.plot(distances)
            plt.plot([0,x_pos],[0,y_pos])


    
def serverFunc(xs,ys,zs,gyroZ,lastReceiveTime,angles,distances):
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
            else:
                mystr=str(content,'utf-8',errors='replace')
                mystr=mystr.replace('\r',' ')
                mystr=mystr.replace('Acceleration',' ')
                mystr=mystr.replace('Rotation',' ')
                mystr=mystr.replace('Temperature',' ')
                manyArrs=mystr.split('\n')
                for arr in manyArrs:
                    if len(arr)>0:
                        splited=arr.split(' ')
                        splited = [a for a in splited if a!='']
                        if len(splited)>7:
                            print(splited)
                            xs.append(float(splited[1]))
                            # angles.append(float(splited[7]))                    
                            try:
                                angles.append(float(splited[7]))                    
                            except ValueError:
                                if len(angles)>0:
                                    angles.append(angles[-1])
                                else:    
                                    print("err")
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
                    angles.pop(0)
                    xs.pop(0)
                    gyroZ.pop(0)
                # client.send(b'Hello From Python')
                event.set()
        client.close()
xs = []
ys = []
zs = []
angles=[]
distances=[]
gyroZ=[]
currAngle=0
lastReceiveTime=0
fig = plt.figure()
ax = fig.add_subplot(111)
line1, = ax.plot(xs) # Returns a tuple of line objects, thus the comma
plt.xlim(-10, 10)
plt.ylim(-10, 10)
serv = Thread(target=serverFunc, args=(xs,ys,zs,gyroZ,lastReceiveTime,angles,distances, ))
printi = Thread(target=printingFunc, args=(xs,ys,zs,gyroZ,currAngle,lastReceiveTime,angles,distances, ))
serv.start()
printi.start()


# Don't mess with the limits!
plt.autoscale(False)
plt.show()