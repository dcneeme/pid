# test3step
import sys
#print sys.argv

from threestep import *
f=ThreeStep(setpoint=int(sys.argv[1]))
print f.output(int(sys.argv[2])) # actual as parameter
