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

class SensorData(BaseIotData):
    """
    Representación de la clase SensorData.
    """
    
    def __init__(self, typeID: int = ConfigConst.DEFAULT_SENSOR_TYPE, name = ConfigConst.NOT_SET, d = None):
        super(SensorData, self).__init__(name=name, typeID=typeID, d=d)
        
        # Inicialización de las variables de la clase
        self.value = ConfigConst.DEFAULT_VAL
        self.sensorType = typeID  # Asumimos que el typeID es el tipo de sensor por defecto
    
    def getSensorType(self) -> int:
        """Devuelve el tipo de sensor."""
        return self.sensorType
    
    def getValue(self) -> float:
        """Devuelve el valor del sensor."""
        return self.value

    def setValue(self, newVal: float):
        """Establece un nuevo valor para el sensor."""
        self.value = newVal
        self.updateTimeStamp()  # Actualiza la marca de tiempo

    def _handleUpdateData(self, data):
        """
        Actualiza los datos del sensor con los datos de otra instancia de SensorData.
        
        @param data: Instancia de SensorData con la que se actualizarán los datos.
        """
        try:
            if data and isinstance(data, SensorData):
                self.value = data.getValue()
        except Exception as e:
            print(f"Error al actualizar datos: {e}")

    def __str__(self):
        """Devuelve una representación en cadena del SensorData."""
        return f"SensorData(name={self.name}, typeID={self.typeID}, value={self.value}, timeStamp={self.timeStamp})"
    
    # Método para mapear los datos JSON a los atributos de la clase SensorData
    def from_json(self, jsonData):
        """
        Método para mapear los datos JSON a los atributos de la clase SensorData.
        
        @param jsonData: Cadena JSON con la información a mapear.
        """
        try:
            # Convertir la cadena JSON en un diccionario Python
            jsonData = jsonData.replace("\'", "\"").replace('False', 'false').replace('True', 'true')
            jsonStruct = json.loads(jsonData)
            
            # Crear instancia de SensorData
            sensorData = SensorData()
            varStruct = vars(sensorData)
            
            # Iterar sobre las claves del diccionario y asignar valores a la instancia
            for key in jsonStruct:
                if key in varStruct:
                    setattr(sensorData, key, jsonStruct[key])
            
            # Retornar la instancia de SensorData con los valores actualizados
            return sensorData
        except Exception as e:
            print(f"Error al procesar el JSON: {e}")
            return None

    # Método para convertir el objeto SensorData a JSON
    def to_json(self):
        """
        Método para convertir el objeto SensorData a JSON.
        
        @return: Cadena JSON representando el objeto SensorData.
        """
        try:
            # Convertir los datos del objeto en un diccionario
            sensorData = {
                "name": self.name,
                "typeID": self.typeID,
                "value": self.value,
                "sensorType": self.sensorType,
                "timeStamp": self.timeStamp
            }
            
            # Serializar el objeto a formato JSON
            jsonData = json.dumps(sensorData, indent=4)
            return jsonData
        except Exception as e:
            print(f"Error al convertir el objeto a JSON: {e}")
            return None
