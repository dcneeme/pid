# modbus2sql.py
# synchronizes the modbus register with sqlite tables in the following relations:
# di registers -> dichannels
# dochannels -> do registers, di register usage needed for feedback
# ai registers -> aichannels
# aochannels -> ao registers (if any), ai register usage needed for feedback
#setup -> setup registers (close to ao in behaviour)

class MBSQL:

    def __init__(self, ): # initialize
        self.Initialize()
