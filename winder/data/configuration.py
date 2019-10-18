"""Winder configuration module."""

import sys as _sys
import traceback as _traceback


class WinderConfig():
    """Winder configuration parameters class."""

    def __init__(self):
        # General configuration
        self.config = ''
        self.spd = 0.0  # winding speed in rev/s
        self.ac = 0.0  # winding acceleration in rev/s^2
        self.lc = 0.0  # coil lengh in mm
        self.d = 0.0  # wire diameter in mm
        self.nturns = 0  # number of turns

        # Galil configuration
        self.ip = '10.0.28.113'

        # Motor0 configuration
        self.spd0 = 0  # counts/s
        self.ac0 = 0  # counts/s^2
        self.mtype0 = 2  # step direction
        self.steps0 = 200  # steps/rev
        self.usteps0 = 64  # usteps/step

        # Motor1 configuration
        self.spd1 = 0  # counts/s
        self.ac1 = 0  # counts/s^2
        self.mtype1 = -2  # step direction
        self.steps1 = 200  # steps/rev
        self.usteps1 = 64  # usteps/step

    def motor_calculus(self):
        """Estimates motors speed and acceleration."""

        try:
            # Coil
            _turns_per_layer = self.lc/self.d

            # Motor0
            _cnts_per_rev0 = self.steps0*self.usteps0
            self.spd0 = self.spd*_cnts_per_rev0
            self.ac0 = self.ac*_cnts_per_rev0

            # Motor1
            _cnts_per_rev1 = self.steps1*self.usteps1
            _ratio = (0.5*_cnts_per_rev1)/(_turns_per_layer*_cnts_per_rev0)
            self.spd1 = _ratio*self.spd0
            self.ac1 = _ratio*self.ac0

        except Exception:
            print(_traceback.print_exc(file=_sys.stdout))
