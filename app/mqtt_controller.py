"""MQTT Controller Module."""
import paho.mqtt.client as mqtt
from app.exceptions import StairChallengeConnectionError
from app.const import MQTT_BROKER_HOST, MQTT_BROKER_PORT, MQTT_BROKER_KEEPALIVE, MQTT_TRIGGER_TOPIC, MQTT_TEST_TOPIC

class MQTTClient:
    """MQTT Client Class."""
    def __init__(self):
        self.client = mqtt.Client("Raspberry Pi")
        self.client.on_connect = self.on_connect
        # self.client.on_message = self.on_message
        self.client.on_disconnect = self.on_disconnect

    def on_connect(self, client, userdata, flags, rc):
        """Define on_publish event function."""
        if rc == 0:
            print("Connected successfully with MQTT Broker")
            client.subscribe(MQTT_TEST_TOPIC)
            client.subscribe(MQTT_TRIGGER_TOPIC, 1)
        else:
            print("Connection problem with MQTT Broker!")

    def on_disconnect(self, client, userdata, rc):
        """Define on_disconnect event function."""
        if rc != 0:
            print("Unexpected disconnection.")

    def on_message(self, client, userdata, message):
        print(f"Message Received from Others: {message.payload.decode()}")

    def connect(self):
        try:
            """Connect with MQTT Broker."""
            self.client.connect(MQTT_BROKER_HOST, MQTT_BROKER_PORT, MQTT_BROKER_KEEPALIVE)
        except ConnectionRefusedError as exception:
            raise StairChallengeConnectionError("Could not connect to MQTT Broker") from exception

        self.client.loop_start()

    def disconnect(self):
        self.client.loop_stop()
        self.client.disconnect()