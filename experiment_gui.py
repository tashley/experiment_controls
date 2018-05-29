# -*- coding: utf-8 -*-

"""

GUI tools for experiments

Tom Ashley
tashley22@gmail.com
5/29/2018

"""

from flash_controls import Flash
from motor_controls import Motor

class Experiment(object):
      def __init__(self):
            flash = Flash('COM6')
            motor = Motor('COM3')
      
      