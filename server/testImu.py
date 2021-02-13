import matplotlib.pyplot as plt

def readFromFile():
    f = open("Sample9DoF_R_Session1_Shimmer_B663_Calibrated_SD.csv", "r")
    accelerationsX=[]
    accelerationsY=[]
    dates=[]
    for idx,line in enumerate(f):
        if idx>2:
            splited=line.split('\t')
            date=splited[0]
            accX=splited[1]
            accY=splited[2]
            accZ=splited[3]
            accelerationsX.append(float(accX))
            accelerationsY.append(float(accY))
            dates.append(date)
    return dates,accelerationsX,accelerationsY
def calcRoad(v0,acc,dt):
    s=v0*dt+(acc*dt**2)/2
    v_new=v0+dt*acc
    return v_new,s
def createPositions(dates,xs,ys):
    x0=0
    y0=0
    v0_x=0
    v0_y=0
    dt=0.002 #seconds
    positionsX=[]
    positionsY=[]
    for accX,accY in zip(xs,ys):
        #for X
        v0_x,roadX=calcRoad(v0_x,accX,dt)
        newPositionX=x0+roadX
        x0=newPositionX
        positionsX.append(x0)
        #for Y
        v0_y,roadY=calcRoad(v0_y,accY,dt)
        newPositionY=y0+roadY
        y0=newPositionY
        positionsY.append(y0)
    return positionsX,positionsY
ds,xs,ys=readFromFile()
posX,posY=createPositions(ds,xs,ys)
plt.plot(posX,posY)
plt.scatter(posX[0],posY[0],color=['red'])
plt.scatter(posX[-1],posY[-1],color=['green'])
plt.show()

