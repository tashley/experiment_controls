"""

Collection of tools used to control a linear actuator powered by an Mdrive23
stepper motor

"""

import serial
from time import sleep

#%%

ser = serial.Serial('COM3', 9600, timeout=0, writeTimeout=0)

#%%
ser.write('mr -8000\r\n'.encode())


#%%
ser.close()



# motor = Motor('COM3')
# motor.initialize()

# flash = Flash('COM5')


# for i in nits:
      # flash.fire()
      # motor.run_profile(upspeed, downspeed)
