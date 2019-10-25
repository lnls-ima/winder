"""Widget for the control tab."""

# import sys as _sys
# import traceback as _traceback
from qtpy.QtWidgets import (
    QWidget as _QWidget,
#     QMessageBox as _QMessageBox,
    )
from qtpy.QtCore import (
    QTimer as _QTimer,
    )
import qtpy.uic as _uic

from winder.gui.utils import get_ui_file as _get_ui_file
from winder.devices import mdriver as _mdriver
from winder.data import config as _config


class ControlWidget(_QWidget):
    """Control Widget class for the winder GUI."""

    def __init__(self, parent=None):
        """Set up the ui."""
        super().__init__(parent)

        # setup the ui
        uifile = _get_ui_file(self)
        self.ui = _uic.loadUi(uifile, self)

        self.mdriver = _mdriver
        self.config = _config

        self.counter_timer = _QTimer()
        self.update_time = 20
        self.counts = 0.0  # current number of turns

        # connect signals and slots
        self.connect_signals_slots()

    def connect_signals_slots(self):
        """Create signal and slots connections."""
        self.ui.pbt_zero.clicked.connect(self.clear_counter)
        self.ui.pbt_jog_n.pressed.connect(self.jog_negative)
        self.ui.pbt_jog_n.released.connect(self.stop)
        self.ui.pbt_jog_p.pressed.connect(self.jog_positive)
        self.ui.pbt_jog_p.released.connect(self.stop)
        self.ui.pbt_on.clicked.connect(self.on)
        self.ui.pbt_off.clicked.connect(self.off)
        self.counter_timer.timeout.connect(self.update_counter)

    def clear_counter(self):
        """Sets current position as zero and clears lcd counter."""
        self.counts = 0.0
        self.ui.lcd_turn_counter.display(0)
        self.mdriver.set_position(motor=0, position=0)
        self.mdriver.set_position(motor=1, position=0)

    def update_counter(self):
        """Updates the lcd turn counter."""
        pos = self.mdriver.read_positions()[0]
        self.counts = pos / (self.config.steps0 * self.config.usteps0)
        if self.counts >= self.config.nturns:
            self.stop()
            self.counter_timer.stop()
        self.ui.lcd_turn_counter.display(self.counts)

    def jog_negative(self):
        """Unwind the coil."""
        self.counter_timer.start(self.update_time)
        _motors = [1, 1, 0, 0, 0, 0, 0, 0]
        _i = self.ui.cmb_motor.currentIndex()
        if _i == 1:
            _motors[1] = 0
        elif _i == 2:
            _motors[0] = 0
        self.mdriver.jog(motor=0, spd=self.config.spd0, pos_direction=False)
        self.mdriver.jog(motor=1, spd=self.config.spd1, pos_direction=False)
        self.mdriver.begin_motion(_motors)

    def jog_positive(self):
        """Wind the coil."""
        self.update_counter()
        if self.counts < self.config.nturns:
            self.counter_timer.start(self.update_time)
            _motors = [1, 1, 0, 0, 0, 0, 0, 0]
            _i = self.ui.cmb_motor.currentIndex()
            if _i == 1:
                _motors[1] = 0
            elif _i == 2:
                _motors[0] = 0
            self.mdriver.jog(motor=0, spd=self.config.spd0, pos_direction=True)
            self.mdriver.jog(motor=1, spd=self.config.spd1, pos_direction=True)
            self.mdriver.begin_motion(_motors)

    def stop(self):
        """Stops all motor movement."""
        self.counter_timer.stop()
        self.mdriver.stop(-1)

    def on(self):
        """Turns on the motors."""
        self.mdriver.enable_motor(motor=0)
        self.mdriver.enable_motor(motor=1)

    def off(self):
        """Turns off the motors."""
        self.mdriver.disable_motor(motor=0)
        self.mdriver.disable_motor(motor=1)
