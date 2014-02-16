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
# last change 08.02.2014

import time

class 3STEP:
    """ Three-step motor control.
        Outputs pulse length to run the motor in one or another direction
    """
    def __init__(self, setpoint = 0, motor_time =100, maxpulse_time = 100, maxpulse_error = 100, minpulse_time =1 , minpulse_error = 1, run_period = 200):
        self.setSetpoint(setpoint)
        self.setMotorTime(motor_time)
        self.setMaxpulseTime(maxpulse_time)
        self.setMaxpulseError(maxpulse_error)
        self.setMinpulseTime(minpulse_time)
        self.setMinpulseError(minpulse_error)
        self.setRunPeriod(run_period)
        
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
        self.MaxpulseLenght = abs(invar)
    
    def setMaxpulseError(self, invar):
        """ Ties maximum error to maximum pulse length in seconds to use. 
        That also defines the 'sensitivity' of the relation between the error and the motor reaction      
        """
        self.MaxpulseError = abs(invar)
        
    def setMinpulseLength(self, invar):
        """ Sets minimum pulse length in seconds to use """
        self.MinpulseLength = abs(invar)
        
    def setMinpulseError(self, invar):
        """ Ties the minimumm pulse length to the error level. This also sets the dead zone, 
        where there is no output (motor run) below this (absolute) value on either direction """
        self.MinpulseError = abs(invar) 
        
    def setRunPeriod(self, invar):
        """ Sets the time for no new pulse to be started """
        self.RunPeriod = abs(invar) 
        
    
    def Initialize(self):
        """ initialize time dependant variables
        """
        self.currtime = time.time()
        self.prevtime = self.currtime
        self.last_start = self.currtm - self.Motortime # this way we are ready to start a new pulse if needed
        self.last_length = 0 # positive or negative value means signal to start pulse with given length in seconds. 0 means no pulse start
        self.last_state = 0 # +1 or -1 value means signal to start pulse with given length in seconds
        self.last_limit = 0 # value 0 for means travel position between limits, +1 on hi limit, -1 on lo limit
        self.runtime = 0 # cumulative runtime towards up - low
        

    def extrapolate(x, x1 = 0, y1 = 0, x2 = 0, y2 = 0):
        """ Returns extrapolated value y based on x and two points defined by x1y1 and x2y2 """ 
        if y1 != y2: # valid data to avoid division by zero
            return y1+(x-x1)*(y2-y1)/(x2-x1)
        else:
            return None
            
            
    def output(self, actual):
        """ Performs pulse generation if needed and if no previous pulse is currently active.
        Returns output values for pulse length, running state and reaching the travel limit. 
        All output values can be either positive or negative depending on the direction towards higher or lower limit.
        """
        error=self.Setpoint - actual            # current error value
        self.currtm = time.time()               # get current time
        
        #current state, need to stop?
        if self.currtime > abs(last_length) and self.last_state != 0: # need to stop
            if self.onLimit == 0 or (self.onLimit == -1 and error > 0) or (self.onLimit == 1 and error < 0): # modify running time
                self.runtime = self.runtime + (self.currtime - self.prevtime)
                state = 0 # stop the run
                self.last_state = state
        
        if self.runtime > self.MotorTime:
            self.onLimit = 1 # reached hi limit
            self.runtime = self.MotorTime
            
        if self.runtime < -1*self.MotorTime:
            self.onLimit = -1 # reached lo limit
            self.runtime = -1*self.MotorTime
            
                
        #need to start a new pulse? chk runPeriod 
        if self.currtime > self.last_start + self.RunPeriod: # free to start next pulse
            if error > MinpulseError: # run higher needed
                length = extrapolate(error, MinpulseError, MinpulseLength, MaxpulseError, MaxpulseLength)
                state = 1
            elif error < -abs(MinpulseError): # run lower needed
                length = extrapolate(error, -MinpulseError, -MinpulseLength, -MaxpulseError, -MaxpulseLength)
                state = -1
            else: # no need for a new pulse
                length = 0
        else: # no new pulse yet
            length = 0
            state = self.last_state
        
        if state != self.laststate:
            self.laststate = state
            
        return length, state, self.onLimit
