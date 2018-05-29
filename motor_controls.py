"""

Collection of tools used to control a linear actuator powered by an Mdrive23
stepper motor

"""

import serial
from time import sleep
import numpy as np

#%%

class Motor(object):
      def __init__(self, port):
            """ Opens motor connection and initializes motor variables """
            
            self.con = serial.Serial(port, 9600, timeout=0, writeTimeout=0)
            sleep(1)
            self.load_settings()
            
            self.maxvel = 8000
            self.xlim = 139877
            
      def close(self):
            """ Closes motor connection """
            
            self.con.close()
            

      ######################
      # Commands
      ######################
      def send_command(self, commandstr):
            """ Sends text command to motor (mcode language) """
            
            self.con.write((commandstr + '\r\n').encode())
            
      def set_variable(self, var, val):
            """ Sets the value of a motor variable """
            
            command = var + ' ' + val
            self.send_command(command)
            sleep(0.1)
            
      def clear_errors(self):
            """ Clears motor error code """
            
            self.set_variable('ER', '0')
            sleep(0.1)
            
      ######################
      # Reading outputs
      ######################
      
      def read_output(self):
            """ Returns motor output buffer as lsit of lines """\
            
            raw_output = self.con.readlines()
            strlines = [line.decode()[:-2] for line in raw_output]
            
            return strlines
      
      def read_system_variables(self):
            """ Returns dictionary of current motor variables """
            
            # send command and read result
            self.send_command('PR AL')
            sleep(1)
            varstrs = self.read_output()[:-1]
            
            # process motor output
            varlist = [[varstr[:varstr.find(' ')],
                        varstr[varstr.find(' ')+3:]]
                       for varstr in varstrs]
            
            self.vardict = {name : val for name, val in varlist}
            
      
      def read_variable(self, var):
            """ Returns value of a specific variable specified by var """
            
            self.con.flushInput()
            self.send_command('PR ' + var)
            sleep(0.1)
            val = self.read_output()[-1]
            return val
      
      def errorcode(self):
            """ Returns most recent error code """
            
            return self.read_variable('ER')


      ######################
      # Initialization
      ######################

      def load_settings(self):
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
                
            # Load variables
            self.read_system_variables()
            
            
            # Load settings from text file
            with open('motor_settings.txt', 'r') as f:
                  settingstrs = [line[:-1] for line in f.readlines()]
            
            setlist = [[setstr[:setstr.find(' ')], 
                                  setstr[setstr.find(' ')+ 3 :]]
                                 for setstr in settingstrs]
      
            self.setdict = {name : val for name, val in setlist}
            
            
            # Compare and set important variables if different
            for key in self.setdict:
                  if self.vardict[key] != self.setdict[key]:
                        self.set_variable(key, self.setdict[key])
                  else:
                        pass

      ######################
      # Movement
      ######################
      
      def move_to_switch(self, switch):
            """ Sends cart to switch
            
                  -1: limit minus
                  0: home
                  1: limit plus
            
            """
            
            if switch == 0:
                  motor.send_command('HM 3')
            elif np.abs(switch) == 1:
                  command = 'SL ' + str(switch * self.maxvel)
                  motor.send_command(command)
            else:
                  raise Exception('Must specify switch -1, 0, or 1')
      
      def wait(self):
            """ delays until cart movement is complete """
            
            while int(self.read_variable('MV')):
                  pass
      
                  
      def initialize_coordinates(self):
            """ finds range of switches and sets zero position """
            
            self.move_to_switch(-1)
            self.wait()            
            self.send_command('MR {}'.format(self.maxvel))
            self.wait()
            self.set_variable('P', '0')
            self.move_to_switch(1)
            self.wait()
            self.send_command('MR -{}'.format(self.maxvel))
            self.xlim = int(self.read_variable('P'))
            
      def to_origin(self, reverse=False):
            """ Sends cart to origin unlese reverse == false, 
            in which case cart is sent to xlim """
            self.set_variable('VM', str(self.maxvel))
            
            if reverse == True:
                  origin = self.xlim
            elif reverse == False:
                  origin = 0
            
            self.send_command('MA {}'.format(origin))
            
            self.wait()
            
      
      def scan(self, reverse=True, scanvel=2000, retvel=8000):
            """ Performs single scan at velocity = scanvel then returns to 
            appropriate origin in anticipation of another scan.
            Assumes position is already at correct origin."""
            
            self.set_variable('VM', str(scanvel))
            
            if reverse == True:
                  scanext = 0
            elif reverse == False:
                  scanext = self.xlim
            
            self.send_command('MA {}'.format(scanext))
            self.wait()
            self.to_origin(reverse=reverse)
      
#%%

motor = Motor('COM3')
#%%
motor.to_origin(reverse=False)
motor.scan(reverse=False, scanvel=4000)
#%%
motor.to_origin(reverse=True)
motor.scan(reverse=True, scanvel=4000)

#%%
motor.close()
      
      
      
      
      
      
      
      
      
      
      
      
      
