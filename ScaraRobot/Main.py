################################################################################
# Scara Robot Control
#
#	F.S.Enterprise
#
#	History
#		Rev 1.0:2023.08.19
#		Rev	1.1:2023.08.25
#

########################################
#
#		LT(6)							RT(7)
#		LB(4)							RB(5)
#
#		UP			BACK(8)	START(9)	Y(1)
#	LEFT	RIGHT					X(0)	B(2)
#		DOWN							A(3)
#
#		ANALOG LEFT				ANALOG RIGHT
#			H(X) V(Y)			H(G) V(Z)
#
#			LEFT				RIGHT
#			BUTTON(10)			BUTTON(11)
#
#	Play	select open teaching file and do action
#	Back	select save teaching file
#	A		none
#	B		save teaching point
#	X		none
#	Y		none
#
#	LB		none
#	LT		none
#	RB		none
#	RT		none
#
#	HAT UP		Torque on / off
#	HAT DOWN	CW/CCW
#	HAT LEFT	Yaw ccw
#	HAT RIGHT	Yaw cw
#
import GamePadLib
from GamePadLib import GamePad
import ScaraRobotLib
from ScaraRobotLib import ScaraRobot
import TeachingLib
from TeachingLib import Teaching
import time

########################################
#
class ScaraRobotConntrol():

	####################################
	# Constoructor
	#
	def __init__(self):
		self.InitializeParameters()

	####################################
	# Parameter Initializer
	#
	def InitializeParameters(self):

		self.pad         = None
		self.scara       = None
		self.teaching    = None
		self.torque      = False

		self.maxX        = 100
		self.minX        = -100
		self.maxY        = 100
		self.minY        = -100
		self.maxZ        = 35
		self.minZ        = -33
		self.maxYaw      = 150
		self.minYaw      = -150
		self.maxGrip     = 30
		self.minGrip     = 10

		self.x           = 0
		self.y           = 0
		self.z           = 0
		self.yaw         = 0
		self.grip        = self.maxGrip
		self.hatStep     = 1

		self.maxHatStep  = 10
		self.moveMs      = 100
		self.dirCW       = True
		self.initMoveMs  = 2000
		self.absAxis     = False

	####################################
	# Parameter Initializer
	#
	def Initialize(self):
		####################################
		#
		self.pad = GamePad()
		print('Initializing Game Pad ...')
		print('')
		ret, text = self.pad.Initialize()
		if ret == False:
			print(text)
			print('Error occured, check the device.')
			return ret

		self.scara = ScaraRobot()
		print('Initializing Game Pad ...')
		print('')
		ret, text = self.scara.Initialize()
		if ret == False:
			print(text)
			print('Error occured, check the device.')
			return ret

		####################################
		# Initilize Succeeded ?
		#
		print('Initialize Succeeded.')

		################################
		#
		self.pad.SetButtonCallback(self.ButtonCallback)
		self.pad.SetAxisCallback(self.AxisCallback)
		self.pad.SetHatCallback(self.HatCallback)

		self.scara.SetPos(ScaraRobotLib.POS_X, self.x)
		self.scara.SetPos(ScaraRobotLib.POS_Y, self.y)
		self.scara.SetPos(ScaraRobotLib.POS_Z, self.z)
		self.scara.SetPos(ScaraRobotLib.POS_YAW, self.yaw)
		self.scara.SetPos(ScaraRobotLib.POS_GRIP, self.grip)
		self.scara.SetDir(ScaraRobotLib.DIR_CW)

		self.pad.AxisRepeatEnable(False)
		self.SetAxisAbs(True)

#		self.pad.AxisRepeatEnable(True)
#		self.SetAxisAbs(False)

		################################
		#
		self.teaching = Teaching()

		return ret

	####################################
	#
	def SetAxisAbs(self, abs):
		self.absAxis = abs

	####################################
	#
	def Run(self):
		################################
		#
		while True:
			self.pad.Idle()
			if self.pad.IsButtonPressed(GamePadLib.BT_LB) == True \
					and self.pad.IsButtonPressed(GamePadLib.BT_RB) == True \
					and self.pad.IsButtonPressed(GamePadLib.BT_LT) == True \
					and self.pad.IsButtonPressed(GamePadLib.BT_RB) == True:
				print('Quit.')
				break

	####################################
	# Joystick Button Callback
	#
	#	button	button index
	#	on		bool True:on / False:off
	#
	def ButtonCallback(self, button, on):

		###############################
		# PLAY button - Torque On / Off
		#
		if button == GamePadLib.BT_START and on == 1:
			print('Select Open Teaching File')
			if self.teaching.SelectOpenTeachingFile() == True:
				self.teaching.LoadActionList()
				num = self.teaching.GetEnumAction()
				print('num : ', num)
				for i in range(num):
					if self.teaching.GetType(i) == 'move':
						x, y, z, yaw, grip, ms = self.teaching.GetPositions(i)
						print('num : ', i, ' x:' , x, ' y:', y, ' z: ', z, ' yaw: ', yaw, ' grip:', grip, ' ms:', ms)
					self.x    = x
					self.y    = y
					self.z    = z
					self.yaw  = yaw
					self.grip = grip
					self.scara.SetPos(ScaraRobotLib.POS_X, self.x)
					self.scara.SetPos(ScaraRobotLib.POS_Y, self.y)
					self.scara.SetPos(ScaraRobotLib.POS_Z, self.z)
					self.scara.SetPos(ScaraRobotLib.POS_YAW, self.yaw)
					self.scara.SetPos(ScaraRobotLib.POS_GRIP, self.grip)
					self.scara.Move(ms)
					time.sleep(ms / 1000)

				print('Done.')

		###############################
		# Back Button
		#
		elif button == GamePadLib.BT_BACK and on == 1:
			print('Select Save Teaching File')
			self.teaching.SelectSaveTeachingFile()

		###############################
		# A button - switch direction CW / CCW
		#
		elif button == GamePadLib.BT_A and on == 1:
			pass

		###############################
		#
		elif button == GamePadLib.BT_B and on == 1:
			self.teaching.AddPosition(	self.scara.GetPos(ScaraRobotLib.POS_X),
										self.scara.GetPos(ScaraRobotLib.POS_Y),
										self.scara.GetPos(ScaraRobotLib.POS_Z),
										self.scara.GetPos(ScaraRobotLib.POS_YAW),
										self.scara.GetPos(ScaraRobotLib.POS_GRIP),
										500)

		###############################
		#
		elif button == GamePadLib.BT_X and on == 1:
			pass

		###############################
		# Y Button
		#
		elif button == GamePadLib.BT_Y and on == 1:
			pass

		###############################
		# LB button - Z up
		#
		elif button == GamePadLib.BT_LB:
			pass

		###############################
		# LT button - Z down
		#
		elif button == GamePadLib.BT_LT:
			pass

		###############################
		# RB button - Gripper Close
		#
		elif button == GamePadLib.BT_RB:
			pass

		###############################
		# RT button - Gripper Open
		#
		elif button == GamePadLib.BT_RT:
			pass

#		print('Button Callback Called. ', str(button), str(on))

	####################################
	# Joystick Axis Callback
	#
	#	axis	axis index
	#	pos		position
	#
	def AxisCallback(self, axis, pos):

		###############################
		# X Moving
		#
		if axis == GamePadLib.ANA_LEFT_HORZ:
			if self.absAxis == True:
				tempX = pos * 100

			else:
				tempX = self.x;
				tempX += pos * 1

			if tempX > self.maxX:
				tempX = self.maxX
			if tempX < self.minX:
				tempX = self.minX

			self.x = tempX
			self.scara.SetPos(ScaraRobotLib.POS_X, self.x)

		###############################
		# Y Moving
		#
		elif axis == GamePadLib.ANA_LEFT_VERT:
			if self.absAxis == True:
				tempY = pos * 100

			else:
				tempY = self.y;
				tempY += pos * 1

			if tempY > self.maxY:
				tempY = self.maxY
			if tempY < self.minY:
				tempY = self.minY

			self.y = tempY
			self.scara.SetPos(ScaraRobotLib.POS_Y, self.y)

		###############################
		# Z Moving
		#
		if axis == GamePadLib.ANA_RIGHT_VERT:
			if self.absAxis == True:
				tempZ = pos * -100

			else:
				tempZ = self.z;
				tempZ += pos * -0.5

			if tempZ > self.maxZ:
				tempZ = self.maxZ
			if tempZ < self.minZ:
				tempZ = self.minZ

			self.z = tempZ
			self.scara.SetPos(ScaraRobotLib.POS_Z, self.z)

		###############################
		# Grip Moving
		#
		elif axis == GamePadLib.ANA_RIGHT_HORZ:
			if self.absAxis == True:
				tempGrip = pos * -300

			else:
				tempGrip = self.grip;
				tempGrip += pos * 1

			if tempGrip > self.maxGrip:
				tempGrip = self.maxGrip
			if tempGrip < self.minGrip:
				tempGrip = self.minGrip

			self.grip = tempGrip
			self.scara.SetPos(ScaraRobotLib.POS_GRIP, self.grip)

#		print('X : ', self.x, 'Y : ', self.y, 'Z : ', self.z, 'Yaw : ', self.yaw, 'Grip : ', self.grip)
#		print('X : ', self.scara.GetPos(ScaraRobotLib.POS_X), ' Y : ', self.scara.GetPos(ScaraRobotLib.POS_Y))

		###############################
		#
		self.scara.Move(self.moveMs)

#		print('Axis Callback Called.', str(axis), str(pos))

	####################################
	# Joystick Hat Switch Callback
	#
	#	hat 	hat index
	#	state	state
	#
	def HatCallback(self, hat, state):

		################################
		#
		if state == GamePadLib.HAT_UP:
			self.torque = not self.torque
			if self.torque == True:
				self.scara.TorqueControl(True)
				print('Torque On')
				self.scara.Move(self.initMoveMs)

			else:
				self.scara.TorqueControl(False)
				print('Torque Off')

		################################
		#
		elif state == GamePadLib.HAT_DOWN:
			if self.dirCW == True:
				self.dirCW = False
				print('Direction CCW')
				self.scara.SetDir(ScaraRobotLib.DIR_CCW)

			else:
				self.dirCW = True
				print('Direction CW')
				self.scara.SetDir(ScaraRobotLib.DIR_CW)

		################################
		#
		elif state == GamePadLib.HAT_LEFT:
			tempYaw = self.yaw
			tempYaw += self.hatStep * -1
			if tempYaw > self.maxYaw:
				tempYaw = self.maxYaw
			if tempYaw < self.minYaw:
				tempYaw = self.minYaw

			self.yaw = tempYaw
			self.scara.SetPos(ScaraRobotLib.POS_YAW, self.yaw)
			self.scara.Move(self.moveMs)

			self.hatStep += 1
			if self.hatStep > self.maxHatStep:
				self.hatStep = self.maxHatStep


		################################
		#
		elif state == GamePadLib.HAT_RIGHT:
			tempYaw = self.yaw
			tempYaw += self.hatStep * 1
			if tempYaw > self.maxYaw:
				tempYaw = self.maxYaw
			if tempYaw < self.minYaw:
				tempYaw = self.minYaw

			self.yaw = tempYaw
			self.scara.SetPos(ScaraRobotLib.POS_YAW, self.yaw)
			self.scara.Move(self.moveMs)

			self.hatStep += 1
			if self.hatStep > self.maxHatStep:
				self.hatStep = self.maxHatStep

		################################
		#
		elif state == GamePadLib.HAT_UP_LEFT:
			pass

		################################
		#
		elif state == GamePadLib.HAT_UP_RIGHT:
			pass

		################################
		#
		elif state == GamePadLib.HAT_DOWN_LEFT:
			pass

		################################
		#
		elif state == GamePadLib.HAT_DOWN_RIGHT:
			pass

		################################
		#
		elif state == GamePadLib.HAT_NONE:
			self.hatStep = 1

#		print('Hat Callback Called.', str(hat), str(state), self.yaw)

########################################
# main program
#
def main():

	cnt = ScaraRobotConntrol()
	if cnt.Initialize() == True:
		cnt.Run()


################################################################################
if __name__ == "__main__":
	main()
