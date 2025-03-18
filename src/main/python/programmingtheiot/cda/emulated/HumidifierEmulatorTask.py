#####
# 
# This class is part of the Programming the Internet of Things project.
# 
# It is provided as a simple shell to guide the student and assist with
# implementation for the Programming the Internet of Things exercises,
# and designed to be modified by the student as needed.
#

import logging

from time import sleep

import programmingtheiot.common.ConfigConst as ConfigConst

from programmingtheiot.common.ConfigUtil import ConfigUtil
from programmingtheiot.cda.sim.BaseActuatorSimTask import BaseActuatorSimTask

from pisense import SenseHAT

class HumidifierEmulatorTask(BaseActuatorSimTask):
	"""
	Shell representation of class for student implementation.
	
	"""

	def __init__(self):
		super( \
			HumidifierEmulatorTask, self).__init__( \
				name = ConfigConst.HUMIDIFIER_ACTUATOR_NAME, \
				typeID = ConfigConst.HUMIDIFIER_ACTUATOR_TYPE, \
				simpleName = "HUMIDIFIER")

		enableEmulation = \
			ConfigUtil().getBoolean( \
				ConfigConst.CONSTRAINED_DEVICE, ConfigConst.ENABLE_EMULATOR_KEY)

		self.sh = SenseHAT(emulate = enableEmulation)

	def _activateActuator(self, val: float = ConfigConst.DEFAULT_VAL, stateData: str = None) -> int:
		simple_name = self.getSimpleName() if self.getSimpleName() is not None else "Unknown"  
		val = val if val is not None else ConfigConst.DEFAULT_VAL  # Asegurar que val no sea None

		if self.sh.screen:
			msg = f"{simple_name} ON: {val}C"
			self.sh.screen.scroll_text(msg)
			return 0
		else:
			logging.warning("No SenseHAT LED screen instance to write.")
			return -1


	def _deactivateActuator(self, val: float = ConfigConst.DEFAULT_VAL, stateData: str = None) -> int:
		simple_name = self.getSimpleName() if self.getSimpleName() is not None else "Unknown"

		if self.sh.screen:
			msg = f"{simple_name} OFF"
			self.sh.screen.scroll_text(msg)
			sleep(5)  # Opcional, para que el mensaje se vea antes de limpiar la pantalla
			self.sh.screen.clear()
			return 0
		else:
			logging.warning("No SenseHAT LED screen instance to clear / close.")
			return -1

	