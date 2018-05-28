"""

Collection of tools for controlling camera flash trigger using a
Numato Labs 8 channel USB GPIO board

"""

import serial
from time import sleep

#%%

ser = serial.Serial('COM6', 19200, timeout=1)


#%%

ser.write("gpio set 0\r\n".encode())
sleep(0.5)
ser.write('gpio clear 0\r\n'.encode())
 #%%
ser.close()