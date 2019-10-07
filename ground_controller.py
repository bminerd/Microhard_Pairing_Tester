from Cryptodome.PublicKey import RSA
import os
import socket
import ssl
import time
import random

from RadioMicrohardpDDL1800 import RadioMicrohardpDDL1800

# ipAddress = input("Enter Ground Controller radio IP: ")
# username = input("Enter Ground Controller radio username: ")
# password = input("Enter Ground Controller radio password: ")
# pairingChannelFrequencyMhz = input("Enter pairing channel in MHz: ")
# operatingChannelFrequencyMhz = input("Enter operating channel in MHz: ")

ipAddress = "192.168.168.1"
username = "admin"
password = "Diu4u"
operatingChannelFrequencyMhz = 1814
operatingChannelBandwidthMhz = RadioMicrohardpDDL1800.ChannelBandwidth.CHANNEL_BANDWIDTH_4_MHZ

pairingChannelFrequencyMhz = 1830
pairingChannelBandwidthMhz = RadioMicrohardpDDL1800.ChannelBandwidth.CHANNEL_BANDWIDTH_1_MHZ
pairingSsid = "pDDL"
pairingKey = "1234567890"

radio = RadioMicrohardpDDL1800(ipAddress, username, password)
radio.openTelnet()

channelFrequencyMhz = random.randrange(1814, 1866)
print("Setting radio to random channel ({} MHz)".format(channelFrequencyMhz))
radio.setRadioChannelFrequencyMhz(channelFrequencyMhz)

print("Setting SSID to \"dummy\"")
radio.setRadioNetworkId("dummy")

print("Setting encryption key to \"dummy\"")
radio.setRadioEncryptionKey("dummy")

totalStartTime = time.time()
rebootStartTime = totalStartTime

print("Simulating radio power-on (rebooting radio)")
radio.rebootModem()

rebootTime = time.time() - rebootStartTime

connectStartTime = time.time()

print("Configuring the radio for low power transmission (7 dbm / 5 mw)")
radio.setRadioTxPowerDbm(7)

print("Configuring the radio with the pairing channel frequency")
radio.setRadioChannelFrequencyMhz(pairingChannelFrequencyMhz, False)

print("Configuring the radio with the pairing channel bandwidth")
radio.setRadioChannelBandwidth(pairingChannelBandwidthMhz, False)

print("Configuring the radio with the pairing network ID")
radio.setRadioNetworkId(pairingSsid, False)

print("Configuring the radio with the pairing encryption key")
radio.setRadioEncryptionKey(pairingKey, False)

print("Enabling configuration changes")
radio.enableConfigurationChanges()

print("Waiting for connection with Air Vehicle...")

isConnected = False

while not isConnected:

    isConnected = radio.isRadioConnectedToNetwork()
    time.sleep(0.5)

connectTime = time.time() - connectStartTime
print("Connected to Air Vehicle")

# SSL session

# randomKey = ''.join(os.urandom.choice('0123456789ABCDEF') for i in range(16))

# keyExists = os.path.isfile('ground_controller_private_key.pem')

# if not keyExists:
#     key = RSA.generate(2048)
#     privateKeyString = key.exportKey()

#     with open ('ground_controller_private_key.pem', 'w') as privateFile:
#         print("{}".format(privateKeyString.decode()), file=privateFile)

#     publicKeyString = key.publickey().exportKey()

#     with open ('ground_controller_public_key.pem', 'w') as publicFile:
#         print("{}".format(publicKeyString.decode()), file=publicFile)

# context = ssl.SSLContext(protocol=ssl.PROTOCOL_TLSv1_2)
# context.load_cert_chain('cert.pem')

# with socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0) as sock:
#     sock.bind(('192.168.168.219', 8443))
#     sock.listen(5)

#     with context.wrap_socket(sock, server_side=True) as ssock:
#         conn, addr = ssock.accept()
#         conn.send("KEY=")

print("Configuring the radio with the operating channel frequency")
radio.setRadioChannelFrequencyMhz(operatingChannelFrequencyMhz, False)

print("Configuring the radio with the operating channel bandwidth")
radio.setRadioChannelBandwidth(operatingChannelBandwidthMhz, False)

print("Enabling configuration changes")
radio.enableConfigurationChanges()

totalTime = time.time() - totalStartTime

radio.closeTelnet()

print("\nTest Complete\n")
print("Results")
print("-------------------------")
print("Time to boot: {:.1f} seconds".format(rebootTime))
print("Time to connect after power-on: {:.1f} seconds".format(connectTime))
print("Total time (boot + connect): {:.1f} seconds".format(totalTime))