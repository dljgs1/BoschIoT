###调用方法#########
###CSV里面一共有四列数据，依次为 x加速度，y加速度，z加速度, 时间
###把每一列转成一个list,将这4个list作为参数传入到csvDataToCoordinates方法中
###这个方法会返回一个二维数组，没个小数组有三个数字，这三个数字就是x,y,z轴上的坐标距离起始点的距离

from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt


def makePlot(x, y, z):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(x, y, z, c='r', marker='o')

    plt.xlim(-1, 1)
    plt.ylim(-1, 1)

    ax.set_xlabel('X Label')
    ax.set_ylabel('Y Label')
    ax.set_zlabel('Z Label')

    plt.show()


fig = plt.figure()


def make2dplot(x, y, num=331, show=False):
    fig.add_subplot(num)
    plt.plot(y, x)
    if show:
        plt.show()


# Vf = a(Tf-Ti)+Vi
def convertAccelToSpeed(accelList, timeList):
    lastTime = timeList[0]
    lastSpeed = 0
    length = len(accelList)
    resultSpeed = [0] * length
    if len(accelList) == len(timeList):
        for x in range(1, length):
            timeNow = timeList[x]
            currentSpeed = 0.5 * (accelList[x] + accelList[x - 1]) * (timeNow - lastTime) + lastSpeed
            resultSpeed[x] = currentSpeed
            lastTime = timeNow
            lastSpeed = currentSpeed
        return resultSpeed
    else:
        raise Exception("Acceleration and Time data list length not the same! Must be same length")


width = 16
threshod = 0.2


def acce_filter(accelList):
    for i in range(len(accelList)):
        accelList[i] = sum(accelList[i:i + width]) / width
    for i in range(len(accelList)):
        if abs(accelList[i]) < threshod:
            accelList[i] = 0
    return accelList


## distance = 1/2(final_speed+initial_speed)*Time
def convertSpeedToDistance(speedList, timeList):
    lastTime = timeList[0]
    lastSpeed = speedList[0]
    lastPosition = 0
    length = len(speedList)
    resultDisplacement = [0] * length
    if len(speedList) == len(timeList):
        for x in range(1, length):
            v_final = speedList[x]
            currentTime = timeList[x]
            currentPosition = lastPosition + 0.5 * (speedList[x] + speedList[x - 1]) * (currentTime - lastTime)
            resultDisplacement[x] = currentPosition
            lastTime = currentTime
            lastPosition = currentPosition
            lastSpeed = v_final
        return resultDisplacement
    else:
        raise Exception("Speed and Time data list length not the same! Must be same length")


def csvDataToCoordinates(xDirectionList, yDirectionList, zDirectionList, timeList):
    result = []
    length = len(timeList)

    xDirectionList = acce_filter(xDirectionList)
    yDirectionList = acce_filter(yDirectionList)
    zDirectionList = acce_filter(zDirectionList)

    make2dplot(xDirectionList, timeList, 331)
    make2dplot(yDirectionList, timeList, 332)
    make2dplot(zDirectionList, timeList, 333)

    xDirectionList = convertAccelToSpeed(xDirectionList, timeList)
    yDirectionList = convertAccelToSpeed(yDirectionList, timeList)
    zDirectionList = convertAccelToSpeed(zDirectionList, timeList)

    make2dplot(xDirectionList, timeList, 334)
    make2dplot(yDirectionList, timeList, 335)
    make2dplot(zDirectionList, timeList, 336)

    xPositionList = convertSpeedToDistance(xDirectionList, timeList)
    yPositionList = convertSpeedToDistance(yDirectionList, timeList)
    zPositionList = convertSpeedToDistance(zDirectionList, timeList)

    make2dplot(xPositionList, timeList, 337)
    make2dplot(yPositionList, timeList, 338)
    make2dplot(zPositionList, timeList, 339,True)
    # plot_data.makePlot()
    for i in range(0, length):
        three_dimensional = []
        three_dimensional.append(xPositionList[i])
        three_dimensional.append(yPositionList[i])
        three_dimensional.append(zPositionList[i])
        result.append(three_dimensional)
    return result


from vec2img import pts2flatten, pts2image
import numpy as np
import pandas as pd

if __name__ == "__main__":
    data = pd.read_csv("0_4.csv")
    dt = data.get_values()

    c = csvDataToCoordinates(dt[:, 0], dt[:, 1], dt[:, 2], dt[:, 3] / (10 ** 9))
    c = np.array(c)
    makePlot(c[:, 0], c[:, 1], c[:, 2])
    c = pts2flatten(c)
    c = np.array(c)
    pts2image(c)
    make2dplot(c[:, 0], c[:, 1], 111, True)


