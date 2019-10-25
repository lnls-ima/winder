"""Widget for the configuration tab."""

# import sys as _sys
# import traceback as _traceback
import os as _os
from qtpy.QtWidgets import (
    QWidget as _QWidget,
    QMessageBox as _QMessageBox,
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

        self.list_config_files()
        # connect signals and slots
        self.connect_signals_slots()

    def connect_signals_slots(self):
        """Create signal and slots connections."""
        self.ui.pbt_config.pressed.connect(self.configure)
        self.ui.pbt_connect.pressed.connect(self.connect)
        self.ui.pbt_disconnect.pressed.connect(self.disconnect)
        self.ui.pbt_save.pressed.connect(self.save)
        self.ui.cmb_config.currentIndexChanged.connect(self.load)

    def enable_buttons(self, config=False, connect=True, disconnect=False):
        self.ui.pbt_config.setEnabled(config)
        self.ui.pbt_connect.setEnabled(connect)
        self.ui.pbt_disconnect.setEnabled(disconnect)

    def connect(self):
        """Connects to the motor driver."""
        if self.mdriver.connect(self.config.ip):
            self.enable_buttons(True, False, True)
        else:
            _msg = "Não foi possivel conectar ao driver do motor."
            _QMessageBox.warning(self, 'Falha', _msg, _QMessageBox.Ok)

    def disconnect(self):
        """Disconnects the motor driver"""
        self.mdriver.disconnect()
        self.enable_buttons(False, True, False)

    def save(self):
        """Save current configuration to file."""
        self.update_config()
        filename = self.ui.cmb_config.currentText()
        self.config.save_file(filename + '.cfg')
        self.ui.cmb_config.addItem(filename)

    def load(self):
        """Loads configuration set."""
        filename = self.ui.cmb_config.currentText() + '.cfg'
        if filename != '':
            self.config.read_file(filename)

        self.ui.sbd_w.setValue(self.config.spd)
        self.ui.sbd_a.setValue(self.config.ac)
        self.ui.sbd_l.setValue(self.config.lc)
        self.ui.sbd_d.setValue(self.config.d)
        self.ui.sb_nturns.setValue(self.config.nturns)

    def list_config_files(self):
        """List configuration files and insert in the combobox."""
        file_list = _os.listdir()
        cfg_list = []
        for file in file_list:
            if '.cfg' in file:
                cfg_list.append(file.split('.')[0])

        cfg_list.sort()
        self.ui.cmb_config.addItems(cfg_list)
        self.ui.cmb_config.setCurrentIndex(-1)

    def update_config(self):
        """Updates configuration object with current UI values."""
        self.config.spd = self.ui.sbd_w.value()
        self.config.ac = self.ui.sbd_a.value()
        self.config.lc = self.ui.sbd_l.value()
        self.config.d = self.ui.sbd_d.value()
        self.config.nturns = self.ui.sb_nturns.value()

    def configure(self):
        """Configures the winder with the current widget values."""
        # Updates configurations
        self.update_config()
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
