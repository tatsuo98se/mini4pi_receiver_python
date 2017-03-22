from datetime import datetime

class Motor:

    def __init__(self, pin_motor_in1, pin_motor_in2,
                 pin_motor_pwm, pin_servo_pwm, options):

        self.pin_motor_in1 = pin_motor_in1
        self.pin_motor_in2 = pin_motor_in2
        self.pin_motor_pwm = pin_motor_pwm
        self.pin_servo_pwm = pin_servo_pwm
        self.update_last_operation_date()

    def driveMotor(self, x, y):
        if (x == 0 and y == 0) or ((int(datetime.now().strftime('%s')) - self.last_update) > 1):
            self.set_motor_params(0.0, False, False)
            self.set_steering_params(0)
            return

        if (int(datetime.now().strftime('%s')) - self.last_update) > 2:
            self.sleep()
            return

        print("drive motor: " + str(x) + ", " + str(y))
        pwm = min(abs(y)/100.0, 1)
        if y > 0:
            self.set_motor_params(pwm, False, True)
        else:
            self.set_motor_params(pwm, True, False)

        steering = x/100.0
        if x > 0:
            steering = min(steering, 1)
        else:
            steering = max(steering, -1)

        self.set_steering_params(steering)

    def update_last_operation_date(self):
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
        print("sleep")


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
        