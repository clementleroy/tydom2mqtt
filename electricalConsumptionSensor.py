import json
import time
from datetime import datetime
from sensors import sensor

class ElectricalConsumptionSensor:

    def __init__(self, tydom_attributes, tydom_client=None, mqtt=None):
        self.attributes = tydom_attributes
        self.device_id = self.attributes['device_id']
        self.endpoint_id = self.attributes['endpoint_id']
        self.id = self.attributes['id']
        self.name = self.attributes['name']
        self.mqtt = mqtt
        self.tydom_client = tydom_client

    async def setup(self):
        self.device = {}
        self.device['manufacturer'] = 'Delta Dore'
        self.device['model'] = 'Consommation Electrique'
        self.device['name'] = self.name
        self.device['identifiers'] = self.id

        #self.config_topic = cover_config_topic.format(id=self.id)
        self.config = {}
        self.config['name'] = self.name
        self.config['unique_id'] = self.id
        # self.config['attributes'] = self.attributes
        #self.config['json_attributes_topic'] = cover_attributes_topic.format(id=self.id)

        self.config['device'] = self.device
        # print(self.config)

        if (self.mqtt != None):
            self.mqtt.mqtt_client.publish(self.config_topic, json.dumps(self.config), qos=0)
        # setup_pub = '(self.config_topic, json.dumps(self.config), qos=0)'
        # return(setup_pub)


    async def update(self):
        await self.setup()
        self.setup()

        try:
            await
            self.update_sensors()
        except Exception as e:
            print("Electrical consumption sensors Error :")
            print(e)

       # self.state_topic = alarm_state_topic.format(id=self.id, state=self.current_state)
        if (self.mqtt != None):
            self.mqtt.mqtt_client.publish(self.state_topic, self.current_state, qos=0, retain=True)  # Alarm State
            self.mqtt.mqtt_client.publish(self.config['json_attributes_topic'], self.attributes, qos=0)
        print("Electrical consumption created / updated : ", self.name, self.id, self.current_state)

    async def update_sensors(self):
        # print('test sensors !')
        for i, j in self.attributes.items():
            # sensor_name = "tydom_alarm_sensor_"+i
            # print("name "+sensor_name, "elem_name "+i, "attributes_topic_from_device ",self.config['json_attributes_topic'], "mqtt",self.mqtt)
            if not i == 'device_type' or not i == 'id':
                new_sensor = None
                new_sensor = sensor(elem_name=i, tydom_attributes_payload=self.attributes, attributes_topic_from_device=self.config['json_attributes_topic'], mqtt=self.mqtt)
                await new_sensor.update()
