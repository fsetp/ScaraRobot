
import ScaraRobotLib
from ScaraRobotLib import ScaraRobot

import time



x		= 0
y		= 0
z		= 0
yaw		= 0
grip	= 0
ms		= 100

scara = ScaraRobot()
scara.Initialize()

scara.SetPos(ScaraRobotLib.POS_X,		x)
scara.SetPos(ScaraRobotLib.POS_Y,		y)
scara.SetPos(ScaraRobotLib.POS_Z,		z)
scara.SetPos(ScaraRobotLib.POS_YAW,		yaw)
scara.SetPos(ScaraRobotLib.POS_GRIP,	grip)

scara.SetDir(ScaraRobotLib.DIR_CW)

scara.TorqueControl(True)


scara.Move(ms)
time.sleep(1)

scara.TorqueControl(False)
