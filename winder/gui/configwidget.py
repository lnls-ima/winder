"""Widget for the configuration tab."""

# import sys as _sys
# import traceback as _traceback
from qtpy.QtWidgets import (
    QWidget as _QWidget,
    QApplication as _QApplication,
#     QMessageBox as _QMessageBox,
    )
import qtpy.uic as _uic

from winder.gui.utils import get_ui_file as _get_ui_file
from winder.devices import mdriver as _mdriver
from winder.data import config as _config


class ConfigWidget(_QWidget):
    """Config Widget class for the winder GUI."""

    def __init__(self, parent=None):
        """Set up the ui."""
        super().__init__(parent)

        # setup the ui
        uifile = _get_ui_file(self)
        self.ui = _uic.loadUi(uifile, self)

        self.mdriver = _mdriver
        self.config = _config

        # connect signals and slots
        self.connect_signals_slots()

    def connect_signals_slots(self):
        """Create signal and slots connections."""
        self.ui.pbt_config.pressed.connect(self.configure)
        self.ui.pbt_connect.pressed.connect(self.connect)
        self.ui.pbt_disconnect.pressed.connect(self.disconnect)
        self.ui.pbt_save.pressed.connect(self.save)
        self.ui.cmb_config.currentTextChanged.connect(self.load)

    def connect(self):
        """Connects to the motor driver."""
        self.mdriver.connect(self.config.ip)

    def disconnect(self):
        """Disconnects the motor driver"""
        self.mdriver.disconnect()

    def save(self):
        """Save current configuration."""
        pass

    def configure(self):
        """Configures the winder with the current widget values."""
        # Updates configurations
        self.config.spd = self.ui.sbd_w.value()
        self.config.ac = self.ui.sbd_a.value()
        self.config.lc = self.ui.sbd_l.value()
        self.config.d = self.ui.sbd_d.value()
        self.config.nturns = self.ui.sb_nturns.value()
        self.config.motor_calculus()

        # Configures stepper motors
        _mt0 = self.config.mtype0
        _spd0 = self.config.spd0
        _ac0 = self.config.ac0
        _st0 = self.config.steps0
        _ust0 = self.config.usteps0
        _mt1 = self.config.mtype1
        _spd1 = self.config.spd1
        _ac1 = self.config.ac1
        _st1 = self.config.steps0
        _ust1 = self.config.usteps0
        self.mdriver.configure_stepper(motor=0, mtype=_mt0, spd=_spd0, ac=_ac0,
                                       steps=_st0, usteps=_ust0)
        self.mdriver.configure_stepper(motor=1, mtype=_mt1, spd=_spd1, ac=_ac1,
                                       steps=_st1, usteps=_ust1)

    def load(self):
        """Loads configuration set."""
        pass
