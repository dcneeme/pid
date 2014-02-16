#-------------------------------------------------------------------------------
# threestep.py
# droid4control.com 2014
# depending on the difference of the setpoint and actual value (error), one or another output
# is activated for a time, depending on the error. 
# there class must be called not too often, only on times the output can be activated
# giving time for maximum pulse to be over before next call. 
# it produces no output if called before the end of ongoing pulse! 

# the first output value is given to start a motor running pulse given the pulse length in seconds. negative value means 'lower' direction
# the second output value is to indicate the state of ongoing pulse, if any. value 1 means running towards 'higher', -1 to lower, 0 means motort stopped.
# the third output value signals about possibly reaching the hi or lo limit for traveling, 
# due to cumulative running time in one direction has been higher than running time to the other by more than the motor_time).
#
# the needed parameter are: setpoint, actual, motor_time (s), maxpulse_time (s), maxpulse_error, 
#  minpulse_time (s), minpulse_error. the two last ones define the dead-zone (with no output).
#
#usage
#from threestep import *
#f=ThreeStep(setpoint=3)
#print f.output(10) # actual as parameter, outputs length if pulse must be started, state and onlimit values -1...1

# last change 08.02.2014
# reset runtime and reset pulse should be added?


import time

class ThreeStep:
    """ Three-step motor control.
        Outputs pulse length to run the motor in one or another direction
    """
    def __init__(self, setpoint = 0, motortime = 100, maxpulse = 10, maxerror = 100, minpulse =1 , minerror = 1, runperiod = 20):
        self.setSetpoint(setpoint)
        self.setMotorTime(motortime)
        self.setMaxpulseLength(maxpulse)
        self.setMaxpulseError(maxerror)
        self.setMinpulseLength(minpulse)
        self.setMinpulseError(minerror)
        self.setRunPeriod(runperiod)
        
        self.Initialize() 
        
        
    def setSetpoint(self, invar):
        """ Set the setpoint for the actual value """
        self.Setpoint = invar

    def setMotorTime(self, invar):
        """ Sets motor running time in seconds to travel from one limit to another 
        (give the bigger value if the travel times are different in different directions)
        """
        self.MotorTime = abs(invar)

    def setMaxpulseLength(self, invar):
        """ Sets maximum pulse time in seconds to use """
        self.MaxpulseLength = abs(invar)
    
    def setMaxpulseError(self, invar):
        """ Ties maximum error to maximum pulse length in seconds to use. 
        That also defines the 'sensitivity' of the relation between the error and the motor reaction      
        """
        self.MaxpulseError = abs(invar)
        
    def setMinpulseLength(self, invar):
        """ Sets minimum pulse length in seconds to use """
        self.MinpulseLength = abs(invar)
        
    def setMinpulseError(self, invar):
        """ Ties the minimum pulse length to the error level. This also sets the dead zone, 
        where there is no output (motor run) below this (absolute) value on either direction """
        self.MinpulseError = abs(invar) 
        
    def setRunPeriod(self, invar):
        """ Sets the time for no new pulse to be started """
        self.RunPeriod = abs(invar) 
        
    
    def Initialize(self):
        """ initialize time dependant variables
        """
        self.currtime = time.time()
        #self.prevtime = self.currtime
        self.last_start = self.currtime - self.RunPeriod - 1 # this way we are ready to start a new pulse if needed
        self.last_length = 0 # positive or negative value means signal to start pulse with given length in seconds. 0 means no pulse start
        self.last_state = 0 # +1 or -1 value means signal to start pulse with given length in seconds
        self.last_limit = 0 # value 0 for means travel position between limits, +1 on hi limit, -1 on lo limit
        self.runtime = 0 # cumulative runtime towards up - low
        self.onLimit = 0
        
        

    def extrapolate(self, x, x1 = 0, y1 = 0, x2 = 0, y2 = 0):
        """ Returns extrapolated value y based on x and two points defined by x1y1 and x2y2 """ 
        if y1 != y2: # valid data to avoid division by zero
            return y1+(x-x1)*(y2-y1)/(x2-x1)
        else:
            return None
            
            
    def output(self, invar): # actual as parameter
        """ Performs pulse generation if needed and if no previous pulse is currently active.
        Returns output values for pulse length, running state and reaching the travel limit. 
        All output values can be either positive or negative depending on the direction towards higher or lower limit.
        If error gets smaller than minpulse during the nonzero output, zero the output state.
        """
        try:
            error=self.Setpoint - invar            # error value
        except:
            error=0 # for the case of invalid actual
            msg='invalid actual '+repr(invar)+' for threestep error calculation, error zero used!'
            print(msg)
            
        #error=self.Setpoint - invar            # current error value
        self.currtime = time.time()               # get current time
        state=0 # pulse level, not known yet
        
        #current state, need to stop? level control happens by calling only!
        if self.currtime > self.last_start + abs(self.last_length) and self.last_state != 0: # need to stop ##########  STOP ##############
            #print('need to stop ongoing pulse due to pulse time (',abs(self.last_length),') s out') # debug
            if self.onLimit == 0 or (self.onLimit == -1 and error > 0) or (self.onLimit == 1 and error < 0): # modify running time
                self.runtime = self.runtime + self.last_state*(self.currtime - self.last_start) # sign via state is important
            state = 0 # stop the run
            self.last_state = state
            print('threestep: stopped pulse, cumulative travel time',int(self.runtime))
        
        if self.runtime > self.MotorTime: # limit
            self.onLimit = 1 # reached hi limit
            self.runtime = self.MotorTime
            print('reached hi limit') # debug
            
        if self.runtime < -self.MotorTime: # limit
            self.onLimit = -1 # reached lo limit
            self.runtime = -self.MotorTime
            print('reached lo limit') # debug
                
        #need to start a new pulse? chk runPeriod 
        if self.currtime > self.last_start + self.RunPeriod and self.last_state == 0: # free to start next pulse (no ongoing)
            #print('no ongoing pulse, last_state',self.last_state,'time from previous start',int(self.currtime - self.last_start)) # debug
            if abs(error) > self.MinpulseError: # pulse is needed
                print('threestep: new pulse needed due to error vs minpulseerror',error,self.MinpulseError) # debug
                if error > 0 and error > self.MinpulseError: # pulse to run higher needed
                    length = self.extrapolate(error, self.MinpulseError, self.MinpulseLength, self.MaxpulseError, self.MaxpulseLength)
                    self.last_length = length
                    self.last_start = self.currtime
                    state = 1
                    print('threestep: started pulse w len',length) # debug
                elif error < 0 and error < -self.MinpulseError: # pulse to run lower needed
                    length = self.extrapolate(error, -self.MinpulseError, -self.MinpulseLength, -self.MaxpulseError, -self.MaxpulseLength)
                    self.last_length = length
                    self.last_start = self.currtime
                    state = -1
                    print('threestep: started pulse w len',length) # debug
            else: # no need for a new pulse
                length = 0
                #print('no need for a pulse due to error vs minpulseerror',error,self.MinpulseError) # debug
        else: # no new pulse yet or pulse already active
            length = 0
            state = self.last_state
            msg='pulse last start '+str(int(self.currtime - self.last_start))+' s ago, runperiod '+str(self.RunPeriod)+', cumulative travel time '+str(int(self.runtime)) # debug
            #print(msg)
            #syslog(msg) # debug
        
        
        #if abs(error) < self.MinpulseError and state != 0: # stop the ongoing pulse - not strictly needed
        #    state = 0 # if the actual drive to the motor happens via timer controlled by length previously output, this does not have any effect
        #    print('stop the ongoing pulse') # debug
        
        pulseleft=int(self.last_start + abs(self.last_length) - self.currtime)
        if state != 0 and pulseleft > 0:    
            msg='ongoing pulse time left '+str(pulseleft)+', state (direction) '+str(state) # debug
            #print(msg)
            #syslog(msg) # debug
        
        
        if state != self.last_state:
            self.last_state = state
        
        msg='sp '+str(self.Setpoint)+', actual '+str(invar)+', error '+str(error) # debug
        print(msg)
        #syslog(msg)
        return length, state, self.onLimit, int(self.runtime)
