"""

Collection of tools for controlling camera flash trigger using a
Numato Labs 8 channel USB GPIO board

"""

import serial
from time import sleep

#%%

class Flash(object):
      def __init__(self, port):
            """"Open flash connection"""
            self.con = serial.Serial(port, 19200, timeout=1)
            sleep(1)
            self.con.write("gpio clear 0\r\n".encode())
      
      def fire(self):
            """ Fire flash and delay 0.1 seconds"""
            self.con.write("gpio set 0\r\n".encode())
            self.con.write("gpio clear 0\r\n".encode())

      def close(self):
            """ Close flash connection """
            self.con.close()
            sleep(1)