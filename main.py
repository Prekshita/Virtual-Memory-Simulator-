""" This file take inputs and check for any exception. and display error message if there are any exception. The input is provided through gui. The input trace file should be JSON format. """

from tkinter import filedialog, messagebox
from tkinter import *
import json 
from virtual_memory import virtualMemory

import pdb
from math import log 
fileName = ""

""" fileSelect():
is used to select the JSON trace file. File selected is stored in fileName 
"""
def fileSelect():
	global fileName
	fileName = filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = [("Json File", "*.json")])

""" guiElements():
guiElements Class attributes are used  to store inputs provided through GUI dropDown
"""
class guiElements():
	def __init__(self):
		self.virMSize = None
		self.phyMsize = None
		self.pOffset = None
		self.vByteSize = None
		self.pByteSize = None
		self.pageByteSize = None
"""
setUpVM(): 
This function takes guiElements object as an input and read the Json file.
funtion is used to handel all the exception from the data provided. This function checks if Page size is smaller than physical memory size or Physical memory smaller than virtual memory. It also checks if data provided in input trace file is in formate [ Read/Wrte, Process ID, Address ]. if any of the above mention condition is not satisfied, will raises an exception and return back
If there is no exception then it creates a object of virtualMemory class and execute its method startVM by passing trace file data 
"""
def setUpVM(guiObject):
	inputTrace = []
	sizeDict = {'KB':1024, 'MB': 1024*1024, 'GB': 1024*1024*1024} # Dict to provide value of KB, MB, GB
	vMSize = int(guiObject.virMSize.get()) * sizeDict[guiObject.vByteSize.get()]
	pMSize = int(guiObject.phyMsize.get()) * sizeDict[guiObject.pByteSize.get()]
	pageSize = int(guiObject.pOffset.get()) *sizeDict[guiObject.pageByteSize.get()]
	try:
		with open (fileName) as fobj: 
			inputTrace = json.load(fobj) # loading json file 
	except:
		messagebox.showerror("Error","Problem loading file, try again")
		return 
	try: 
		error = None
		for element in inputTrace:
			if int(element[1]) < 0 : # checking if processID is other than +ve integer 
				error = "Invalid Process ID : "+ element[1]+" \nThe process number should be greater than or equal to Zero"
			elif (element[0] not in "WR"): #checking if operation is other than 'R' or 'W'
				error = "Invalid Operation mode : "+ element[0]+ " \nMode of operation should be Write :'W' or Read :'R'"
			elif int(log(vMSize,2)) != len(element[2])*4: #checking if Input address bits not same as input virtual memory size
				error = "Invalid Virtual Address :"+ element[2] + "\n address size does not correspond to Hexadecimal Virtual Address "
			else: # checking if input address is Hexadecimal value 
				for character in element[2]:
					if character not in "abcdefABCDEF0123456789":
						error = " Invalid Address input " + element[2] +"\n Address Input should be HexaDecimal value Ex: FEAB1234"
			if error:
				messagebox.showerror("Error",error)
				return
	except Exception as e: # generic exception 
		error = "invalid input : "+ str(element)
		print("An exception was generated while scanning the input from file(", str(element), "): ", str(e))
		messagebox.showerror("Error",error)
		return
	""" Page size should be lessthan or equal to physical memory . physical memory should be less than virtual memory """
	if(pageSize > vMSize or pMSize > vMSize or pageSize > pMSize):
		messagebox.showerror("Error", "Not a valid Input \n Page size should be smaller than Physical memory Size \n physical memory should be smaller than Virtual memory size")
	else: 
		vMObj = virtualMemory(vMSize, pMSize, pageSize)# creating object of Virtual memory 
		statValue = vMObj.startVM(inputTrace)
		""" Virtual memory Simulator statiscs is displayed using tkinter message box."""
		value = " Number of Process: {0}\n\n Number of page Hits: {1}\n\n Number of Page Fault: {2}\n\n Number of Page Replaced: {3}\n\n Number of Write Back: {4}\n\n Number of Input Virtual Addresses: {5}\n\n Percentage of page Hit: {6}%\n\n Percentage of Page Miss: {7}%". format(statValue.processCount, statValue.pageHit, statValue.pageFaultCount, statValue.pageReplaceCount, statValue.pageWBackCount , statValue.noOfAddress, statValue.pageHit*100/statValue.noOfAddress, statValue.pageFaultCount*100/statValue.noOfAddress)
		messagebox.showinfo("Statistics", value)
	
	
	
"""
main(): 
Input is provided through GUI, GUI has drop down to select different address for virtual, physical and pagesize. On pressing "File select" button fileSelect function is called. this function directs us to select the file(JSON file) and upload.
RUN button is used to run the Virtual memory simulatior.
gui object is created for class guiElements 
"""
def main():
	gui = guiElements()
	root = Tk()
	root.title("Virtual memory simulator ")
	Label(root, text = "Select from dropdown").grid(row = 0, column = 2, columnspan = 2,sticky='w', pady=(20,0))
	""" creating Dropdown widget for Virtual memory """
	Label ( root, text = "Virtual memory size:").grid(row = 1, column = 1, sticky='e', pady = 20)
	gui.virMSize = StringVar()
	gui.virMSize.set("4")  # default set of Virtual memory size  to 1GB
	gui.vByteSize = StringVar()
	gui.vByteSize.set("GB")
	""" Dropdown options for virtual memory size"""
	OptionMenu(root, gui.virMSize,"1","2","4","8","16","32","64","128","256","512").grid(row = 1, column = 2)
	OptionMenu(root, gui.vByteSize, "KB", "MB", "GB").grid(row = 1, column = 3, padx = (0,50))
	
	""" creating Dropdown widget for page size """
	gui.pOffset = StringVar()
	gui.pOffset.set("1") # default set of page offset to 64KB
	gui.pageByteSize = StringVar()
	gui.pageByteSize.set("KB")
	Label(root, text = "Page Size :").grid(row = 2,column = 1, sticky='e', pady = 20)
	#Label(root, text = "Select from dropdown").grid(row = 2, column = 1)
	
	""" Dropdown options for page Size"""
	OptionMenu(root,gui.pOffset,"1","2","4","8","16","32","64","128","256","512").grid(row = 2, column = 2)
	OptionMenu(root,gui.pageByteSize,"KB", "MB", "GB").grid(row = 2, column = 3, padx = (0,50))

	""" creating Dropdown widget for Physical memory"""
	gui.phyMsize = StringVar()
	gui.phyMsize.set("16") # default set of physical Memory Size to 256MB
	gui.pByteSize = StringVar()
	gui.pByteSize.set("KB")
	Label(root, text = "Physical Memory Size:").grid(row = 3,column = 1, sticky='e', pady = 20)
	#Label(root, text = "Select from dropdown").grid(row = 4, column = 1)

	""" Dropdown options for Physicla memory size""" 
	OptionMenu(root, gui.phyMsize,"1","2","4","8","16","32","64","128","256","512").grid(row = 3, column = 2)
	OptionMenu(root, gui.pByteSize, "KB", "MB", "GB").grid(row = 3, column = 3, padx = (0,50))
	""" Creating a button to selectfie (JSON file).  will execute function fileSelect on pressing this button """
	Label(root, text ="Upload Input trace file(*.json):").grid(row = 4,column = 1, sticky='e', pady = 20, padx = (30, 0))
	#Label(root, text=fileName).grid(row = 8, column = 3, sticky='e')
	Button(root, text ="select file", command = fileSelect).grid(row = 4, column = 2)
	""" creating Button RUN on pressing will execute setUpVM function"""
	Button(root, text ="RUN", command = lambda: setUpVM(gui), width=8, bg='pale green').grid (row = 5, column = 2, pady=20)

	root.mainloop()

if __name__ == "__main__":
	main()
