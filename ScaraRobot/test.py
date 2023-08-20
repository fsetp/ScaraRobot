import GamePadLib
from GamePadLib import GamePad
import ScaraRobotLib
from ScaraRobotLib import ScaraRobot

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
		self.pad = None
		self.scara = None
		self.torque = False
		self.x = 0
		self.y = 0
		self.z = 0
		self.yaw = 0
		self.oc = 0
		self.hatStep = 1

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

		return ret

	####################################
	#
	def Run(self):
		################################
		#
		while True:
			self.pad.Idle()

	####################################
	#
	#	button	button index
	#	on		bool True:on / False:off
	#
	def ButtonCallback(self, button, on):
		if button == GamePadLib.BT_START and on == 1:
			self.torque = not self.torque
			if self.torque == True:
				self.scara.TorqueControl(True)
				print('Torque On')
			else:
				self.scara.TorqueControl(False)
				print('Torque Off')

		elif button == GamePadLib.BT_A and on == 1:
			x   = self.scara.GetPos(0)
			y   = self.scara.GetPos(1)
			z   = self.scara.GetPos(2)
			yaw = self.scara.GetPos(3)
			oc  = self.scara.GetPos(4)
			print('X:' , str(x), ' Y:', str(y), ' Z: ', str(z), ' YAW: ', str(yaw), ' OC:', str(oc))

	#	print('Button Callback Called. ', str(button), str(on))

	####################################
	#
	#	axis	axis index
	#	pos		position
	#
	def AxisCallback(self, axis, pos):

		###############################
		# XY Moving
		#
		tempX = 0.0
		tempY = 0.0

		#
		if axis == GamePadLib.ANA_LEFT_HORZ:
			tempX = pos * 1000

		elif axis == GamePadLib.ANA_LEFT_VERT:
			tempY = pos * 1000

		self.x = tempY
		self.y = tempX

		self.scara.MoveXY(self.x, self.y, 500)

		###############################
		# Z Yaw Moving
		#
		tempZ = 0.0
		tempYaw = 0.0

		#
		if axis == GamePadLib.ANA_RIGHT_HORZ:
			tempYaw = pos * 100

		elif axis == GamePadLib.ANA_RIGHT_VERT:
			tempZ = pos * 100

		self.yaw = tempYaw * -1
		self.z = tempZ * -1

		self.scara.MoveZ(self.z, 500)
		self.scara.MoveYaw(self.yaw, 500)

		print('Axis Callback Called.', str(axis), str(pos))

	####################################
	#
	#	hat 	hat index
	#	state	state
	#
	def HatCallback(self, hat, state):

		stepPower = 5
		tempX = self.y
		tempY = self.x

		################################
		#
		if state == GamePadLib.HAT_UP:
			tempY -= self.hatStep

		elif state == GamePadLib.HAT_DOWN:
			tempY += self.hatStep

		elif state == GamePadLib.HAT_LEFT:
			tempX -= self.hatStep

		elif state == GamePadLib.HAT_RIGHT:
			tempX += self.hatStep

		elif state == GamePadLib.HAT_UP_LEFT:
			tempX -= self.hatStepstep
			tempY -= self.hatStep

		elif state == GamePadLib.HAT_UP_RIGHT:
			tempX += self.hatStep
			tempY -= self.hatStep

		elif state == GamePadLib.HAT_DOWN_LEFT:
			tempX -= self.hatStep
			tempY += self.hatStep

		elif state == GamePadLib.HAT_DOWN_RIGHT:
			tempX += self.hatStep
			tempY += self.hatStep

		################################
		#
		if state == GamePadLib.HAT_NONE:
			self.hatStep = 1

		else:
			self.hatStep = self.hatStep + stepPower
			if self.hatStep > 50:
				self.hatStep = 50

		self.x = tempY
		self.y = tempX

		self.scara.MoveXY(self.x, self.y, 500)

		print('Hat Callback Called.', str(hat), str(state), str(self.hatStep), str(tempX), str(tempY))

########################################
# main program
#
def main():

	cnt = ScaraRobotConntrol()
	cnt.Initialize()
	cnt.Run()


################################################################################
if __name__ == "__main__":
	main()
