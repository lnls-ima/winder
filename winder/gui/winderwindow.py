"""Main window for winder GUI."""

from qtpy.QtWidgets import (
    QMainWindow as _QMainWindow,
    )
import qtpy.uic as _uic

from winder.gui.utils import get_ui_file as _get_ui_file
from winder.gui.controlwidget import ControlWidget as _ControlWidget
from winder.gui.configwidget import ConfigWidget as _ConfigWidget


class WinderWindow(_QMainWindow):
    """Main Window class for the winder GUI."""

    def __init__(self, parent=None, width=500, height=800):
        """Set up the ui and add main tabs."""
        super().__init__(parent)

        # set up the ui
        uifile = _get_ui_file(self)
        self.ui = _uic.loadUi(uifile, self)
        self.resize(width, height)

        # define tab names and correspondig widgets
        self.tab_names = [
            'configurar',
            'controlar',
            ]

        self.tab_widgets = []
        self.tab_widgets.append(_ConfigWidget())
        self.tab_widgets.append(_ControlWidget())

        # add widgets to main tab
        self.ui.twg_main_tab.clear()
        for i in range(len(self.tab_names)):
            tab_name = self.tab_names[i]
            tab = self.tab_widgets[i]
            setattr(self, tab_name, tab)
            self.ui.twg_main_tab.addTab(tab, tab_name.capitalize())
