################################################################################
# Scara Robot Control
#
#	F.S.Enterprise
#
#	History
#		Rev 1.0:2023.08.19
#		Rev	1.1:2023.08.25
#
#	https://docs.python.org/ja/3/library/ctypes.html
#
import ctypes
import time

VID = 0x10C4	# ロボットのVender ID
PID	= 0xEA80	# ロボットのProduct ID

POS_X    = 0
POS_Y    = 1
POS_Z    = 2
POS_YAW  = 3
POS_GRIP = 4

DIR_CW  = 0
DIR_CCW = 1

########################################
#
dll = ctypes.cdll.LoadLibrary("./ScaraLib.dll")

########################################
#
dllSetDebugMode = dll.SetDebugMode
dllSetDebugMode.argtype = ctypes.c_bool
dllSetDebugMode.restype = None
########################################
#
dllGetEnumDevices = dll.GetEnumDevices
dllGetEnumDevices.argtype = None
dllGetEnumDevices.restype = ctypes.c_int
########################################
#
dllScaraOpen = dll.ScaraOpen
dllScaraOpen.argtypes = [ctypes.c_int]
dllScaraOpen.restype = ctypes.c_void_p
########################################
#
dllScaraClose = dll.ScaraClose
dllScaraClose.argtypes = [ctypes.c_void_p]
dllScaraClose.restype = ctypes.c_bool
########################################
#
dllInitialize = dll.Initialize
dllInitialize.argtypes = [ctypes.c_void_p]
dllInitialize.restype = ctypes.c_bool
########################################
#
dllSetDir = dll.SetDir
dllSetDir.argtypes = [ctypes.c_int]
dllSetDir.restype = ctypes.c_bool
########################################
#
dllFixYaw = dll.FixYaw
dllFixYaw.argtype = ctypes.c_bool
dllFixYaw.restype = ctypes.c_bool
########################################
#
dllSetPos = dll.SetPos
dllSetPos.argtypes = [ctypes.c_int, ctypes.c_double]
dllSetPos.restype = ctypes.c_bool
########################################
#
dllGetPos = dll.GetPos
dllGetPos.argtypes = [ctypes.c_int]
dllGetPos.restype = ctypes.c_double
########################################
#
dllMotorTorque = dll.MotorTorque
dllMotorTorque.argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.c_int, ctypes.c_int]
dllMotorTorque.restype = ctypes.c_bool
########################################
#
dllMove = dll.Move
dllMove.argtypes = [ctypes.c_void_p, ctypes.c_int]
dllMove.restype = ctypes.c_bool

########################################
#
class ScaraRobot():

	####################################
	# Constoructor
	#
	def __init__(self):
		self.InitializeParameters()

	####################################
	# Parameter Initializer
	#
	def InitializeParameters(self):
		self.numDevice = 0
		self.hDevice   = None

	####################################
	#
	def Initialize(self):
		numDevice = self.GetEnumDevices();
		print(numDevice, ' device(s) found.')

		if (numDevice > 0):
			self.hDevice = self.ScaraOpen(0);
			print('device', hex(self.hDevice))

#			self.SetDebugMode(True)
			self.FixYaw(True)
			dllInitialize(self.hDevice)
			return True, ''

		else:
			return False, 'No Scara Robot.'

	####################################
	#
	def SetDir(self, type):
		return dllSetDir(type)

	####################################
	#
	def FixYaw(self, fix):
		return dllFixYaw(fix)

	####################################
	#
	def SetDebugMode(self, debug):
		return dllSetDebugMode(debug)

	########################################
	#
	def GetEnumDevices(self):
		return dllGetEnumDevices()

	########################################
	#
	def ScaraOpen(self, deviceNum):
		return dllScaraOpen(deviceNum)

	####################################
	#
	def TorqueControl(self, on):
		return dllMotorTorque(self.hDevice, on, 1, 5)

	####################################
	#
	def GetPos(self, type):
		return dllGetPos(type)

	####################################
	#
	def SetPos(self, type, pos):
		return dllSetPos(type, pos)

	####################################
	#
	def Move(self, ms):
		return dllMove(self.hDevice, ms)

