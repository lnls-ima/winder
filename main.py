"""Run the winder application.

Created on 15 de out de 2019

@author: VitorPS
"""

from winder.gui import winderapp

_run_in_thread = True


if _run_in_thread:
    thread = winderapp.run_in_thread()
else:
    winderapp.run()
