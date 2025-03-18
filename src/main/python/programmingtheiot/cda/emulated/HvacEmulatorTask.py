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

class HvacEmulatorTask(BaseActuatorSimTask):
    """
    Shell representation of class for student implementation.
    """

    def __init__(self):
        super( 
            HvacEmulatorTask, self).__init__( 
                name = ConfigConst.HVAC_ACTUATOR_NAME, 
                typeID = ConfigConst.HVAC_ACTUATOR_TYPE, 
                simpleName = "HVAC")

        # **Asegurar que el emulador se active**
        enableEmulation = ConfigUtil().getBoolean( 
            ConfigConst.CONSTRAINED_DEVICE, ConfigConst.ENABLE_EMULATOR_KEY)

        self.sh = SenseHAT(emulate = enableEmulation)  # **Esta línea corrige el error**

    def _activateActuator(self, val: float = ConfigConst.DEFAULT_VAL, stateData: str = None) -> int:
        simple_name = self.getSimpleName() if self.getSimpleName() is not None else "Unknown"
        val = val if val is not None else ConfigConst.DEFAULT_VAL  # Evitar None en val

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

            # optional sleep (5 seconds) for message to scroll before clearing display
            sleep(5)

            self.sh.screen.clear()
            return 0
        else:
            logging.warning("No SenseHAT LED screen instance to clear / close.")
            return -1
