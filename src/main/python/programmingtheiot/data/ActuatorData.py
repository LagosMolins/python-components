#####
# 
# This class is part of the Programming the Internet of Things project.
# 
# It is provided as a simple shell to guide the student and assist with
# implementation for the Programming the Internet of Things exercises,
# and designed to be modified by the student as needed.
#

import programmingtheiot.common.ConfigConst as ConfigConst
from programmingtheiot.data.BaseIotData import BaseIotData

class ActuatorData(BaseIotData):
    """
    Representación de la clase ActuatorData.
    """

    def __init__(self, typeID: int = ConfigConst.DEFAULT_ACTUATOR_TYPE, name = ConfigConst.NOT_SET, d = None):
        super(ActuatorData, self).__init__(name=name, typeID=typeID, d=d)
        
        # Inicialización de variables de instancia
        self.value = ConfigConst.DEFAULT_VAL
        self.command = ConfigConst.DEFAULT_COMMAND
        self.stateData = ""
        self.isResponse = False

    # Métodos getter
    def getCommand(self) -> int:
        """Devuelve el comando del actuador."""
        return self.command

    def getStateData(self) -> str:
        """Devuelve los datos de estado del actuador."""
        return self.stateData

    def getValue(self) -> float:
        """Devuelve el valor del actuador."""
        return self.value

    def isResponseFlagEnabled(self) -> bool:
        """Devuelve si la respuesta está habilitada."""
        return self.isResponse

    # Métodos setter
    def setCommand(self, command: int):
        """Establece el comando del actuador."""
        self.command = command
        self.updateTimeStamp()  # Actualiza la marca de tiempo

    def setAsResponse(self):
        """Marca el actuador como respuesta."""
        self.isResponse = True
        self.updateTimeStamp()  # Actualiza la marca de tiempo

    def setStateData(self, stateData: str):
        """Establece los datos de estado del actuador."""
        if stateData:
            self.stateData = stateData
            self.updateTimeStamp()  # Actualiza la marca de tiempo

    def setValue(self, val: float):
        """Establece el valor del actuador."""
        self.value = val
        self.updateTimeStamp()  # Actualiza la marca de tiempo

    # Método privado para manejar actualizaciones de datos
    def _handleUpdateData(self, data):
        """
        Actualiza los datos del actuador con los datos de otra instancia de ActuatorData.
        
        @param data: Instancia de ActuatorData con la que se actualizarán los datos.
        """
        try:
            if data and isinstance(data, ActuatorData):
                self.command = data.getCommand()
                self.stateData = data.getStateData()
                self.value = data.getValue()
                self.isResponse = data.isResponseFlagEnabled()
        except Exception as e:
            print(f"Error al actualizar datos: {e}")

    # Método opcional para obtener la representación en cadena del objeto
    def __str__(self):
        """Devuelve una representación en cadena del ActuatorData."""
        return f"ActuatorData(name={self.name}, typeID={self.typeID}, command={self.command}, stateData={self.stateData}, value={self.value}, timeStamp={self.timeStamp})"
