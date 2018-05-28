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
                fixes errors if not. """
            
            with open('motor_settings.txt', 'r') as f:
                  settingstrs = [line[:-1] for line in f.readlines()]
            
            setlist = [[setstr[:setstr.find(' ')], 
                                  setstr[setstr.find(' ')+ 3 :]]
                                 for setstr in settingstrs]
      
            setdict = {name : val for name, val in setlist}
            
            return setdict
            
#%%

motor = Motor('COM3')
#%%


motor.read_variables()

#%%
motor.close()

#%%
with open('motor_settings.txt', 'r') as f:
      settingstrs = f.readlines()