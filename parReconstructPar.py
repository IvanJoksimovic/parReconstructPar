import os
import numpy as np
import multiprocessing
from multiprocessing import Process

def applyOpenFOAMreconstructPar(times,procNo):

	i = 1

	for t in times:
		print("Processor {0} : Reconstructing time {1} , {2} of {3}".format(procNo,t,i,len(times)))
		os.system("reconstructPar -time {0} > logProcessor_{1}".format(t,procNo))
		i+=1


os.system("rm -rf ./logProcessor*")
os.system("foamListTimes -processor > logProcessorTimes")
allProcessorTimes = np.genfromtxt("./logProcessorTimes")

nProcs = 8

processorTimes = np.array_split(allProcessorTimes,nProcs)
#print(processorTimes)

processes = []
for i in range(0,nProcs):
	p = Process(target = applyOpenFOAMreconstructPar,args = (processorTimes[i],i,))
	processes.append(p)

for p in processes:
	p.start()

for p in processes:
	p.join()

print("IVAN: all done!")



