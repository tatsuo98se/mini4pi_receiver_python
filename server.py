# coding: UTF-8
import sys
import traceback
import socket
from threading import Thread,Event
import motor as mt

class RepeatRun(Thread):
    def __init__(self, action, interval):
        Thread.__init__(self)
        self.stopped = Event()
        self.action = action
        self.interval = interval

    def run(self):
        while not self.stopped.wait(self.interval):
          self.action()

    def stop(self):
      self.stopped.set()


xdirection = 0
ydirection = 0

#motor
motor = mt.createMotor(4, 17, 13, 12, {"mode":"production"})

#Timer
timers = RepeatRun(lambda: motor.driveMotor(xdirection, ydirection), 0.1)
timers.start()

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
hostname = s.getsockname()[0]
s.close()
print(hostname)

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    serversocket.bind((hostname, 20000))
    serversocket.listen(1)

    while True:
        print('Waiting for connections...')
        sock, client_address = serversocket.accept() #接続されればデータを格納

        # ファイルオブジェクトを作成
        sf = sock.makefile()

        # 1行読み取る場合
        while True:
            line = sf.readline()
            if not line:
                break

            x, y = line.split(",")
            xdirection = int(x)
            ydirection = int(y)
            print("x: " + str(xdirection) + " y:" + str(ydirection))
            motor.update_last_operation_date()

        sock.close()
        print('disconnected.')
except:
    print("Unexpected error:", sys.exc_info()[0])
    print(traceback.format_exc())
    raise
finally:
    timers.stop()
    serversocket.close()
    print('finish')
