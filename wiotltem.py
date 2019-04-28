import socket
import ssl
import time
import ujson
from network import LTE
from mqtt import MQTTClient
from L76GNSS import L76GNSS
from pytrack import Pytrack

def sendGPSLocation(devId, msgServer, authToken):
    try :
        py = Pytrack()
        l76 = L76GNSS(py, timeout=30)
        lo = {}
        m = {}
        # Query location data
        coord = l76.coordinates()
        if coord[0] != None :
            # LTE Connection
            lte = LTE()         # instantiate the LTE object
            lte.attach()        # attach the cellular modem to a base station
            while not lte.isattached():
                time.sleep(0.25)
            lte.connect()       # start a data session and obtain an IP address
            while not lte.isconnected():
                time.sleep(0.25)
            print(b"LTE-M Connection open!")

            try :
                # Watson IoT message send
                client = MQTTClient(devId, msgServer,user="use-token-auth", password=authToken, port=1883)
                client.connect()

                lo["La"] = coord[0]
                lo["Lo"] = coord[1]

                m["d"] = lo
                client.publish(topic="iot-2/evt/status/fmt/json", msg=ujson.dumps(m))
                print(b"Message Sent!")
                client.disconnect()
            except OSError:
                print(b"MQTT Connection Error!")

            # LTE Disconnect
            lte.disconnect()
            lte.dettach()
            print(b"LTE-M Connection closed!")

        else :
            print(b"No GPS lock!")
    except OSError:
        print(b"Error!")

