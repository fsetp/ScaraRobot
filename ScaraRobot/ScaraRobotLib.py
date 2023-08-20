################################################################################
# https://docs.python.org/ja/3/library/ctypes.html
#
import ctypes
import time

VID = 0x10C4	# ロボットのVender ID
PID	= 0xEA80	# ロボットのProduct ID

########################################
#
dll = ctypes.cdll.LoadLibrary("./ScaraLib.dll")

########################################
#
dllSetDebugMode = dll.SetDebugMode
dllSetDebugMode.argtype = ctypes.c_bool
dllSetDebugMode.restype = None
########################################

########################################
#
dllGetEnumDevices = dll.GetEnumDevices
dllGetEnumDevices.argtype = None
dllGetEnumDevices.restype = ctypes.c_bool
########################################
#
dllDeviceOpen = dll.DeviceOpen
dllDeviceOpen.argtypes = [ctypes.c_int]
dllDeviceOpen.restype = ctypes.c_void_p
########################################
#
dllDeviceClose = dll.DeviceClose
dllDeviceClose.argtypes = [ctypes.c_void_p]
dllDeviceClose.restype = ctypes.c_bool

########################################
#
dllScaraInitialize = dll.ScaraInitialize
dllScaraInitialize.argtypes = [ctypes.c_void_p]
dllScaraInitialize.restype = ctypes.c_bool
########################################
#
dllMotorTorque = dll.MotorTorque
dllMotorTorque.argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.c_int, ctypes.c_int]
dllMotorTorque.restype = ctypes.c_bool
########################################
#
dllMoveXY = dll.MoveXY
dllMoveXY.argtypes = [ctypes.c_void_p, ctypes.c_double, ctypes.c_double, ctypes.c_int]
dllMoveXY.restype = ctypes.c_bool
########################################
#
dllMoveZ = dll.MoveZ
dllMoveZ.argtypes = [ctypes.c_void_p, ctypes.c_double, ctypes.c_int]
dllMoveZ.restype = ctypes.c_bool
########################################
#
dllMoveXYZ = dll.MoveXYZ
dllMoveXYZ.argtypes = [ctypes.c_void_p, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_int]
dllMoveXYZ.restype = ctypes.c_bool
########################################
#
dllMoveXYZYaw = dll.MoveXYZYaw
dllMoveXYZYaw.argtypes = [ctypes.c_void_p, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_int]
dllMoveXYZYaw.restype = ctypes.c_bool
########################################
#
dllMoveXYZYawOC = dll.MoveXYZYawOC
dllMoveXYZYawOC.argtypes = [ctypes.c_void_p, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_int]
dllMoveXYZYawOC.restype = ctypes.c_bool
########################################
#
dllMoveYawOC = dll.MoveYawOC
dllMoveYawOC.argtypes = [ctypes.c_void_p, ctypes.c_double, ctypes.c_double, ctypes.c_int]
dllMoveYawOC.restype = ctypes.c_bool
########################################
#
dllMoveYaw = dll.MoveYaw
dllMoveYaw.argtypes = [ctypes.c_void_p, ctypes.c_double, ctypes.c_int]
dllMoveYaw.restype = ctypes.c_bool
########################################
#
dllMoveOC = dll.MoveOC
dllMoveOC.argtypes = [ctypes.c_void_p, ctypes.c_double, ctypes.c_int]
dllMoveOC.restype = ctypes.c_bool
########################################
#
dllGetPos = dll.GetPos
dllGetPos.argtypes = [ctypes.c_void_p, ctypes.c_int]
dllGetPos.restype = ctypes.c_double

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
#		self.msMove    = 2000

	####################################
	#
	def Initialize(self):
#		numDevice = dll.GetEnumDevices();
		numDevice = dllGetEnumDevices(None);
		print(numDevice, ' device(s) found.')

		if (numDevice > 0):
			self.hDevice = dllDeviceOpen(0);
			print('device', hex(self.hDevice))

#			dllSetDebugMode(True)
			dllScaraInitialize(self.hDevice)
			return True, ''

		else:
			return False, 'No Scara Robot.'

	####################################
	#
	def TorqueControl(self, on):
		return dllMotorTorque(self.hDevice, on, 1, 5)

	####################################
	#
	def MoveXY(self, x, y, ms):
		return dllMoveXY(self.hDevice, x, y, ms)

	####################################
	#
	def MoveZ(self, z, ms):
		return dllMoveZ(self.hDevice, z, ms)

	####################################
	#
	def MoveYaw(self, yaw, ms):
		return dllMoveYaw(self.hDevice, yaw, ms)

	####################################
	#
	def MoveOC(self, oc, ms):
		return dllMoveOC(self.hDevice, oc, ms)

	####################################
	#
	def GetPos(self, motor):
		return dllGetPos(self.hDevice, motor)
