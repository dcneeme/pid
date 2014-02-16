''' vent.py
    controlling EC-ventilators via ModbusRTU
'''
# last change 09.01.2014

from pymodbus.client.sync import ModbusTcpClient as ModbusClient # modbusTCP
client = ModbusClient(method='rtu', stopbits=1, bytesize=8, parity='E', baudrate=19200, timeout=0.2, port='/dev/ttyAPP0') # change if needed


class Vent:
    """ Communication with ventilation related EC-motor.
    """

    def __init__(self, unit = 2, SPEEDREGISTER = 0xD114, ERRORREGISTER = 0xD182, SERIALREGISTER = 0xD1A2):
        self.unit = unit
        self.speed_register = SPEEDREGISTER
        self.error_register = ERRORREGISTER
        self.serial_register = SERIALREGISTER
        
    
    def set_speed(self, speed): # max value is FFFF, 4 lower bits are insignificant!
        """ Set the ventilator speed
        """
        result = client.write_register(address = self.speed_register, value = setPoint, unit = self.unit)
        return result
        
    def get_error(self): # content of the error register
        ''' check error register '''
        error = client.read_holding_registers(address = self.error_register, count = 1, unit = self.unit) #
        return error
        
    def get_serial(self): # serialnumber of the ventilator
        ''' check error register '''
        serial = client.read_holding_registers(address = self.serial_register, count=1, unit = self.unit) #
        return serial
    
    