#-------------------------------------------------------------------------------
# PID.py
# A simple implementation of a PID controller
#-------------------------------------------------------------------------------
# Example source code for the book "Real-World Instrumentation with Python"
# by J. M. Hughes, published by O'Reilly Media, December 2010,
# ISBN 978-0-596-80956-0.
#-------------------------------------------------------------------------------
# modified by droid4control.com 2014, introducing limit control and reset integral
#
# usage example:
# from PID import *
# f2=PID(SP=20, min=-100, max=100)
# f1=PID(SP=10, min=-100, max=100)
# f1.output(11)
# (-15.375, -2.0, -13.375, -0.0, -1, 0) # returns output, p, i , d, e, onLimit


import time

class PID:
    """ Simple PID control.
        This class implements a simplistic PID control algorithm.
    """
    def __init__(self, SP=0, P=2.0, I=1.0, D=0.0, min=-9999, max=9999): # initialize gains
        self.Kp=P
        self.Ki=I
        self.Kd=D
        self.setPoint=SP
        self.Min=min
        self.Max=max
        self.Initialize()

    def setKp(self, invar): # Set proportional gain
        self.Kp = invar

    def setKi(self, invar): # Set integral gain
        self.Ki = invar
        
    def resetIntegral(self): # reset integral part
        self.Ci = 0

    def setKd(self, invar): # Set derivative gain
        self.Kd = invar

    def setPrevErr(self, preverr): # Set previous error value
        self.prev_err = preverr
        
    def setMin(self, outMin): # Set lower limit for output
        self.Min = outMin

    def setMax(self, outMax): # Set lower limit for output
        self.Max = outMax
        
    def setSetpoint(self, setPoint): # Set lower limit for output
        self.setPoint = setPoint

    def Initialize(self): # initialize delta t variables
        self.currtm = time.time()
        self.prevtm = self.currtm
        self.prev_err = 0
        #self.setpoint = 0
        self.onLimit=0 # value 0 means between limits, 1 on lo limit, 2 on hi limit
        
        # term result variables
        self.Cp = 0
        self.Ci = 0
        self.Cd = 0


    def output(self, actual):
        """ Performs a PID computation and returns a control value based on
            the elapsed time (dt) and the difference between actual vaue and setpoint.
        """
        error=self.setPoint - actual            # error value
        self.currtm = time.time()               # get t
        dt = self.currtm - self.prevtm          # get delta t
        de = error - self.prev_err              # get delta error

        self.Cp = self.Kp * error               # proportional term
        if self.onLimit == 0 or (self.onLimit ==1 and error>0) or (self.onLimit == 2 and error<0): # no limit reached or moving away from limit
            self.onLimit=0
            self.Ci += error * dt                   # integral term
        
        self.Cd = 0
        if dt > 0:                              # no div by zero
            self.Cd = de/dt                     # derivative term

        self.prevtm = self.currtm               # save t for next pass
        self.prev_err = error                   # save t-1 error

        # sum the terms and return the result
        Output=self.Cp + (self.Ki * self.Ci) + (self.Kd * self.Cd)
        if Output > self.Max:
            self.onLimit=2 # reached hi limit
            Output=self.Max
        if Output < self.Min:
            self.onLimit=1 # reached lo limit
            Output=self.Min
           
        return Output,self.Cp,(self.Ki * self.Ci),(self.Kd * self.Cd),error,self.onLimit # [out,p,i,d,e,limit]
         