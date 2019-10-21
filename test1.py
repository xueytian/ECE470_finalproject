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

vrep.simxFinish(-1)

while True:
    clientID = vrep.simxStart('127.0.0.1', 19999, True, True, 5000, 5)
    if clientID > -1:
        break
    else:
        time.sleep(0.2)
        print("Failed connecting to remote API server!")
print("Connection success!")

vrep.simxSetFloatingParameter(clientID, vrep.sim_floatparam_simulation_time_step, tstep, vrep.simx_opmode_oneshot)

vrep.simxSynchronous(clientID, True) 
vrep.simxStartSimulation(clientID, vrep.simx_opmode_oneshot)

# —————————————————————————————————————————————————————————————————


jointHandle = np.zeros((jointNum,), dtype=np.int)
for i in range(jointNum):
    _, returnHandle = vrep.simxGetObjectHandle(clientID, jointName + str(i+1), vrep.simx_opmode_blocking)
    jointHandle[i] = returnHandle

_, baseHandle = vrep.simxGetObjectHandle(clientID, baseName, vrep.simx_opmode_blocking)

print('Handles available!')


jointConfig = np.zeros((jointNum,))
for i in range(jointNum):
     _, jpos = vrep.simxGetJointPosition(clientID, jointHandle[i], vrep.simx_opmode_streaming)
     jointConfig[i] = jpos
lastCmdTime=vrep.simxGetLastCmdTime(clientID)
vrep.simxSynchronousTrigger(clientID)
# 开始仿真
while vrep.simxGetConnectionId(clientID) != -1:
    currCmdTime=vrep.simxGetLastCmdTime(clientID)
    dt = currCmdTime - lastCmdTime


    for i in range(jointNum):
        _, jpos = vrep.simxGetJointPosition(clientID, jointHandle[i], vrep.simx_opmode_buffer)
        # print(round(jpos * RAD2DEG, 2))
        jointConfig[i] = jpos


    vrep.simxPauseCommunication(clientID, True)
    for i in range(jointNum):
        vrep.simxSetJointTargetPosition(clientID, jointHandle[i], 120/RAD2DEG, vrep.simx_opmode_oneshot)
    vrep.simxPauseCommunication(clientID, False)
    lastCmdTime=currCmdTime
    vrep.simxSynchronousTrigger(clientID)
    vrep.simxGetPingTime(clientID)