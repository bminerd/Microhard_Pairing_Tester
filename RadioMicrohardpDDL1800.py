import base64
import telnetlib
import math
from enum import Enum
import re
import time

class RadioMicrohardpDDL1800:
    
    #---------------------------------------------------------------------------
    # Public types
    #---------------------------------------------------------------------------

    class ChannelBandwidth(Enum):
        CHANNEL_BANDWIDTH_8_MHZ = 0
        CHANNEL_BANDWIDTH_4_MHZ = 1
        CHANNEL_BANDWIDTH_2_MHZ = 2
        CHANNEL_BANDWIDTH_1_MHZ = 3

    #---------------------------------------------------------------------------
    # Public constructors
    #---------------------------------------------------------------------------

    #---------------------------------------------------------------------------
    def __init__(self, ipAddress, username, password):

        self.ipAddress = ipAddress
        self.port      = 23
        self.username  = username
        self.password  = password
        self.telnetClient = telnetlib.Telnet()

    #---------------------------------------------------------------------------
    # Public methods
    #---------------------------------------------------------------------------

    #---------------------------------------------------------------------------
    def openTelnet(self):

        self.telnetClient.open(self.ipAddress, self.port)

        self.telnetClient.read_until("login: ")
        self.telnetClient.write(self.username + "\r")

        self.telnetClient.read_until("Password: ")
        self.telnetClient.write(self.password + "\r")
        self.telnetClient.read_until(">")

    #---------------------------------------------------------------------------
    def closeTelnet(self):

        self.telnetClient.write("ATO\r")
        self.telnetClient.close()

    #---------------------------------------------------------------------------
    def rebootModem(self):
        
        self.telnetClient.write("AT+MSREB\r")
        response = self.telnetClient.read_until("OK\r")

        time.sleep(60)

        self.telnetClient.close()
        self.openTelnet()

    #---------------------------------------------------------------------------
    def enableConfigurationChanges(self):

        self.telnetClient.write("AT&W\r")
        response = self.telnetClient.read_until(">")

    #---------------------------------------------------------------------------
    def getRadioTxPowerDbm(self):

        self.telnetClient.write("AT+MWTXPOWER\r")
        response = self.telnetClient.read_until(">")

        txPowerDbm = int(re.findall(".* (\d+) dbm.*", response)[0])

        return txPowerDbm

    #---------------------------------------------------------------------------
    def setRadioTxPowerDbm(self, txPowerDbm, enableChange=True):

        if txPowerDbm < 7:
            txPowerDbm = 7
        elif txPowerDbm > 30:
            txPowerDbm = 30

        self.telnetClient.write("AT+MWTXPOWER={}\r".format(txPowerDbm))
        response = self.telnetClient.read_until(">")

        if enableChange:

            self.enableConfigurationChanges()

    #---------------------------------------------------------------------------
    def getRadioTxPowerW(self):

        txPowerDbm = self.getRadioTxPowerDbm()
        
        txPowerW = pow(10, (txPowerDbm - 30) / 10)

        return txPowerW

    #---------------------------------------------------------------------------
    def setRadioTxPowerW(self, txPowerW, enableChange=True):

        txPowerDbm = 10 * log(txPowerW) + 30

        self.setRadioTxPowerDbm(txPowerDbm)

        if enableChange:

            self.enableConfigurationChanges()

    #---------------------------------------------------------------------------
    def getRadioChannelFrequencyMhz(self):

        self.telnetClient.write("AT+MWFREQ\r")
        response = self.telnetClient.read_until(">")

        channelFrequencyMhz = int(re.findall(".* (\d+) MHz.*", response)[0])

        return channelFrequencyMhz

    #---------------------------------------------------------------------------
    def setRadioChannelFrequencyMhz(self, channelFrequencyMhz, enableChange=True):

        if channelFrequencyMhz < 1814:

            channelFrequencyMhz = 1814

        elif channelFrequencyMhz > 1866:

            channelFrequencyMhz = 1866

        channelFrequencyMhz = channelFrequencyMhz - 1810

        self.telnetClient.write("AT+MWFREQ1800={}\r".format(channelFrequencyMhz))
        response = self.telnetClient.read_until(">")

        if enableChange:

            self.enableConfigurationChanges()

    #---------------------------------------------------------------------------
    def getRadioChannelBandwidth(self):

        self.telnetClient.write("AT+MWFBAND\r")
        response = self.telnetClient.read_until(">")

        channelBandwidth = ChannelBandwidth(re.findall(".* (\d+) - .*MHz.*", response)[0])

        return channelBandwidth

    #---------------------------------------------------------------------------
    def setRadioChannelBandwidth(self, channelBandwidth, enableChange=True):

        self.telnetClient.write("AT+MWFBAND={}\r".format(channelBandwidth))
        response = self.telnetClient.read_until(">")

        if enableChange:

            self.enableConfigurationChanges()

    #---------------------------------------------------------------------------
    def getRadioChannelInterferenceTable(self, subBands=2):

        interferenceTable = []

        for i in range(subBands):

            self.telnetClient.write("AT+MWINTFSCAN={}\r".format(i))
            response = self.telnetClient.read_until(">", 20)

            channels = re.findall("[\n|\r](\d+)", response)

            for channel in channels:

                interferenceTable.append(int(channel))

        interferenceTable.sort()

        return interferenceTable

    #---------------------------------------------------------------------------
    def getRadioNetworkId(self):

        self.telnetClient.write("AT+MWNETWORKID\r")
        response = self.telnetClient.read_until(">")

        networkId = int(re.findall(".* ID: (\w+)", response)[0])

        return networkId

    #---------------------------------------------------------------------------
    def setRadioNetworkId(self, networkId, enableChange=True):

        self.telnetClient.write("AT+MWFNETWORKID={}\r".format(networkId))
        response = self.telnetClient.read_until(">")

        if enableChange:

            self.enableConfigurationChanges()

    #---------------------------------------------------------------------------
    def getRadioEncryptionKey(self):

        self.telnetClient.write("AT+MWVENCRYPT\r")
        response = self.telnetClient.read_until(">")

        encryptionKey = int(re.findall(".* Password: (\w+)", response)[0])

        return encryptionKey

    #---------------------------------------------------------------------------
    def setRadioEncryptionKey(self, encryptionKey, enableChange=True):

        self.telnetClient.write("AT+MWVENCRYPT={}\r".format(encryptionKey))
        response = self.telnetClient.read_until(">")

        if enableChange:

            self.enableConfigurationChanges()

    #---------------------------------------------------------------------------
    def isRadioConnectedToNetwork(self):

        self.telnetClient.write("AT+MWSTATUS\r")
        response = self.telnetClient.read_until(">")

        isConnected = "Connection Info" in response
        
        return isConnected
    