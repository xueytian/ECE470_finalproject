# -*- coding: utf-8 -*-
"""
Created on Sun Oct 13 15:05:17 2019

@author: xueyt
"""
from __future__ import division
import numpy as np
import math
import vrep
import time

RAD2DEG = 180 / math.pi   
tstep = 0.005            
jointNum = 6
baseName = 'Jaco'
jointName = 'Jaco_joint'

print('Program started')
# 关闭潜在的连接
vrep.simxFinish(-1)
# 每隔0.2s检测一次，直到连接上V-rep
while True:
    clientID = vrep.simxStart('127.0.0.1', 19999, True, True, 5000, 5)
    if clientID > -1:
        break
    else:
        time.sleep(0.2)
        print("Failed connecting to remote API server!")
print("Connection success!")
# 设置仿真步长，为了保持API端与V-rep端相同步长
vrep.simxSetFloatingParameter(clientID, vrep.sim_floatparam_simulation_time_step, tstep, vrep.simx_opmode_oneshot)
# 然后打开同步模式
vrep.simxSynchronous(clientID, True) 
vrep.simxStartSimulation(clientID, vrep.simx_opmode_oneshot)

# —————————————————————————————————————————————————————————————————

# 然后读取Base和Joint的句柄
jointHandle = np.zeros((jointNum,), dtype=np.int) # 注意是整型
for i in range(jointNum):
    _, returnHandle = vrep.simxGetObjectHandle(clientID, jointName + str(i+1), vrep.simx_opmode_blocking)
    jointHandle[i] = returnHandle

_, baseHandle = vrep.simxGetObjectHandle(clientID, baseName, vrep.simx_opmode_blocking)

print('Handles available!')

# 然后首次读取关节的初始值，以streaming的形式
jointConfig = np.zeros((jointNum,))
for i in range(jointNum):
     _, jpos = vrep.simxGetJointPosition(clientID, jointHandle[i], vrep.simx_opmode_streaming)
     jointConfig[i] = jpos
lastCmdTime=vrep.simxGetLastCmdTime(clientID)  # 记录当前时间
vrep.simxSynchronousTrigger(clientID)  # 让仿真走一步
# 开始仿真
while vrep.simxGetConnectionId(clientID) != -1:
    currCmdTime=vrep.simxGetLastCmdTime(clientID)  # 记录当前时间
    dt = currCmdTime - lastCmdTime # 记录时间间隔，用于控制

            # 读取当前的状态值，之后都用buffer形式读取
    for i in range(jointNum):
        _, jpos = vrep.simxGetJointPosition(clientID, jointHandle[i], vrep.simx_opmode_buffer)
        # print(round(jpos * RAD2DEG, 2))
        jointConfig[i] = jpos

        # 控制命令需要同时方式，故暂停通信，用于存储所有控制命令一起发送
    vrep.simxPauseCommunication(clientID, True)
    for i in range(jointNum):
        vrep.simxSetJointTargetPosition(clientID, jointHandle[i], 120/RAD2DEG, vrep.simx_opmode_oneshot)
    vrep.simxPauseCommunication(clientID, False)
    lastCmdTime=currCmdTime    # 记录当前时间
    vrep.simxSynchronousTrigger(clientID)  # 进行下一步
    vrep.simxGetPingTime(clientID)    # 使得该仿真步走完