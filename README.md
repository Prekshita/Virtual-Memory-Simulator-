# Virtual-Memory-Simulator
"""Virtual memory Simulator : 
Simulator takes Virtual memory Size , Physical Memory size, page size and address trace file as input. and run the virtual memory simulator and provide the statistics of Number of process present in system, Number of page Fault, number of page replacement and number of write back to the secondary memory
This simulator handels virtual Page Number. It will not handel any address change with in that page. """

from tkinter import *
from math import log
from collections import deque
import pdb

""" 
	virtualMemoAddr(): 
	For each trace input created an object of class virtualMemoAddr. each object has 
	Attributes			
	virtualPageNo(Public)		: Stores virtual page number
	virtualPageOffset(Public)	:stores virtual offset
	processID (Public)			:Stores Process Number
	operation(Public)			:Stores Read/Write operation 


	printValue(): 
	This function will display a formated data VPO, VPN , PID, R/W

"""
class virtualMemoAddr():
	def __init__(self, virtualPageNo, virtualPageOffset, processID, operation):
		self.virtualPageNo = virtualPageNo
		self.virtualPageOffset = virtualPageOffset
		self.processID = processID
		self.operation = operation
		
	def printValue(self):
		print ("VPN : {0:3} VPO : {1:3}, PID : {2:3}, R/W : {3:3}".format(self.virtualPageNo,self.virtualPageOffset,self.processID, self.operation))
""" page():
	page object is created inside page table. for each virtual Page Number 
	
	Attributes
	Physical Page Number(Public) : Stores Physical page Number
	Dirty Bit(Public) :   This bit is set if address inside page needs to be written """
class page():
	def __init__(self):
		self.PPN = None
		self.dirtyBit = 0
""" pageTable(): 
	For each processID page table object is created. if N processes are running N PageTable will be created.
	
	Attributes
	__pageTableDict(Private) : Key = Virtual Page Number, Value = Page
	
	updatePageTable():
	this function checks if Virtual Page Number is present in Page table. if its present will update the dirty bit.
	If Virtual page number is not present it will create new page  and insert this page in Physical memory 
	and update dirty bit
	Inputs: virtualMemoryaddress, physicalMemory, StatsObj
	outputs : none """

class pageTable():
	def __init__(self):
		self.__pageTableDict = {}

	def updatePageTable(self, virtualMemoAddr, physicalMemory, StatsObj):
		if virtualMemoAddr.virtualPageNo in self.__pageTableDict: # Check if page in page table
			if physicalMemory.pageExistsOrNot(self.__pageTableDict[virtualMemoAddr.virtualPageNo]): #Check if page present in physical memory 
				StatsObj.pageHit += 1
			else:
				physicalMemory.insertPage(self.__pageTableDict[virtualMemoAddr.virtualPageNo], StatsObj)# insert page to physical memort 
				StatsObj.pageFaultCount += 1
		else:
			self.__pageTableDict[virtualMemoAddr.virtualPageNo] = page() # create new page 
			StatsObj.pageFaultCount += 1
			physicalMemory.insertPage(self.__pageTableDict[virtualMemoAddr.virtualPageNo], StatsObj)
		if virtualMemoAddr.operation is 'W': # check if operation is write 
			self.__pageTableDict[virtualMemoAddr.virtualPageNo].dirtyBit = 1 # set dirty bit if operation is write 
"""
	statistics():
	This class provide the statics of Virtual Simulator 
	
	Attributes:
	processCount 		: Keep count of Number of process In system
	pageFaultCount 		: Number of page faults 
	pageReplaceCount 	: Number of pages removed from Physical memory due to page Fault
	pageWBackCount 		:Number of pages written to Seconadry memory from Physical memory 

"""

class statistics():
	def __init__(self):
		self.processCount = 0
		self.pageFaultCount = 0
		self.pageReplaceCount = 0
		self.pageWBackCount = 0
		self.pageHit =0
		self.noOfAddress = 0

	
"""
	physicalMemory():
	This class implemts Physical Memory 
	
	Attributes:
	pMemorySize 	:Size of Physical memory
	pageSize		:Size of Page
	pMaxPageNo		:Maximum number of pages Inside Physical memory
	queue			:To implement queue, Page replacement method
	pPageNumberDict :To store the Information of Physical memory
					Key : Physical Page Number, Value = page
	
	insertPage():
		This method check if physical memory is full and call pageReplacement() method if its full or insert page if it has space.
		
	pageReplacement():
		Page replacement policy : Queue
		This method replaces page inside physical memory. pops out page which was inseted first.
"""
class physicalMemory():
	
	def __init__(self, pMemorySize, pageSize):
		self.pMemorySize = pMemorySize
		self.pageSize = pageSize
		self.pMaxPageNo = int(self.pMemorySize/self.pageSize) # Max number of pages in Physical memory 
		self.queue = deque(maxlen = self.pMaxPageNo) # setting ques size to physical memory 
		self.pPageNumberDict ={}
		
	def pageReplacement(self,page, StatsObj):
		pdb.set_trace
		popedPage = self.queue.popleft() # pop page from physical memory 
		if popedPage.dirtyBit:
			StatsObj.pageWBackCount += 1
		page.PPN = popedPage.PPN  # replace the popped page position in physical memory  with new page 
		del self.pPageNumberDict[popedPage.PPN]
		popedPage.PPN = None
		self.queue.append(page)
		self.pPageNumberDict[page.PPN] = page
		
	def pageExistsOrNot(self, page):
		if page.PPN in self.pPageNumberDict:
			return True
		else:
			return False
		
	def insertPage(self, page, StatsObj):
		if len(self.pPageNumberDict) >= self.pMaxPageNo: # check if physical memory has space.
			StatsObj.pageReplaceCount += 1
			self.pageReplacement(page,StatsObj)
		else:
			for position in range(self.pMaxPageNo): 
				if position not in self.pPageNumberDict: # check if any space available in physical memory 
					self.pPageNumberDict[position] = page
					page.PPN = position
					self.queue.append(page)
					break
					
"""
	virtualMemory() 
	this class will implemet virtual memory 
	Attributes:
	vMemorySize :Size of Virtual Memory
	virtualPgaOffset: Size of Virtual page 
	pMemortSize : size of physical memory size
	vMObjList : List to hold each virtual address. each elemt is a list of VPN,VPN,ProcessID, operation
	processDict: to hold all the processes. key = ProcessID, value = PageTable
	
	extractVPOAndVPN():
	this funtion extarct VPO and VPN from virtual address
	input : Virtual address
	outputs : VPO, VPN
	
	startVM():
		JSON file data is provided to this function. This function reads each trace input and format this input. create a object of class virtualMemoAddr class and store it in a list.
		 Each element in list is checked for its processID in processDict.Loads pageTable If ProcessID is present or create new processID if its not present
		 this function create a object of class statistics and return statistics of Input traces.
		 
	
"""
class virtualMemory():
	def __init__(self, vAddrSize, pAddSize, pageSize):
		self.vMemorySize = vAddrSize
		self.virtualPgaOffset = pageSize
		self.pMemortSize = pAddSize
		self.vMObjList= []
		self.processDict ={} 
		self.virtualPageNUmber =int(log( self.vMemorySize / self.virtualPgaOffset, 2))# number of bits to represent Virtual page number 

	def extractVPOAndVPN(self,address):
		decVal = int(address, 16) # conver Hex to int
		binVal = bin(decVal)# conver int to binary 
		virtualPage = binVal[2:self.virtualPageNUmber+2]# binVal will be 0b10100 , to trunceate first 2 character (0b)
		vOffset = binVal[self.virtualPageNUmber+2:]
		return virtualPage,vOffset

	def startVM(self,addressList):
		statUpdate = statistics()
		for value in addressList:
			address = value[2]
			vPage, vOffset = self.extractVPOAndVPN(address)
			self.vMObjList.append(virtualMemoAddr(vPage, vOffset, value[1], value[0]))

		pMemory = physicalMemory(self.pMemortSize, self.virtualPgaOffset)
		for element in self.vMObjList:
			if element.processID not in self.processDict:
				self.processDict[element.processID] = pageTable() # create ProcessID if it does not exist 
				statUpdate.processCount += 1
			PageTableObj = self.processDict[element.processID] 
			PageTableObj.updatePageTable(element, pMemory, statUpdate) 
			statUpdate.noOfAddress += 1
		return statUpdate
		

	
		

	
	
	
	
