"""

Collection of tools used to control a linear actuator powered by an Mdrive23
stepper motor

"""

import serial
from time import sleep

#%%

class Motor(object):
      def __init__(self, port):
            """ Opens motor connection and initializes motor variables """
            
            self.con = serial.Serial(port, 9600, timeout=0, writeTimeout=0)
            sleep(1)
            self.read_variables()
            
            
      def close(self):
            """ Closes motor connection """
            
            self.con.close()
            
            
      def send_command(self, commandstr):
            """ Sends text command to motor (mcode language) """
            
            self.con.write((commandstr + '\r\n').encode())
            
            
      def read_output(self):
            """ Returns motor output buffer as lsit of lines """\
            
            raw_output = self.con.readlines()
            strlines = [line.decode()[:-2] for line in raw_output]
            
            return strlines
      
      
      def read_variables(self):
            """ Returns dictionary of current motor variables """
            
            # send command and read result
            motor.send_command('PR AL')
            sleep(1)
            varstrs = motor.read_output()[:-1]
            
            # process motor output
            varlist = [[varstr[:varstr.find(' ')],
                        varstr[varstr.find(' ')+3:]]
                       for varstr in varstrs]
            
            self.vardict = {name : val for name, val in varlist}
            
      
      
      def reload_settings(self):
            """ Checks to make sure initial motor settings are correct,
                fixes errors if not.

                Important variables:
                A: Acceleration (40000)
                D: Deceleration (40000)
                EE: Encoder enable (1)
                EM: Echo mode (2)
                ER: Error code (0)
                HC: Holding current (5)
                MT: Motor settling delay time (25)
                PM: Position maintenance enable (0)
                RC: Motor run current (90)
                S1: Switch 1 - Limit minus (3, 0, 1)
                S2: Switch 2 - Limit plus (2, 0, 1)
                S3: Switch 3 - Home (1, 0, 1)
                S7: Something about clocks (34, 0)
                S8: Something about clocks (34, 0)
                S13: Something about inputs (60, 0)
                VI: Initial velocity (40)
                VM: Maximum velocity (8000)


                """
            
            with open('motor_settings.txt', 'r') as f:
                  settingstrs = [line[:-1] for line in f.readlines()]
            
            setlist = [[setstr[:setstr.find(' ')], 
                                  setstr[setstr.find(' ')+ 3 :]]
                                 for setstr in settingstrs]
      
            setdict = {name : val for name, val in setlist}
            

            
            
#%%

motor = Motor('COM3')
#%%


motor.read_variables()

#%%
motor.close()

#%%
with open('motor_settings.txt', 'r') as f:
      settingstrs = f.readlines()