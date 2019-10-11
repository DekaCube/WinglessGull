#Scheduling Simulator v 1.3
#Daniel Bennett
#Operating Systems

#Define the process class, the process will keep track of timers and where it is located
#as well as where it wants to be. 

class Process:
    def __init__(self,pid,bursts):
        self.bursts = bursts[0:]
        self.pid = pid #process identifier
        self.responce = -1
        self.wait = 0 #total time spent in ready queue
        self.tr = 0
        self.cburst = 0 #current cpu burst
        self.ioburst = 0  #current io burst
        self.state = "IO"
        self.timeincpu = 0
        self.tq = 1 #size of current timeslice
        self.location = "NONE" #where the process is currently located
        self.update() #update the process to load first burst and change state to CPU
    
    #set length of current timeslice for this process
    def set_tq(self,new_tq):
        self.tq = new_tq
        return
    
    #set the location of this process
    def set_location(self,location):
        self.location = location
        return
    
    def _print(self):
        print("==========PROCESS INFORMATION==============")
        print("Process ID = " + self.pid)
        print("Current Burst = " + str(self.cburst))
        print("Current State = " + self.state)
        print("Turnaround = " + str(self.tr))
        print("Wait = " + str(self.wait))
        print("Responce Time = " + str(self.responce))
        print("Time in CPU = " + str(self.timeincpu))
        print("Current IO Burst = " + str(self.ioburst))
        print("Remaining bursts = " + str(self.bursts))
        print("Current Location = " + self.location)
        print("===========================================")
    
    def update(self):
        #if process is in CPU state, burst is finished, and has another burst(IO)
        if self.cburst == 0 and self.bursts != [] and self.state == "CPU":
            self.ioburst = self.bursts[0]
            self.bursts = self.bursts[1:]
            self.state = "IO"
               
        #if burst is finished and no more bursts exist
        if self.cburst <= 0 and self.bursts == []:
            self.state = "DONE"
            
        #if in IO and finished with IO burst    
        if self.ioburst == 0 and self.state == "IO":
            self.cburst = self.bursts[0]
            self.bursts = self.bursts[1:]
            self.state = "CPU"
            
    #ticks the timers in the process based on where it is located
    def tick(self):
        if self.location == "CPU":
            if self.responce == -1:
                self.responce = self.tr
            self.timeincpu += 1
            self.tr += 1
            self.cburst -= 1
            self.update()
            return
        
        if self.location == "IO":
            self.ioburst -= 1
            self.tr += 1
            self.update()
            return
            
        if self.location == "RQ":
            self.tr += 1
            self.wait += 1
            self.update()
            return
        
    #getters
    def get_tq(self):
        return self.tq
    
    def get_time(self):
        return self.timeincpu
    
    def get_id(self):
        return self.pid
    
    def get_state(self):
        return self.state
    
    def get_location(self):
        return self.location
        
        
#define the idle process, this process is used when the CPU has no jobs available when
#it makes a job request, the idle process has a timeslice of 1, every tick the CPU will check
#to see if a new job is available.

idle = Process("IDLE",[999999999])

#Place for finished processes to go
class Completed:
    processes = []
    
    def add_process(p):
        Completed.processes.append(p)
    
    def done():
        if len(Completed.processes) == total_processes:
            return True
        else:
            return False

#define the IO Area for processes

class IO:
    #list of all processes currently in IO Area
    processes = []
    
    #tick the processes in IO Area
    def tick():
        for i in IO.processes:
            i.tick()
        
        for i in IO.processes:
            if sch.idx == "FCFS" and i.get_state() == "CPU":
                i.set_location("RQ")
                FCFS.add_process(i)
                IO.processes.remove(i)
                
            if sch.idx == "SJF" and i.get_state() == "CPU":
                i.set_location("RQ")
                SJF.add_process(i)
                IO.processes.remove(i)
                
            if sch.idx == "MFQ" and i.get_state() == "CPU":
                i.set_location("RQ")
                MFQ.add_process(i)
                IO.processes.remove(i)
     
    #add a process to the IO Area           
    def add_process(p):
        p.set_location("IO")
        IO.processes.append(p)
        
    def _print():
        print("=============== IO QUEUE =======================")
        if IO.processes == []:
            print ("[EMPTY]")
        for i in IO.processes:
            
            print(i.get_id() + " - IO Remaining = " + str(i.ioburst))
         
           
        print("================================================")

           
#define the First Come First Serve Queue      
class FCFS:
    #list of processes in the Queue
    processes = []
    idx = "FCFS"
    
    def add_process(p):
        p.set_location("RQ")
        if p.pid != "IDLE":
            FCFS.processes.append(p)
        else:
            return
    
    def get_next_process():
        
        if FCFS.processes != []:
            retval = FCFS.processes[0]
            retval.set_tq(9999)
            FCFS.processes = FCFS.processes[1:]
            
        elif FCFS.processes == []:
            retval = idle
        
        retval.set_location("CPU")
        return retval
    
    def _print():
        print("=============== FCFS READY LIST ================")
        if FCFS.processes == []:
            print("[EMPTY]")
        for i in FCFS.processes:
            print(i.pid + " remaining burst = " + str(i.cburst))
        
        print("================================================")
            
    def tick():
        for i in FCFS.processes:
            i.tick()      
    

#define the Shortest Job First Queue
class SJF:
    processes = []
    idx = "SJF"
    
    def add_process(p):
      p.set_location("RQ")
      if p.pid != "IDLE":
        SJF.processes.append(p)
      else:
         return   
     
    def get_next_process():
        if SJF.processes != []:
           retval = SJF.find_smallest_job()
           if retval in SJF.processes:
               SJF.processes.remove(retval)
           retval.set_location("CPU")
           retval.set_tq(9999)
           return retval
       
        elif SJF.processes == []:
            idle.set_location("CPU")
            idle.set_tq(1)
            return idle
    
    def find_smallest_job():
        jobsize = 99999
        job = idle
        for i in SJF.processes:
            if i.cburst < jobsize:
                job = i
                jobsize = i.cburst
        return job
    
    def _print():
        print("============= SJF READY QUEUE ==================")
        if SJF.processes == []:
            print("[QUEUE IS EMPTY]")
        for i in SJF.processes:
            print(i.pid + " remaining burst = " + str(i.cburst))
            
        print("=================================================")
            
    def tick():
        for i in SJF.processes:
            i.tick()

#define Multilevel Feedback Queue
class MFQ:
    Q1 = []
    Q2 = []
    Q3 = []
    idx = "MFQ"
    
    
    
    def add_process(p):
        p.set_location("RQ")
        if p.get_time() < 5 and p.get_id() != "IDLE": #if in CPU longer less than 5 ticks
            if p not in MFQ.Q1:
                MFQ.Q1.append(p)
        elif p.get_time() < 10 and p.get_id() != "IDLE": #else if in CPU less than 10 ticks
            if p not in MFQ.Q2:
               MFQ.Q2.append(p)
        elif p.get_id() != "IDLE": #else
            if p not in MFQ.Q3:
               MFQ.Q3.append(p)
        return
    
    def _print():
        print("========= MULTILEVEL FEEDBACK QUEUE READY LIST ========")
        print("Q1 ----------------------------------------------------")
        if MFQ.Q1 == []:
            print ("[EMPTY]")
        for i in MFQ.Q1:
            print(i.pid + " remaining burst = " + str(i.cburst))
        print("-------------------------------------------------------")
        print("Q2-----------------------------------------------------")
        if MFQ.Q2 == []:
            print ("[EMPTY]")
        for i in MFQ.Q2:
            print(i.pid + " remaining burst = " + str(i.cburst))
        print("-------------------------------------------------------")        
        print("Q3-----------------------------------------------------")
        if MFQ.Q3 == []:
            print ("[EMPTY]")
        for i in MFQ.Q3:
            print(i.pid + " remaining burst = " + str(i.cburst))
        print("-------------------------------------------------------")
        print("=======================================================")
        
    def get_next_process():
        retval = idle
        if MFQ.Q1 != []:
            retval = MFQ.Q1[0]
            MFQ.Q1 = MFQ.Q1[1:]
            retval.set_location("CPU")
            retval.set_tq(5 - retval.get_time())
            return retval
        elif MFQ.Q2 != []:
            retval = MFQ.Q2[0]
            MFQ.Q2 = MFQ.Q2[1:]
            retval.set_location("CPU")
            retval.set_tq(10 - retval.get_time())
            return retval
        elif MFQ.Q3 != []:
            retval = MFQ.Q3[0]
            MFQ.Q3 = MFQ.Q3[1:]
            retval.set_location("CPU")
            retval.set_tq(99999)
            return retval
        else:
            idle.set_location("CPU")
            idle.set_tq(1)
            return idle
    def went_to_io(p):
        if p.get_id() in MFQ.Q1V:
            MFQ.Q1V.remove(p.get_id())
        if p.get_id() in MFQ.Q2V:
            MFQ.Q2V.remove(p.get_id())
    
    
    def tick():
        for i in MFQ.Q1:
            i.tick()
        for i in MFQ.Q2:
            i.tick()
        for i in MFQ.Q3:
            i.tick()
            
#Processor Class, this class is the workhorse , responcible for making logic descions and calling
#methods of all other classes.
class Processor:
    def __init__(self):
        self.currentprocess = idle
        self.current_tq = 0
        self.total_ticks = 0
        self.idle_ticks = 0
        
    def _print(self):
        print("============= PROCESSOR INFO =======================")
        print("Current t[q] = " + str(self.current_tq))
        print("Current Process : " + self.currentprocess.get_id())
        print("Idle ticks : " + str(self.idle_ticks))
        print("Total ticks : " + str(self.total_ticks))
        print("=====================================================")
        
    def tick(self):
         #code to do context switching
        needsnew = False
        sent_to_io = False
        
        if self.currentprocess.get_state() == "IO":
            self.currentprocess.set_location("IO")
            IO.add_process(self.currentprocess)
            
            #this code below resets the priority of the process everytime it goes
            #to IO, commented out because reduced performance of the MFQ
            '''
            if scheduler == "MFQ":
                MFQ.went_to_io(self.currentprocess)
            '''
            needsnew = True
            sent_to_io = True
        
        if self.currentprocess.get_state() == "DONE":
            self.currentprocess.set_location("DONE")
            Completed.add_process(self.currentprocess)
            needsnew = True
        
        if self.current_tq <= self.currentprocess.get_time() and sent_to_io == False:
            if sch.idx == "FCFS":
                self.currentprocess.set_location("RQ")
                FCFS.add_process(self.currentprocess)
                needsnew = True
            if sch.idx == "SJF":
                self.currentprocess.set_location("RQ")
                SJF.add_process(self.currentprocess)
                needsnew = True
                
            if sch.idx == "MFQ":
                self.currentprocess.set_location("RQ")
                MFQ.add_process(self.currentprocess)
                needsnew = True
            
        
        if needsnew and sch.idx == "FCFS":
            self.currentprocess = FCFS.get_next_process()
            self.currentprocess.set_location("CPU")
            self.current_tq = self.currentprocess.get_tq()
        
        if needsnew and sch.idx == "MFQ":
            self.currentprocess = MFQ.get_next_process()
            self.currentprocess.set_location("CPU")
            self.current_tq = self.currentprocess.get_tq()
        
        if needsnew and sch.idx == "SJF":
            self.currentprocess = SJF.get_next_process()
            self.currentprocess.set_location("CPU")
            self.current_tq = self.currentprocess.get_tq()
        
        #context switching is done now, do 1 unit of work
        self.currentprocess.tick()
        self.total_ticks += 1
        if self.currentprocess.get_id() == "IDLE":
            self.idle_ticks += 1
        #print information on context switch    
        
        if needsnew and total_processors == 1:
            print("----------------------CONTEXT SWITCH-----------------------")
            self._print()
            self.currentprocess._print()
            IO._print()
            sch._print()
        
#Start of Simulation Code
            
sch = FCFS #set scheduler to use
total_processors = 1 # number of processors, context switching is only displayed
#when processors == 1
total_processes = 8 #total number of processes, this is how the completed queue knows when all
#jobs are finished

processors = []
    
#define processes
p1 = Process("P1", [5, 27, 3, 31, 5, 43, 4, 18, 6, 22, 4, 26, 3, 24, 4])
p2 = Process("P2",[4, 48, 5, 44, 7, 42, 12, 37, 9, 76, 4, 41, 9, 31, 7, 43, 8])
p3 = Process("P3",[8, 33, 12, 41, 18, 65, 14, 21, 4, 61, 15, 18, 14, 26, 5, 31, 6])
p4 = Process("P4",[3, 35, 4, 41, 5, 45, 3, 51, 4, 61, 5, 54, 6, 82, 5, 77, 3])
p5 = Process("P5",[16, 24, 17, 21, 5, 36, 16, 26, 7, 31, 13, 28, 11, 21, 6, 13, 3, 11, 4])
p6 = Process("P6",[11, 22, 4, 8, 5, 10, 6, 12, 7, 14, 9, 18, 12, 24, 15, 30, 8])
p7 = Process("P7",[14, 46, 17, 41, 11, 42, 15, 21, 4, 32, 7, 19, 16, 33, 10])
p8 = Process("P8",[4, 14, 5, 33, 6, 51, 14, 73, 16, 87, 6])

#add processes to scheduler
sch.add_process(p1)
sch.add_process(p2)
sch.add_process(p3)
sch.add_process(p4)
sch.add_process(p5)
sch.add_process(p6)
sch.add_process(p7)
sch.add_process(p8)



#initialize processor objects
for i in range(0,total_processors):
    proc = Processor()
    processors.append(proc)


while not Completed.done():
#for i in range(0,275): #testing for a set number of ticks
   for i in processors: #tick processors
       i.tick()
   IO.tick() #tick IO Queue
   sch.tick() #tick Ready Queue


      
#calculate utilization and process statistics
sumwait = 0
sumtr = 0
sumresp = 0

sumtotalticks = 0
sumidleticks = 0


for i in processors:
    sumtotalticks += i.total_ticks
    sumidleticks += i.idle_ticks

#calculate utilization by working_ticks / total_ticks
utilization = (sumtotalticks - sumidleticks) / sumtotalticks
    
#print info for all completed processes
print("===========COMPLETED PROCESS INFORMATION================")
for i in Completed.processes:
    i._print()
    sumwait += i.wait
    sumtr += i.tr
    sumresp += i.responce
print("===========END OF COMPLETED PROCESS INFORMATION =========")
        
    
sumwait = sumwait / total_processes
sumtr = sumtr / total_processes
sumresp = sumresp / total_processes
    
print("CPU UTILIZATION = " + str(round(utilization * 100,2)) + "%")
print("AVERAGE WAIT TIME = " +str(sumwait))
print("AVERAGE TURNAROUND = " +str(sumtr))
print("AVERAGE RESPONCE TIME = " +str(sumresp))

#print info for idle process
idle._print()
