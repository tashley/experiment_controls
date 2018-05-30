# -*- coding: utf-8 -*-

"""

GUI tools for experiments

Tom Ashley
tashley22@gmail.com
5/29/2018

"""

from flash_controls import Flash
from motor_controls import Motor
from time import sleep
import datetime as dt

class Experiment(object):
      def __init__(self, reset_coordinates=False, scan_upstream=True,
                   scanspeed=3, returnspeed=3,
                   startflash=True, endflash=True):
            
            """
            Initializes experiment with the following settings:
            
            reset_coordinates: True runs coordinate initialization routine
                               before starting experiment
            scan_upstream:     Scan in upsream direction if True
            scanspeed:         Cart speed in cm/s for scan
            returnspeed:       Cart speed in cm/s for return
            startflash:        Flashes before scan if True
            endflash:          Double flash after scan if True
            
            """
      
            self.flash = Flash('COM6')
            self.motor = Motor('COM3')
            
            self.scanspeed = scanspeed * 800
            self.returnspeed = returnspeed * 800
            self.startflash = startflash
            self.endflash = endflash
            
            if reset_coordinates:
                  self.motor.initialize_coordinates()
            else:
                  pass
            
            if scan_upstream:
                  self.scandir = 0
            else:
                  self.scandir = 1
                  
      def scan(self):
            """ Runs scan including flashes if specified """
            if self.startflash:
                  self.flash.fire()
            
            self.motor.move(self.scandir, self.scanspeed)
            if self.motor.stalled():
                  print('Stalled on scan at position {}'.format(
                              self.motor.read_variable('P')))
            
            if self.endflash:
                  self.flash.fire()
                  sleep(2)
                  self.flash.fire()
        
      def to_scan_origin(self):
            """ Returns motor to origin at returnspeed """
            
            self.motor.move(abs(self.scandir - 1), self.returnspeed)
            
            if self.motor.stalled():
                  print('Stalled on move to origin at position {}'.format(
                              self.motor.read_variable('P')))
      
      
      def run_experiment(self, duration):
            """ 
            Scans bed for the specified duration using initial settings.
            duration is in seconds.
            
            """
            
            self.to_scan_origin()
            
            self.start_time = dt.datetime.now()
            self.end_time = self.start_time + dt.timedelta(0, duration)
            
            counter = 1
            while dt.datetime.now() < self.end_time:
                  print('Starting scan {}'.format(counter))
                  self.scan()
                  self.to_scan_origin()
                  counter +=1

      def close(self):
            self.motor.close()
            self.flash.close()

#%%
experiment = Experiment(reset_coordinates=False, scan_upstream=True,
                   scanspeed=3, returnspeed=10,
                   startflash=True, endflash=True)
#%%
experiment.run_experiment(60)
            
            
            
            
            
      
      