import logging
import unittest

from time import sleep

import programmingtheiot.common.ConfigConst as ConfigConst

from programmingtheiot.common import ConfigConst


from programmingtheiot.cda.connection.MqttClientConnector import MqttClientConnector
from programmingtheiot.common.ConfigUtil import ConfigUtil
from programmingtheiot.common.ResourceNameEnum import ResourceNameEnum
from programmingtheiot.common.DefaultDataMessageListener import DefaultDataMessageListener
from programmingtheiot.data.ActuatorData import ActuatorData

from programmingtheiot.data.SensorData import SensorData
from programmingtheiot.data.SystemPerformanceData import SystemPerformanceData
from programmingtheiot.data.DataUtil import DataUtil





class MqttClientControlPacketTest(unittest.TestCase):
	@classmethod
	def setUpClass(cls):
		logging.basicConfig(format = '%(asctime)s:%(module)s:%(levelname)s:%(message)s', level = logging.DEBUG)
		logging.info("Executing the MqttClientControlPacketTest class...")

		cls.cfg = ConfigUtil()
		# Usa un ID único para no interferir con otros clientes
		cls.mcc = MqttClientConnector(clientID = "TestClient_MQTT_ControlPackets")
		cls.listener = DefaultDataMessageListener()
		cls.mcc.setDataMessageListener(cls.listener)

	def setUp(self):
		pass

	def tearDown(self):
		pass

	def testConnectAndDisconnect(self):
		logging.info("Test: Connect and Disconnect")
		self.mcc.connectClient()
		sleep(2)  # Espera para ver los logs de conexión
		self.mcc.disconnectClient()
		sleep(2)

	def testServerPing(self):
		logging.info("Test: Ping the Server")
		self.mcc.connectClient()
		sleep(2)

		# PINGREQ/PINGRESP ocurre automáticamente por keep-alive
		logging.info("Waiting to observe PINGREQ / PINGRESP exchange...")
		sleep(65)  # Espera más que el keep-alive (60s) para ver el ping

		self.mcc.disconnectClient()
		sleep(2)

	def testPubSub(self):
		logging.info("Test: Publish and Subscribe (QoS 1 and 2)")
		self.mcc.connectClient()
		sleep(2)

		testTopic = ResourceNameEnum.CDA_ACTUATOR_CMD_RESOURCE

		# Subscribe (SUBSCRIBE + SUBACK)
		self.mcc.subscribeToTopic(testTopic, qos=1)
		self.mcc.subscribeToTopic(testTopic, qos=2)
		sleep(2)

		# Publish message (PUBLISH + PUBACK/PUBREC/PUBREL/PUBCOMP dependiendo del QoS)
		#actData = ConfigConst()
		actData=ConfigConst.COMMAND_ON

		actData.setValue(22.5)

		self.mcc.publishMessage(topicName=testTopic, data=actData, qos=1)
		self.mcc.publishMessage(topicName=testTopic, data=actData, qos=2)
		sleep(4)

		# Unsubscribe (UNSUBSCRIBE + UNSUBACK)
		self.mcc.unsubscribeFromTopic(testTopic)
		sleep(2)

		self.mcc.disconnectClient()
		sleep(2)
