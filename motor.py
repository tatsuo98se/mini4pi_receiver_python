from datetime import datetime
from threading import Thread,Event

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

class Motor:

    def __init__(self, pin_motor_in1, pin_motor_in2,
                 pin_motor_pwm, pin_servo_pwm, options):

        self.__update_last_operation_date()

        self.__old_x = 0
        self.__old_y = 0
        self.__x = 0
        self.__y = 0
        self.__timer = RepeatRun(lambda: self.__apply_motor_params(), 0.2)
        self.__timer.start()
        self.__is_sleep = False

    def stop(self):
        self.__timer.stop()

    def __is_params_changed(self):
        if self.__old_y != self.__y or self.__old_x != self.__x:
            return True
        return False

    def __apply_motor_params(self):
        if not self.__is_params_changed():
            self.sleep()
            return

        self.__is_sleep  = False
        if (int(datetime.now().strftime('%s')) - self.last_update) > 1:
            self.driveMotor(0, 0)
            return

        print("drive motor: " + str(self.__x) + ", " + str(self.__y))
        pwm = min(abs(self.__y)/100.0, 1)
        if self.__y > 0:
            self.set_motor_params(pwm, False, True)
        else:
            self.set_motor_params(pwm, True, False)

        steering = self.__x/100.0
        if self.__x > 0:
            steering = min(steering, 1)
        else:
            steering = max(steering, -1)

        self.set_steering_params(steering)


    def driveMotor(self, x, y):
        self.__update_last_operation_date()
        self.__old_x = self.__x
        self.__old_y = self.__y
        self.__x = x
        self.__y = y

    def __update_last_operation_date(self):
        self.last_update = int(datetime.now().strftime('%s'))

    def set_motor_params(self, pwm, in1, in2):
        print("set_motor_params:" + str(pwm) + ", " + str(in1) + ", " + str(in2))

    # steer_in_percent: -1.0 ~ +1.0
    # -1.0: left
    #  0.0: center
    #  1.0: right
    # max steering degree is depend on implementation of subclass.
    def set_steering_params(self, steering_in_percent):
        print("set_steering_params " + str(steering_in_percent))

    def sleep(self):
        if not self.__is_sleep:
            print("sleep")
        self.__is_sleep = True


class StubMotor(Motor):
    def __init__(self,
                 pin_motor_in1,
                 pin_motor_in2,
                 pin_motor_pwm,
                 pin_servo_pwm,
                 options):

        Motor.__init__(self,
                       pin_motor_in1,
                       pin_motor_in2,
                       pin_motor_pwm,
                       pin_servo_pwm,
                       options)

    def set_motor_params(self, pwm, in1, in2):
        Motor.set_motor_params(self, pwm, in1, in2)

    def set_steering_params(self, steering_in_percent):
        Motor.set_steering_params(self, steering_in_percent)

def merge_two_dicts(x, y):
    z = x.copy()
    z.update(y)
    return z

def createMotor(pin_motor_in1,
                pin_motor_in2,
                pin_motor_pwm,
                pin_servo_pwm,
                options):

    options = merge_two_dicts({"mode":"production",
                              }, options)

    if options["mode"] == "production":
        print("init RealMotor")
        from real_motor import RealMotor
        return RealMotor(pin_motor_in1,
                         pin_motor_in2,
                         pin_motor_pwm,
                         pin_servo_pwm,
                         options)

    else:
        print("init StubMotor")
        return StubMotor(pin_motor_in1,
                         pin_motor_in2,
                         pin_motor_pwm,
                         pin_servo_pwm,
                         options)
        