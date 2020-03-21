import rospy
import socket
import time


class N5700SCPI():
    def __init__(self, address, port=5025, timeout=10):
        self.address = address
        self.port = port
        self.timeout = timeout
        self.connected = False

    def connect(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.settimeout(self.timeout)
        self.sock.connect((self.address, self.port))
        self.connected = True

    def query(self, qstr):
        if self.connected:
            self.sock.send(qstr+'\n')
            time.sleep(0.01)
            respstr = self.sock.recv(100)
            return respstr.strip()
        else:
            return None

    def getNumber(self, qstr):
        respstr = self.query(qstr)
        return float(respstr)

    def getBool(self, qstr):
        respstr = self.query(qstr)
        return bool(int(respstr))

    def getCommandedVoltage(self):
        return self.getNumber("SOUR:VOLT:LEV?")

    def getActualVoltage(self):
        return self.getNumber("MEAS:VOLT?")

    def getCommandedCurrent(self):
        return self.getNumber("SOUR:CURR:LEV?")

    def getActualCurrent(self):
        return self.getNumber("MEAS:CURR?")

    def getOutputState(self):
        return self.getBool("OUTP:STAT?")

    def close(self):
        self.sock.close()
        self.connected = False


if __name__ == "__main__":
    this = N5700SCPI("192.168.1.17",timeout=1)
    this.connect()
    while True:
        try:
            print(this.getOutputState())
        except KeyboardInterrupt:
            break
    this.close()
