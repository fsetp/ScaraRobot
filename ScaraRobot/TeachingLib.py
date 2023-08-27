################################################################################
# Teaching Control
#
#	F.S.Enterprise
#
#	History
#		Rev	1.1:2023.08.25
#
#	https://imagingsolution.net/program/python/tkinter/asksaveasfilename/
#	https://mulberrytassel.com/tkinter-start-48/
#	https://note.nkmk.me/python-json-load-dump/
#	https://note.nkmk.me/python-file-io-open-with/
#

#from tkinter import filedialog
import tkinter
import tkinter.filedialog
import json

####################################
#
class Teaching():

	####################################
	# Constoructor
	#
	def __init__(self):
		self.saveFileName = 'teaching.tcg'
		self.openFileName = 'teaching.tcg'
		self.rowNumber = 0
		self.actionList = []

	####################################
	#
	def Initialize(self):
		self.rowNumber = 0

	####################################
	#
	def SelectSaveTeachingFile(self):
		main = tkinter.Tk()
		main.withdraw()
		self.saveFileName = tkinter.filedialog.asksaveasfilename(title = 'Teaching File Save as ...',
															filetypes = [('Teaaching', '.tcg')],
															initialdir = './',
															defaultextension = 'tcg')
		main.destroy()
#		print(self.saveFileName)
#		print(type(self.saveFileName))
		if self.saveFileName == '':
			print('cancel')

	####################################
	#
	def SelectOpenTeachingFile(self):
		main = tkinter.Tk()
		main.withdraw()
		self.oepnFileName = tkinter.filedialog.askopenfilename(title = 'Teaching File Open ...',
															filetypes = [('Teaaching', '.tcg')],
															initialdir = './',
															defaultextension = 'tcg')
		main.destroy()

		if self.oepnFileName == '':
			return False

		return True

	####################################
	#
	def AddPosition(self, x, y, z, yaw, grip, ms):

		#
		sentence = {'raw' : self.rowNumber, 'type' : 'move', 'x-pos' : x, 'y-pos' : y, 'z-pos' : z, 'yaw-pos' : yaw, 'grip-pos' : grip, 'ms' : ms}
		print(sentence)
		self.actionList.append(sentence)
		self.rowNumber += 1

		#
		self.SaveActionList()

	####################################
	#
	def SaveActionList(self):

		#
		with open(self.saveFileName, 'w') as file:
			json.dump(self.actionList, file, ensure_ascii = False, indent = 4)

	####################################
	#
	def LoadActionList(self):

		#
		with open(self.openFileName) as file:
			self.actionList = json.load(file)

		self.rowNumber = len(self.actionList)

	####################################
	#
	def GetEnumAction(self):
		return self.rowNumber

	####################################
	#
	def GetType(self, num):
		if (num >= 0 and num < self.rowNumber):
#			print(type(self.actionList[num]))
#			print(self.actionList[num])
			return self.actionList[num]['type']

	####################################
	#
	def GetPositions(self, num):
		if (num >= 0 and num < self.rowNumber):
			return self.actionList[num]['x-pos'] , \
					self.actionList[num]['y-pos'], \
					self.actionList[num]['z-pos'], \
					self.actionList[num]['yaw-pos'], \
					self.actionList[num]['grip-pos'], \
					self.actionList[num]['ms']
	