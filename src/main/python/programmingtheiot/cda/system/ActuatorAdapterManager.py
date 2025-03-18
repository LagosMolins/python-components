#####
# 
# This class is part of the Programming the Internet of Things project.
# 
# It is provided as a simple shell to guide the student and assist with
# implementation for the Programming the Internet of Things exercises,
# and designed to be modified by the student as needed.
#

import logging
from importlib import import_module
import programmingtheiot.common.ConfigConst as ConfigConst
from programmingtheiot.common.ConfigUtil import ConfigUtil
from programmingtheiot.common.IDataMessageListener import IDataMessageListener
from programmingtheiot.data.ActuatorData import ActuatorData

from programmingtheiot.cda.sim.HvacActuatorSimTask import HvacActuatorSimTask
from programmingtheiot.cda.sim.HumidifierActuatorSimTask import HumidifierActuatorSimTask

class ActuatorAdapterManager(object):
    """
    Shell representation of class for student implementation.
    """
    
    def __init__(self, dataMsgListener: IDataMessageListener = None):
        self.dataMsgListener = dataMsgListener
        self.configUtil = ConfigUtil()

        # Cargar las configuraciones desde PiotConfig.props
        self.useSimulator = self.configUtil.getBoolean(
            section=ConfigConst.CONSTRAINED_DEVICE, key=ConfigConst.ENABLE_SIMULATOR_KEY
        )
        self.useEmulator = self.configUtil.getBoolean(
            section=ConfigConst.CONSTRAINED_DEVICE, key=ConfigConst.ENABLE_EMULATOR_KEY
        )
        self.deviceID = self.configUtil.getProperty(
            section=ConfigConst.CONSTRAINED_DEVICE, key=ConfigConst.DEVICE_LOCATION_ID_KEY, defaultVal=ConfigConst.NOT_SET
        )
        self.locationID = self.configUtil.getProperty(
            section=ConfigConst.CONSTRAINED_DEVICE, key=ConfigConst.DEVICE_LOCATION_ID_KEY, defaultVal=ConfigConst.NOT_SET
        )

        self.humidifierActuator = None
        self.hvacActuator = None
        self.ledDisplayActuator = None

        # Cargar los actuadores (simuladores o emuladores) según la configuración
        if self.useEmulator:
            logging.info("Using emulator. Loading actuator emulator tasks.")
            self._initEnvironmentalActuationTasks()

    def _initEnvironmentalActuationTasks(self):
        if self.useEmulator:
            # Cargar los módulos de emulador dinámicamente
            humidifierModule = import_module('programmingtheiot.cda.emulated.HumidifierEmulatorTask', 'HumidifierEmulatorTask')
            humidifierClazz = getattr(humidifierModule, 'HumidifierEmulatorTask')
            self.humidifierActuator = humidifierClazz()

            hvacModule = import_module('programmingtheiot.cda.emulated.HvacEmulatorTask', 'HvacEmulatorTask')
            hvacClazz = getattr(hvacModule, 'HvacEmulatorTask')
            self.hvacActuator = hvacClazz()

            # Si deseas agregar el emulador de LED Display, también puedes agregarlo
            ledDisplayModule = import_module('programmingtheiot.cda.emulated.LedDisplayEmulatorTask', 'LedDisplayEmulatorTask')
            ledDisplayClazz = getattr(ledDisplayModule, 'LedDisplayEmulatorTask')
            self.ledDisplayActuator = ledDisplayClazz()
        else:
            # Si no usas el emulador, solo cargas los simuladores como antes
            self.humidifierActuator = HumidifierActuatorSimTask()
            self.hvacActuator = HvacActuatorSimTask()

    def sendActuatorCommand(self, data: ActuatorData) -> ActuatorData:
        if data and not data.isResponseFlagEnabled():
            # Primero verifica si el evento de actuador está destinado a este dispositivo
            if data.getLocationID() == self.locationID:
                logging.info("Actuator command received for location ID %s. Processing...", str(data.getLocationID()))

                aType = data.getTypeID()
                responseData = None

                # Implementar el manejo de actuadores según el tipo
                if aType == ConfigConst.HUMIDIFIER_ACTUATOR_TYPE and self.humidifierActuator:
                    responseData = self.humidifierActuator.updateActuator(data)
                elif aType == ConfigConst.HVAC_ACTUATOR_TYPE and self.hvacActuator:
                    responseData = self.hvacActuator.updateActuator(data)
                elif aType == ConfigConst.LED_DISPLAY_ACTUATOR_TYPE and self.ledDisplayActuator:
                    responseData = self.ledDisplayActuator.updateActuator(data)
                else:
                    logging.warning("No valid actuator type. Ignoring actuation for type: %s", data.getTypeID())

                return responseData
            else:
                logging.warning("Location ID doesn't match. Ignoring actuation: (me) %s != (you) %s", str(self.locationID), str(data.getLocationID()))
        else:
            logging.warning("Actuator request received. Message is empty or response. Ignoring.")

        return None
    
    def setDataMessageListener(self, listener: IDataMessageListener) -> bool:
        if listener:
            self.dataMsgListener = listener
            return True
        return False
