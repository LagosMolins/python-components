#####
# 
# This class is part of the Programming the Internet of Things project.
# 
# It is provided as a simple shell to guide the student and assist with
# implementation for the Programming the Internet of Things exercises,
# and designed to be modified by the student as needed.
#

import json
import programmingtheiot.common.ConfigConst as ConfigConst
from programmingtheiot.data.BaseIotData import BaseIotData

class SystemPerformanceData(BaseIotData):
    """
    Representación de la clase SystemPerformanceData.
    """
    DEFAULT_VAL = 0.0
    
    def __init__(self, d=None):
        super(SystemPerformanceData, self).__init__(name=ConfigConst.SYSTEM_PERF_MSG, typeID=ConfigConst.SYSTEM_PERF_TYPE, d=d)
        self.cpuUtil = ConfigConst.DEFAULT_VAL
        self.memUtil = ConfigConst.DEFAULT_VAL

    def getCpuUtilization(self):
        """Devuelve la utilización de CPU."""
        return self.cpuUtil

    def getMemoryUtilization(self):
        """Devuelve la utilización de memoria."""
        return self.memUtil

    def setCpuUtilization(self, cpuUtil):
        """Establece la utilización de CPU."""
        self.cpuUtil = cpuUtil
        self.updateTimeStamp()  # Actualiza la marca de tiempo

    def setMemoryUtilization(self, memUtil):
        """Establece la utilización de memoria."""
        self.memUtil = memUtil
        self.updateTimeStamp()  # Actualiza la marca de tiempo

    def _handleUpdateData(self, data):
        """
        Actualiza los datos de rendimiento del sistema con los datos de otra instancia de SystemPerformanceData.
        
        @param data: Instancia de SystemPerformanceData con la que se actualizarán los datos.
        """
        try:
            if data and isinstance(data, SystemPerformanceData):
                self.cpuUtil = data.getCpuUtilization()
                self.memUtil = data.getMemoryUtilization()
        except Exception as e:
            print(f"Error al actualizar datos: {e}")

    def __str__(self):
        """Devuelve una representación en cadena del SystemPerformanceData."""
        return f"SystemPerformanceData(name={self.name}, typeID={self.typeID}, cpuUtil={self.cpuUtil}, memUtil={self.memUtil}, timeStamp={self.timeStamp})"

    # Método para mapear los datos JSON a los atributos de la clase SystemPerformanceData
    def from_json(self, jsonData):
        """
        Método para mapear los datos JSON a los atributos de la clase SystemPerformanceData.
        
        @param jsonData: Cadena JSON con la información a mapear.
        """
        try:
            # Convertir la cadena JSON en un diccionario Python
            jsonData = jsonData.replace("\'", "\"").replace('False', 'false').replace('True', 'true')
            jsonStruct = json.loads(jsonData)
            
            # Crear instancia de SystemPerformanceData
            sysPerfData = SystemPerformanceData()
            varStruct = vars(sysPerfData)
            
            # Iterar sobre las claves del diccionario y asignar valores a la instancia
            for key in jsonStruct:
                if key in varStruct:
                    setattr(sysPerfData, key, jsonStruct[key])
            
            # Retornar la instancia de SystemPerformanceData con los valores actualizados
            return sysPerfData
        except Exception as e:
            print(f"Error al procesar el JSON: {e}")
            return None

    # Método para convertir el objeto SystemPerformanceData a JSON
    def to_json(self):
        """
        Método para convertir el objeto SystemPerformanceData a JSON.
        
        @return: Cadena JSON representando el objeto SystemPerformanceData.
        """
        try:
            # Convertir los datos del objeto en un diccionario
            sysPerfData = {
                "name": self.name,
                "typeID": self.typeID,
                "cpuUtil": self.cpuUtil,
                "memUtil": self.memUtil,
                "timeStamp": self.timeStamp
            }
            
            # Serializar el objeto a formato JSON
            jsonData = json.dumps(sysPerfData, indent=4)
            return jsonData
        except Exception as e:
            print(f"Error al convertir el objeto a JSON: {e}")
            return None
