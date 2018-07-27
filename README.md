Virtual Memory Simulator 

Virtual memory Simulator is written in Python.
Simulator takes Virtual memory Size , Physical Memory size, page size and address trace file as input. 
Input is provided through GUI, GUI has drop down to select different addresses for virtual, physical and pagesize. On pressing "File select" button Gui will navigate throug windows to select a Json file . fileSelect function is called for this operation. 
RUN button is used to run the Virtual memory simulatior.

Input :

Input should be selected such that Page size is lessthan or equal to physical memory size and Physical memory Size less than virtual memory size.
ex: Virtual memory Size 4GB, Physical Memory =  2GB , Page Size = 64KB
Json file should contain List of Element.Each element is a list of different input trace. 
ex : [["W", "1", "FABE1234"][["R", "2", "FAFE1234"]...[]]

First element in the trace input elemnet should be R:Read or W:write
Second element in trace input should be Process ID: Positive Integer 
Third element in the trace input should be Virtual address: Hexa decimal Value

This simulator handels virtual Page Number. It will not handel any address change with in that page. 
for example Virtual memory Size 4GB, Physical Memory =  8KB , Page Size = 2KB 
Input trace is [["W", "1", "FABE1234"][["R", "1", "FABE1234"]...[]]
			VPN			VPO
FABE1234	FABE1		234
FABE12AA	FABE1		2AA

even thoug page offset is different both refer to same page. Simulator will not handling read and write based on address with in page it will check only in page level.

outPut:

	statistics of 
	Number of process present in system
	Number of page Fault
	Number of page replacement 
	Page Hits 
	Number of addresses
	Percentage of page hit 
	Percentage of Page Miss 
	Number of write back to the secondary memory
	
	
setUpVM funtion is used to handel all the exception from the data provided. This function checks if Page size is smaller than physical memory size or Physical memory smaller than virtual memory. it also checks if data provided in input trace file is in formate [ Read/Wrte, Process ID, Address ]. if any of the above mention condition is not satisfied, will raises an exception and return back. If there is no exception then it creates a object of virtualMemory class and execute its method startVM by passing trace file as input . startVM method will retun a statisctis on Number of process present in system, Number of page Fault, number of page replacement, Page Hits, Number of trace, percentage of page hit and number of write back to the secondary memory. This statiscs is displayed using tkinter messahe box.


Virtual Memory class has startVM method. This method takes trace file data as input. In this fuction Value iterator, iterate over input trace list. Virtual address consists of both Virtual Page Number(VPN) and Virtual Page Offset(VPO). extractVPOAndVPN method is used to get Virtual Page Number(VPN) and Virtual Page Offset(VPO). For each trace input simulator will created an object of class virtualMemoAddr. Each object has attribute virtualPageNo,virtualPageOffset, processID and operation. These Objects are stored inside traceObjectList list. This List is iterated over element. 

ProcessID in each element is check against processDict. processDict hold processID and its corresponding page Table. If Current processID exists in processDict , will load its corresponding page table. If process does not exist, will create new processID and assign new pageTable object. updatePageTable method is called for each pageTable object. updatePageTable takes virtualMemoAddr object, physicalMemory object as an input and check if that pageNumber exists in corresponding ProcessID's __pageTableDict. If PageNumber exists in __pageTableDict, will check for operation(Read/Write) and update dirty bit. If page number does not exist will create new page object for that page number in __pageTableDict and will update in Physical memory. 

insertPage method in physical memory class is called to update page in physical memory. This method first check if there is space available to store new page. Stores the page if there is space in physical memory. If there is no sufficient place it will call pageReplacement function.

Page replacement policy : queue 
queue size set same as physical memory size. Will use push and pop method add and remove page from physicla memory 

When Popping the page will check for its dirty bit status and update the page in secondry memory if it is set.



