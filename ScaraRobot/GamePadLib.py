# -*- coding: utf-8 -*-
################################################################################
# Game Pad Interface Library
#
#	F.S.Enterprise
#
#	History
#		Rev 1.0:2023.08.19
#		Rev	1.1:2023.08.25
#
#	Refferece URL
#		https://qiita.com/OkitaSystemDesign/items/ae9268f5d0ac77115032
#
#	Fucntions
#		Initialize()
#		Idle()
#		IsButtonPressed(btnum)
#		SetButtonCallback(func)
#		SetAxisCallback(func)
#		SetHatCallback(func)
#
from pygame.locals import *
import pygame
import keyboard
import sys
import time

########################################
#
MajorRevision		= 1
MinorRevision		= 0
JoystickName		= "Logicool Dual Action USB"

bDebug				= False

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
#			H(0) V(1)			H(2) V(3)
#
#			LEFT				RIGHT
#			BUTTON(10)			BUTTON(11)
#

ANA_LEFT_HORZ		= 0
ANA_LEFT_VERT		= 1
ANA_RIGHT_HORZ		= 2
ANA_RIGHT_VERT		= 3

BT_X				= 0
BT_Y				= 1
BT_B				= 2
BT_A				= 3
BT_LB				= 4
BT_RB				= 5
BT_LT				= 6
BT_RT				= 7
BT_BACK				= 8
BT_START			= 9
BT_ANA_LEFT			= 10
BT_ANA_RIGHT		= 11

HAT_NONE			= 0
HAT_UP				= 1
HAT_DOWN			= 2
HAT_LEFT			= 3
HAT_RIGHT			= 4
HAT_UP_LEFT			= 5
HAT_UP_RIGHT		= 6
HAT_DOWN_LEFT		= 7
HAT_DOWN_RIGHT		= 8

########################################
#
class GamePad():

	####################################
	# Constoructor
	#
	def __init__(self):
		self.InitializeParameters()

	####################################
	# Parameter Initializer
	#
	def InitializeParameters(self):
		#
		self.AxisState          = []
		self.HatState           = []
		self.ButtonState        = []

		self.buttons            = 0
		self.axes               = 0
		self.hats               = 0
		self.joynum             = 0

		self.buttonMap          = []

		self.ButtonCallback     = self.DummyButton
		self.AxisCallback       = self.DummyAxis
		self.HatCallback        = self.DummyHat

		self.bt_repeat_time     = 0
		self.hat_repeat_time    = 0
		self.axis_repeat_enable = False
		self.axis_repeat_time   = 0
		self.hat_res            = HAT_NONE

		self.axis_repeat_state  = 0
		self.bt_repeat_state    = 0
		self.hat_repeat_state   = 0
		self.repeat_1st         = 0.5
		self.repeat_2nd         = 0.1
		self.minAxisDead        = -0.05
		self.maxAxisDead        = 0.05

	####################################
	#
	def AxisRepeatEnable(self, enable):
		self.axis_repeat_enable = enable

	####################################
	#
	def SetButtonCallback(self, func):
		self.ButtonCallback = func

	####################################
	#
	def SetAxisCallback(self, func):
		self.AxisCallback   = func

	####################################
	#
	def SetHatCallback(self, func):
		self.HatCallback    = func

	####################################
	#
	#	button	button index
	#	on		bool True:on / False:off
	#
	def DummyButton(button, on):
		pass

	####################################
	#
	#	axis	axis index
	#	pos		position
	#
	def DummyAxis(axis, pos):
		pass

	####################################
	#
	#	hat 	hat index
	#	state	state
	#
	def DummyHat(hat, state):
		pass

	####################################
	# Control Initializer
	#
	#	Flase : No controller
	#
	def Initialize(self):

		pygame.init()

		################################
		# Check for Available Joystick
		#
		try:
			# check Joystick count
			#
			num = pygame.joystick.get_count()
			if num == 0:
				raise pygame.error

			# check joystick name
			#
			print('[Check Available Joystick(s)]')
			print(' ' + str(num) + ' Joystick(s) Available.')
			print(' Trying to find Controller ....')
			for i in range(num):
				self.joy = pygame.joystick.Joystick(i)
				self.joy.init()
				print(' Device Name "' + self.joy.get_name() + '" as Joystick Number ' + str(i) + '.', end = ' ')

				if self.joy.get_name() == JoystickName:
					self.joynum  = i
					print('Found.')
					print('')

					break
				else:
					print('')

		#
		except pygame.error:
			return False, 'No Joystick.'

		################################
		# Check Buttons, Axis and Hats available
		#
		try:
			#
			print('[Available Control Information]')
			self.buttons = self.joy.get_numbuttons()
			self.axes    = self.joy.get_numaxes()
			self.hats    = self.joy.get_numhats()

			print(" Number of Buttons : " + str(self.buttons))
			print(" Number of Axes    : " + str(self.axes))
			print(" Number of Hats    : " + str(self.hats))
			print('')

			############################
			#
			for i in range(self.buttons):
				self.buttonMap.append(False)

		#
		except pygame.error:
			return False, 'No Joystick.'

		################################
		# Check for Available Buttons
		#
		try:
			#
			print('[Check Available Buttons]')
			print(' ', end = ' ')
			for i in range(self.buttons):
				state = self.joy.get_button(i)
				print(str(i), end = ' ')
				self.ButtonState.append(False)

			print('Available.')
			print('')

		#
		except pygame.error:
			return False, 'Button Map Error.'

		################################
		# Check for Available Axis
		#
		try:
			#
			print('[Check Available Axis]')
			print(' ', end = ' ')
			for i in range(self.axes):
				pos = self.joy.get_axis(i)
				print(str(i), end = ' ')
				self.AxisState.append(pos)

			print('Available.')
			print('')

		#
		except pygame.error:
			return False, 'Axis Map Error.'

		################################
		# Check for Available Hat
		#
		try:
			#
			print('[Check Available Hat]')
			print(' ', end = ' ')
			for i in range(self.hats):
				state = self.joy.get_hat(i)
				print(str(i), end = ' ')
				self.HatState.append(state)

			print('Available.')
			print('')

		#
		except pygame.error:
			return False, 'Hat Map Error.'

		################################
		# Store Initial Status
		#
		self.UpdateButton();
		self.UpdateHat();
		self.UpdateAxis();

		return True, ''

	####################################
	# Update Axis Input
	#
	def UpdateAxis(self):

		#
		for i in range(self.axes):
			pos = self.joy.get_axis(i)

			############################
			#
			if self.axis_repeat_enable == True:

				if pos < self.minAxisDead or pos > self.maxAxisDead:
					if self.axis_repeat_state == 0:
						self.axis_repeat_state = 1
						self.axis_repeat_time = time.time()
						self.AxisState[i] = pos
						self.AxisCallback(i, pos)
#						print('Repeat : ', self.axis_repeat_state, ' Axis : ', i, pos)

					elif self.axis_repeat_state == 1:
						if time.time() > self.axis_repeat_time + self.repeat_1st:
							self.axis_repeat_time = time.time()
							self.axis_repeat_state = 2
							self.AxisState[i] = pos
							self.AxisCallback(i, pos)
#							print('Repeat : ', self.axis_repeat_state, ' Axis : ', i, pos)

					elif self.axis_repeat_state == 2:
						if time.time() > self.axis_repeat_time + self.repeat_2nd:
							self.axis_repeat_time = time.time()
							self.AxisState[i] = pos
							self.AxisCallback(i, pos)
#							print('Repeat : ', self.axis_repeat_state, ' Axis : ', i, pos)

				else:
					self.axis_repeat_state = 0

			############################
			#
			else:
				if self.AxisState[i] != pos:
					self.AxisState[i] = pos
					self.AxisCallback(i, pos)
#					print('Axis : ', i, pos)

	####################################
	# Update Button Input
	#
	def UpdateButton(self):

		#
		for i in range(self.buttons):

			# 押下マップの作成
			state = self.joy.get_button(i)
			if state == 1:
				self.buttonMap[i] = True
			else:
				self.buttonMap[i] = False

			# 変化があったら
			if state != self.ButtonState[i]:
				self.ButtonState[i] = state
				self.ButtonCallback(i, state)
#				print(i, state)

				# 押下
				if state == 1:
					self.bt_repeat_state = 1
					self.bt_repeat_time = time.time()

			# 押しっぱなし
			elif state == 1:
				if self.bt_repeat_state == 1:
					if time.time() > self.bt_repeat_time + self.repeat_1st:
						self.bt_repeat_time = time.time()
						self.bt_repeat_state = 2
						self.ButtonCallback(i, state)

				elif self.bt_repeat_state == 2:
					if time.time() > self.bt_repeat_time + self.repeat_2nd:
						self.bt_repeat_time = time.time()
						self.ButtonCallback(i, state)

#					print(str(i), ' Continue to push.')

	####################################
	# Update HAT input
	#
	def UpdateHat(self):

		#
		for i in range(self.hats):

			#
			state = self.joy.get_hat(i)
#			print('STAT : ', state)

			# 変化があった
			if (self.HatState[i] != state):
				self.HatState[i] = state
				if state == (0, 0):		self.hat_res = HAT_NONE
				elif state == (0, 1):	self.hat_res = HAT_UP
				elif state == (0, -1):	self.hat_res = HAT_DOWN
				elif state == (-1, 0):	self.hat_res = HAT_LEFT
				elif state == (1, 0):	self.hat_res = HAT_RIGHT
				elif state == (-1, 1):	self.hat_res = HAT_UP_LEFT
				elif state == (1, 1):	self.hat_res = HAT_UP_RIGHT
				elif state == (-1, -1):	self.hat_res = HAT_DOWN_LEFT
				elif state == (1, -1):	self.hat_res = HAT_DOWN_RIGHT
				self.HatCallback(i, self.hat_res)
#				print(i, self.hat_res)

				# 押下
				if state != (0, 0):
					self.hat_repeat_state = 1
					self.hat_repeat_time = time.time()

#					print('num : ', i, 'state : ', state, ' hat state : ', self.HatState[i], ' res : ', self.hat_res, ' rep state : ', self.hat_repeat_state)

			# 押しっぱなし
			elif state != (0, 0):

				if self.hat_repeat_state == 1:
					if time.time() > self.hat_repeat_time + self.repeat_1st:
						self.hat_repeat_time = time.time()
						self.hat_repeat_state = 2
						self.HatCallback(i, self.hat_res)

				elif self.hat_repeat_state == 2:
					if time.time() > self.hat_repeat_time + self.repeat_2nd:
						self.hat_repeat_time = time.time()
						self.HatCallback(i, self.hat_res)
			else:
				self.hat_repeat_state = 0

#				print('num : ', i, 'state : ', state, ' hat state : ', self.HatState[i], ' res : ', self.hat_res, ' rep state : ', self.hat_repeat_state)

	####################################
	#
	def Idle(self):
		pygame.event.get()
		self.UpdateAxis()
		self.UpdateButton()
		self.UpdateHat()

	####################################
	#
	def IsButtonPressed(self, btnum):
		return self.buttonMap[btnum]
