# coding: UTF-8
import sys
import traceback
import socket
import motor as mt

#motor
motor = mt.createMotor(4, 17, 13, 12, {"mode":"xproduction"})

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
            motor.driveMotor(xdirection, ydirection)

        sock.close()
        print('disconnected.')
except:
    print("Unexpected error:", sys.exc_info()[0])
    print(traceback.format_exc())
    raise
finally:
    serversocket.close()
    print('finish')
    motor.stop()
