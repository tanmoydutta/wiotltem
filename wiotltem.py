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
                # client = MQTTClient("d:0ilas3:Pycom:fipy01", "0ilas3.messaging.internetofthings.ibmcloud.com",user="use-token-auth", password="bhu76.Tfuyet_", port=1883)
                client.connect()

                lo["La"] = coord[0]
                lo["Lo"] = coord[1]

                m["d"] = lo
                # client.publish(topic="iot-2/evt/status/fmt/json", msg="{\"d\":\"OFF\"}")
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


def gpsData():
    py = Pytrack()
    l76 = L76GNSS(py, timeout=10)
    coord = l76.coordinates()
    print(coord)

def connLTEMTest():
    lte = LTE()         # instantiate the LTE object
    lte.attach()        # attach the cellular modem to a base station
    while not lte.isattached():
        time.sleep(0.25)
    lte.connect()       # start a data session and obtain an IP address
    while not lte.isconnected():
        time.sleep(0.25)
    print(b"LTE-M Connection open!")

    s = socket.socket()
    s = ssl.wrap_socket(s)
    s.connect(socket.getaddrinfo('www.google.com', 443)[0][-1])
    s.send(b"GET / HTTP/1.0\r\n\r\n")
    print(s.recv(4096))
    s.close()

    lte.disconnect()
    lte.dettach()
    print(b"LTE-M Connection closed!")

def mqttTest():
    try :
        lo = {}
        m = {}

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
            client = MQTTClient("d:0ilas3:Pycom:fipy01", "0ilas3.messaging.internetofthings.ibmcloud.com",user="use-token-auth", password="bhu76.Tfuyet_", port=1883)
            client.connect()

            lo["La"] = 52.33194
            lo["Lo"] = 4.940198

            m["d"] = lo
            # client.publish(topic="iot-2/evt/status/fmt/json", msg="{\"d\":\"OFF\"}")
            client.publish(topic="iot-2/evt/status/fmt/json", msg=ujson.dumps(m))
            print(b"Message Sent!")
            client.disconnect()
        except OSError:
            print(b"MQTT Connection Error!")

        # LTE Disconnect
        lte.disconnect()
        lte.dettach()
        print(b"LTE-M Connection closed!")
    except OSError:
        print(b"Error!")
