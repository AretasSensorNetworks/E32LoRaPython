import serial
import time
import enum
import BitVector as bv

'''
This is a module for interfacing with E32 LoRa modules over serial

You need pyserial and BitVector 

First commit will be pretty lean, I will expand on it over the coming weeks

'''

# doing these enums like this is probably bad in the sense they are initialized and taking up memory...
# especially if we port this to micropython

# SPED bits 7,6
class UARTOptions(enum.Enum):
    OPT_8_N_1 = bv.BitVector(bitlist=[0,0]) # default
    OPT_8_O_1 = bv.BitVector(bitlist=[0,1])
    OPT_8_E_1 = bv.BitVector(bitlist=[1,0])
    OPT_8_N_1_ALT = bv.BitVector(bitlist=[1, 1])

    # return the ENUM that matches the value
    @staticmethod
    def get_from_value(b:bv.BitVector):
        if b == UARTOptions.OPT_8_N_1.value:
            return UARTOptions.OPT_8_N_1
        elif b == UARTOptions.OPT_8_O_1.value:
            return UARTOptions.OPT_8_O_1
        elif b == UARTOptions.OPT_8_E_1.value:
            return UARTOptions.OPT_8_E_1
        elif b == UARTOptions.OPT_8_N_1_ALT.value:
            return UARTOptions.OPT_8_N_1_ALT

# SPED bits 5,4,3
class TTLBaudRates(enum.Enum):
    BPS_1200 = bv.BitVector(bitlist=[0,0,0])
    BPS_2400 = bv.BitVector(bitlist=[0,0,1])
    BPS_4800 = bv.BitVector(bitlist=[0,1,0])
    BPS_9600 = bv.BitVector(bitlist=[0,1,1]) # default
    BPS_19200 = bv.BitVector(bitlist=[1,0,0])
    BPS_38400 = bv.BitVector(bitlist=[1,0,1])
    BPS_57600 = bv.BitVector(bitlist=[1,1,0])
    BPS_115200 = bv.BitVector(bitlist=[1,1,1])

    @staticmethod
    def get_from_value(b:bv.BitVector):
        if b == TTLBaudRates.BPS_1200.value:
            return TTLBaudRates.BPS_1200
        elif b == TTLBaudRates.BPS_2400.value:
            return TTLBaudRates.BPS_2400
        elif b == TTLBaudRates.BPS_4800.value:
            return TTLBaudRates.BPS_4800
        elif b == TTLBaudRates.BPS_9600.value:
            return TTLBaudRates.BPS_9600
        elif b == TTLBaudRates.BPS_19200.value:
            return TTLBaudRates.BPS_19200
        elif b == TTLBaudRates.BPS_38400.value:
            return TTLBaudRates.BPS_38400
        elif b == TTLBaudRates.BPS_57600.value:
            return TTLBaudRates.BPS_57600
        elif b == TTLBaudRates.BPS_115200.value:
            return TTLBaudRates.BPS_115200

# SPED bits 2,1,0
class AirDataRates(enum.Enum):
    BPS_300 = bv.BitVector(bitlist=[0,0,0])
    BPS_1200 = bv.BitVector(bitlist=[0,0,1])
    BPS_2400 = bv.BitVector(bitlist=[0,1,0]) # default
    BPS_4800 = bv.BitVector(bitlist=[0,1,1])
    BPS_9600 = bv.BitVector(bitlist=[1,0,0])
    BPS_19200_0 = bv.BitVector(bitlist=[1,0,1])
    BPS_19200_1 = bv.BitVector(bitlist=[1,1,0])
    BPS_19200_2 = bv.BitVector(bitlist=[1,1,1])

    @staticmethod
    def get_from_value(b:bv.BitVector):
        if b == AirDataRates.BPS_300.value:
            return AirDataRates.BPS_300
        elif b == AirDataRates.BPS_1200.value:
            return AirDataRates.BPS_1200
        elif b == AirDataRates.BPS_2400.value:
            return AirDataRates.BPS_2400
        elif b == AirDataRates.BPS_4800.value:
            return AirDataRates.BPS_4800
        elif b == AirDataRates.BPS_9600.value:
            return AirDataRates.BPS_9600
        elif b == AirDataRates.BPS_19200_0.value:
            return AirDataRates.BPS_19200_0
        elif b == AirDataRates.BPS_19200_1.value:
            return AirDataRates.BPS_19200_1
        elif b == AirDataRates.BPS_19200_2.value:
            return AirDataRates.BPS_19200_2

# OPT bit 7
class FixedTransmissionEnable(enum.Enum):
    FT_TRANSPARENT_TRANSMISSION = bv.BitVector(bitlist=[0]) #default
    FT_FIXED_TRANSMISSION       = bv.BitVector(bitlist=[1])

    @staticmethod
    def get_from_value(b:bv.BitVector):
        if b == FixedTransmissionEnable.FT_FIXED_TRANSMISSION.value:
            return FixedTransmissionEnable.FT_FIXED_TRANSMISSION
        elif b == FixedTransmissionEnable.FT_TRANSPARENT_TRANSMISSION.value:
            return FixedTransmissionEnable.FT_TRANSPARENT_TRANSMISSION

# OPT bit 6
class IODriveMode(enum.Enum):
    DRIVE_MODE_OPEN_COLLECTOR        = bv.BitVector(bitlist=[0])
    DRIVE_MODE_PUSH_PULLS_PULL_UPS   = bv.BitVector(bitlist=[1]) # default

    @staticmethod
    def get_from_value(b:bv.BitVector):
        if b == IODriveMode.DRIVE_MODE_PUSH_PULLS_PULL_UPS.value:
            return IODriveMode.DRIVE_MODE_PUSH_PULLS_PULL_UPS
        elif b == IODriveMode.DRIVE_MODE_OPEN_COLLECTOR.value:
            return IODriveMode.DRIVE_MODE_OPEN_COLLECTOR

# OPT bits 5,4,3
class WirelessWakeupTime(enum.Enum):
    WAKE_UP_250 = bv.BitVector(bitlist=[0,0,0]) # default
    WAKE_UP_500 = bv.BitVector(bitlist=[0,0,1])
    WAKE_UP_750 = bv.BitVector(bitlist=[0,1,0])
    WAKE_UP_1000 = bv.BitVector(bitlist=[0,1,1])
    WAKE_UP_1250 = bv.BitVector(bitlist=[1,0,0])
    WAKE_UP_1500 = bv.BitVector(bitlist=[1,0,1])
    WAKE_UP_1750 = bv.BitVector(bitlist=[1,1,0])
    WAKE_UP_2000 = bv.BitVector(bitlist=[1,1,1])

    @staticmethod
    def get_from_value(b:bv.BitVector):
        if b == WirelessWakeupTime.WAKE_UP_250.value:
            return WirelessWakeupTime.WAKE_UP_250
        elif b == WirelessWakeupTime.WAKE_UP_500.value:
            return WirelessWakeupTime.WAKE_UP_500
        elif b == WirelessWakeupTime.WAKE_UP_750.value:
            return WirelessWakeupTime.WAKE_UP_750
        elif b == WirelessWakeupTime.WAKE_UP_1000.value:
            return WirelessWakeupTime.WAKE_UP_1000
        elif b == WirelessWakeupTime.WAKE_UP_1250.value:
            return WirelessWakeupTime.WAKE_UP_1250
        elif b == WirelessWakeupTime.WAKE_UP_1500.value:
            return WirelessWakeupTime.WAKE_UP_1500
        elif b == WirelessWakeupTime.WAKE_UP_1750.value:
            return WirelessWakeupTime.WAKE_UP_1750
        elif b == WirelessWakeupTime.WAKE_UP_2000.value:
            return WirelessWakeupTime.WAKE_UP_2000

# OPT bit 2
class FECSwitch(enum.Enum):
    FEC_OFF = bv.BitVector(bitlist=[0])
    FEC_ON  = bv.BitVector(bitlist=[1]) # default

    @staticmethod
    def get_from_value(b:bv.BitVector):
        if b == FECSwitch.FEC_ON.value:
            return FECSwitch.FEC_ON
        elif b == FECSwitch.FEC_OFF.value:
            return FECSwitch.FEC_OFF

# OPT bits 1,0
class TXPower(enum.Enum):
    PWR_20DBM = bv.BitVector(bitlist=[0, 0])  # default
    PWR_17DBM = bv.BitVector(bitlist=[0, 1])
    PWR_14DBM = bv.BitVector(bitlist=[1, 0])
    PWR_10DBM = bv.BitVector(bitlist=[1, 1])

    @staticmethod
    def get_from_value(b:bv.BitVector):

        if b == TXPower.PWR_20DBM.value:
            return TXPower.PWR_20DBM
        elif b == TXPower.PWR_17DBM.value:
            return TXPower.PWR_17DBM
        elif b == TXPower.PWR_14DBM.value:
            return TXPower.PWR_14DBM
        elif b == TXPower.PWR_10DBM.value:
            return TXPower.PWR_10DBM

# CHAN bits (full byte)
class CommChannel(enum.Enum):
    pass

# HEAD bits (full byte)
class CommandHEAD(enum.Enum):
    SAVE_ON_PWR_DOWN = bv.BitVector(intVal=0xC0, size=8)
    NO_SAVE_ON_PWR_DOWN = bv.BitVector(intVal=0xC2, size=8)

    @staticmethod
    def get_from_value(b:bv.BitVector):

       if b == CommandHEAD.SAVE_ON_PWR_DOWN.value:
           return CommandHEAD.SAVE_ON_PWR_DOWN
       elif b == CommandHEAD.NO_SAVE_ON_PWR_DOWN.value:
           return CommandHEAD.NO_SAVE_ON_PWR_DOWN

class E32Settings:
    # initialize everything to defaults
    def __init__(self):
        self.__ADDH:bv.BitVector(intVal=0, size=8)
        self.__ADDL:bv.BitVector(intVal=0, size=8)
        self.__TTLRate: TTLBaudRates = TTLBaudRates.BPS_9600
        self.__UARTOpt:UARTOptions = UARTOptions.OPT_8_N_1
        self.__AirDataRate:AirDataRates = AirDataRates.BPS_2400
        self.__CHAN:int = 23
        self.__FixedTransmissionEnable = FixedTransmissionEnable.FT_TRANSPARENT_TRANSMISSION
        self.__IODriveMode:IODriveMode = IODriveMode.DRIVE_MODE_PUSH_PULLS_PULL_UPS
        self.__WirelessWakeUpTime = WirelessWakeupTime.WAKE_UP_250
        self.__FECSwitch:FECSwitch = FECSwitch.FEC_ON
        self.__TXPwr:TXPower = TXPower.PWR_20DBM

    def parse_option_bytes(self, optbytes: list):

        if len(optbytes) != 6:
            raise ValueError("Options length incorrect!")
        else:
            _HEAD = bv.BitVector(intVal=optbytes[0], size=8)
            _ADDH = bv.BitVector(intVal=optbytes[1], size=8)
            _ADDL = bv.BitVector(intVal=optbytes[2], size=8)
            _SPED = bv.BitVector(intVal=optbytes[3], size=8)
            _CHAN = bv.BitVector(intVal=optbytes[4], size=8)
            _OPT = bv.BitVector(intVal=optbytes[5], size=8)

            self.__ADDH = _ADDH
            self.__ADDL = _ADDL

            self.__AirDataRate = AirDataRates.get_from_value(_SPED[5:])
            self.__TTLRate = TTLBaudRates.get_from_value(_SPED[2:5])
            self.__UARTOpt = UARTOptions.get_from_value(_SPED[0:2])

            self.__CHAN = int(_CHAN)

            # unfortunately it looks like BitVector returns an int when you request one bit (instead of another BitVector, like slicing does)
            # therefore we have to convert the returned int back into another BitVector
            self.__TXPwr = TXPower.get_from_value(_OPT[6:])
            self.__FECSwitch = FECSwitch.get_from_value(bv.BitVector(intVal=_OPT[5], size=1))
            self.__WirelessWakeUpTime = WirelessWakeupTime.get_from_value(_OPT[2:5])
            self.__IODriveMode = IODriveMode.get_from_value(bv.BitVector(intVal=_OPT[1], size=1))
            self.__FixedTransmissionEnable = IODriveMode.get_from_value(bv.BitVector(intVal=_OPT[0], size=1))

    def setADDH(self, ADDH:int):
        self.__ADDH = ADDH

    def getADDH(self):
        return self.__ADDH

    def setADDL(self, ADDL:int):
        self.__ADDL = ADDL

    def getADDL(self):
        return self.__ADDL

    def setTTLBaudRate(self, rate:TTLBaudRates):
        self.__TTLRate = rate

    def getTTLBaudRate(self):
        return self.__TTLRate

    def setUARTOptions(self, uartOpt:UARTOptions):
        self.__UARTOpt = uartOpt

    def getUARTOptions(self):
        return self.__UARTOpt

    def setAirDataRate(self, rate:AirDataRates):
        self.__AirDataRate = rate

    def getAirDataRate(self):
        return self.__AirDataRate

    def setCHAN(self, channel:int):
        if channel > 31:
            channel = 31

        if channel < 0:
            channel = 0

        self.__CHAN = channel

    def getCHAN(self):
        return self.__CHAN

    def setTXMode(self, mode:FixedTransmissionEnable):
        self.__FixedTransmissionEnable = mode

    def getTXMode(self):
        return self.__FixedTransmissionEnable

    def setIODriveMode(self, mode:IODriveMode):
        self.__IODriveMode = mode

    def getIODriveMode(self):
        return self.__IODriveMode

    def setWirelessWakeUpTime(self, t:WirelessWakeupTime):
        self.__WirelessWakeUpTime = t

    def getWirelessWakeUpTime(self):
        return self.__WirelessWakeUpTime

    def setFECSwitch(self, mode:FECSwitch):
        self.__FECSwitch = mode

    def getFECSwitch(self):
        return self.__FECSwitch

    def setTXPwr(self, power:TXPower):
        self.__TXPwr = power

    def getTXPwr(self):
        return self.__TXPwr

    # returns a bytearray you can write directly to the serial port
    def get_param_bytes(self, head:CommandHEAD):

        _HEAD = head.value.int_val()
        _ADDH = int(self.__ADDH)
        _ADDL = int(self.__ADDL)
        _SPED = E32Settings.get_sped_byte(self.__AirDataRate, self.__TTLRate, self.__UARTOpt)
        _CHAN = self.__CHAN
        _OPT = E32Settings.get_opt_byte(self.__TXPwr, self.__FECSwitch, self.__WirelessWakeUpTime, self.__IODriveMode, self.__FixedTransmissionEnable)

        return bytearray([_HEAD, _ADDH, _ADDL, _SPED, _CHAN, _OPT])

    # assemble a byte (using BitVector) containing all of the bits for the SPED byte
    @staticmethod
    def get_sped_byte(air_rate: AirDataRates, ttl_rate: TTLBaudRates, uart_opt: UARTOptions):
        ret = bv.BitVector(intVal=0, size=8)
        ret[0:2] = uart_opt.value
        ret[2:5] = ttl_rate.value
        ret[5:] = air_rate.value
        return int(ret)

    # assemble a byte (using BitVector) containing all the bits for the OPTION byte
    @staticmethod
    def get_opt_byte(txPwr:TXPower, fecSwitch:FECSwitch, wirelessWakeUpTime:WirelessWakeupTime, ioDriveMode:IODriveMode, fixed:FixedTransmissionEnable):
        ret = bv.BitVector(intVal=0, size=8)
        ret[6:] = txPwr.value
        ret[5] = int(fecSwitch.value)
        ret[2:5] = wirelessWakeUpTime.value
        ret[1] = int(ioDriveMode.value)
        ret[0] = int(fixed.value)
        return int(ret)

    # return a BitVector containing all of the bits for the CHAN byte
    # valid channels are between 0 and 31 (5 low bits)
    @staticmethod
    def getChannelByte(channel: int):

        # just constrain it to the upper or lower limits
        if channel < 0:
            channel = 0

        if channel > 31:
            channel = 31

        ret = bv.BitVector(intVal=channel, size=8)

        return int(ret)

    @staticmethod
    def get_16bit_addr_int(ADDH:bv.BitVector, ADDL:bv.BitVector):
        ret = bv.BitVector(intVal=0, size=16)
        ret[0:8] = ADDH
        ret[8:] = ADDL
        print(ret)
        return int(ret)

    @staticmethod
    def testADDRConcat():
        # ADDH / ADDL
        val = E32Settings.get_16bit_addr_int(bv.BitVector(bitlist=[1, 1, 1, 1, 1, 1, 1, 1]),
                                                 bv.BitVector(bitlist=[1, 1, 1, 1, 1, 1, 1, 1]))
        assert val == 0xffff

    # accepts a list of parameters fetched from the module, instantiates this class,
    # attempts to parse the arguments then concatenate them back into a list of bytes again
    # also prints it for visual comparison
    @staticmethod
    def testModule(params:list):
        HEAD = bv.BitVector(intVal=params[0], size=8)
        ADDH = bv.BitVector(intVal=params[1], size=8)
        ADDL = bv.BitVector(intVal=params[2], size=8)
        SPED = bv.BitVector(intVal=params[3], size=8)
        CHAN = bv.BitVector(intVal=params[4], size=8)
        OPT = bv.BitVector(intVal=params[5], size=8)

        print("HEAD: ", HEAD, "\tADDH: ", ADDH, "\tADDL: ", ADDL, "\tSPED: ", SPED, "\tCHAN: ", CHAN, "\tOPT:  ", OPT)

        # initialize the settings object
        settings = E32Settings()
        # parse the settings we just received
        settings.parse_option_bytes(params)
        # assemble a payload to write to the module
        new_params = settings.get_param_bytes(CommandHEAD.SAVE_ON_PWR_DOWN)

        HEAD2 = bv.BitVector(intVal=new_params[0], size=8)
        ADDH2 = bv.BitVector(intVal=new_params[1], size=8)
        ADDL2 = bv.BitVector(intVal=new_params[2], size=8)
        SPED2 = bv.BitVector(intVal=new_params[3], size=8)
        CHAN2 = bv.BitVector(intVal=new_params[4], size=8)
        OPT2 = bv.BitVector(intVal=new_params[5], size=8)

        print("HEAD: ", HEAD2, "\tADDH: ", ADDH2, "\tADDL: ", ADDL2, "\tSPED: ", SPED2, "\tCHAN: ", CHAN2, "\tOPT:  ", OPT2)

        assert(HEAD == HEAD2)
        assert(ADDH == ADDH2)
        assert(ADDL == ADDL2)
        assert(SPED == SPED2)
        assert(CHAN == CHAN2)
        assert(OPT == OPT2)


ser = serial.Serial('COM18', baudrate=9600)

# get the bytes for the parameters
def readParams():
    ser.write(bytearray([0xC1,0xC1,0xC1]))
    buf = ser.read(6)
    time.sleep(0.1)
    return buf

# get the bytes for the version number of the module
def readVer():
    ser.write(bytearray([0xC3, 0xC3, 0xC3]))
    buf = ser.read(4)
    time.sleep(0.1)
    return buf

# trigger a module reset
def resetModule():
    ser.write(bytearray([0xC4, 0xC4, 0xC4]))
    time.sleep(0.2)

# write the parameters to the module
def writeParams(params:bytearray):
    ser.write(bytearray)
    time.sleep(0.2)
    pass

def sendDataFixed(ADDH:int, ADDL:int, CHAN:int, payload:bytearray):
    pass

print("Reading params:")
ret_params = readParams()
print([hex(x) for x in list(ret_params)])
retList = list(ret_params)

print("Reading version:")
ret_ver = readVer()
print([hex(x) for x in list(ret_ver)])

print("Resetting module:")
resetModule()

E32Settings.testADDRConcat()
E32Settings.testModule(ret_params)


