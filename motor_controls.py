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
            varnames = [varstr[:varstr.find(' ')] for varstr in varstrs]
            varvals = [varstr[varstr.find(' ')+3:] for varstr in varstrs]
            
            vardict = {name : val for name, val in zip(varnames, varvals)}
            
            return vardict
      
      
      def reload_settings(self):
            """ Checks to make sure motor settings are correct """
            
#%%

motor = Motor('COM3')
#%%


output = motor.read_variables()


#%%
motor.close()

#%%
with open('motor_settings.txt', 'r') as f:
      settingstrs = f.readlines()