from asyncio import sleep
import logging
import unittest
import time
import json
from programmingtheiot.cda.connection.MqttClientConnector import MqttClientConnector
from programmingtheiot.common.ResourceNameEnum import ResourceNameEnum
from programmingtheiot.common.DefaultDataMessageListener import DefaultDataMessageListener
from programmingtheiot.data.ActuatorData import ActuatorData
from programmingtheiot.data.DataUtil import DataUtil

class MqttClientControlPacketTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        logging.basicConfig(
            format='%(asctime)s:%(module)s:%(levelname)s:%(message)s',
            level=logging.INFO
        )
        logging.info("Testing MqttClientConnector class...")
        
        cls.mcc = MqttClientConnector(clientID="MyTestMqttClient")
        
        # Configurar el payload exacto
        cls.test_payload = {
            "timeStamp": "2022-02-19T23:10:27.737941+00:00",
            "hasError": False,
            "name": "Not Set",
            "typeID": 0,
            "statusCode": 0,
            "latitude": 0.0,
            "longitude": 0.0,
            "elevation": 0.0,
            "locationID": None,
            "value": 0.0,
            "command": 7,
            "stateData": None
        }

        # Configurar un listener personalizado
        class TestMessageListener(DefaultDataMessageListener):
            def handleIncomingMessage(self, topic: str, msg: str):
                try:
                    logging.info("MQTT message received with payload: %s", msg)
                except Exception as e:
                    logging.error("Error handling message: %s", str(e))
        
        cls.listener = TestMessageListener()
        cls.mcc.setDataMessageListener(cls.listener)

    def setUp(self):
        if hasattr(self.mcc, 'mqttClient') and self.mcc.mqttClient:
            self.mcc.disconnectClient()
            time.sleep(1)

    def tearDown(self):
        if hasattr(self.mcc, 'mqttClient') and self.mcc.mqttClient:
            self.mcc.disconnectClient()
            time.sleep(1)

    def testConnectAndDisconnect(self):
        """Test CONNECT and DISCONNECT packets"""
        logging.info("Testing CONNECT and DISCONNECT")
        
        self.mcc.connectClient()
        time.sleep(1)
        self.mcc.disconnectClient()
        time.sleep(1)

    def testServerPing(self):
        """Test PINGREQ and PINGRESP packets"""
        logging.info("Testing PINGREQ and PINGRESP")
        
        self.mcc.connectClient()
        time.sleep(1)
        logging.info("Waiting for keep-alive ping...")
        sleep(65)
        self.mcc.disconnectClient()

    def testPubSub(self):
        """Test PUBLISH/SUBSCRIBE with QoS 1"""
        logging.info("Testing PUBLISH/SUBSCRIBE")
        
        self.mcc.connectClient()
        time.sleep(1)
        
        topic = ResourceNameEnum.CDA_ACTUATOR_CMD_RESOURCE.value
        
        # Publicar 7 mensajes como en el ejemplo
        for _ in range(7):
            message = json.dumps(self.test_payload)
            self.mcc.publishMessage(topic, message, qos=1)
            time.sleep(0.5)
        
        self.mcc.disconnectClient()
        time.sleep(1)

if __name__ == "__main__":
    unittest.main()