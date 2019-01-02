from motor import Motor
import RPi.GPIO as GPIO

class RealMotor(Motor):

    MAX_LEFT_VALUE = 6
    MAX_RIGHT_VALUE = 8
    CENTER = 7
    CLOCK = 50

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
        GPIO.cleanup()
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(pin_motor_in1, GPIO.OUT)
        GPIO.setup(pin_motor_in2, GPIO.OUT)
        GPIO.setup(pin_motor_pwm, GPIO.OUT)
        GPIO.setup(pin_servo_pwm, GPIO.OUT)

        self.pin_motor_in1 = pin_motor_in1
        self.pin_motor_in2 = pin_motor_in2
        self.pin_motor_pwm = pin_motor_pwm
        self.pin_servo_pwm = pin_servo_pwm
        self.motor = GPIO.PWM(pin_motor_pwm, self.CLOCK)
        self.stearing = GPIO.PWM(pin_servo_pwm, self.CLOCK)


    def set_motor_params(self, pwm, in1, in2):
        Motor.set_motor_params(self, pwm, in1, in2)
        if in1:
            GPIO.output(self.pin_motor_in1, 1)
        else:
            GPIO.output(self.pin_motor_in1, 0)

        if in2:
            GPIO.output(self.pin_motor_in2, 1)
        else:
            GPIO.output(self.pin_motor_in2, 0)

        self.motor.start(0)
        self.motor.ChangeDutyCycle(pwm)


    def set_steering_params(self, steering_in_percent):
        Motor.set_steering_params(self, steering_in_percent)
        stearing_value = 0
        if steering_in_percent > 0:
            steering_in_percent = min(steering_in_percent, 1)
            stearing_value = self.CENTER - \
             (self.CENTER - self.MAX_LEFT_VALUE) * abs(steering_in_percent)
        elif steering_in_percent < 0:
            steering_in_percent = max(steering_in_percent, -1)
            stearing_value = self.CENTER + \
             (self.MAX_RIGHT_VALUE - self.CENTER) * abs(steering_in_percent)
        else:
            stearing_value = self.CENTER

        self.stearing.start(stearing_value)
        print("stearing_value:" + str(stearing_value))

    def sleep(self):
	Motor.sleep(self)
        self.motor.start(0)
        self.stearing.start(0)
        GPIO.output(self.pin_motor_in1, 0)
        GPIO.output(self.pin_motor_in1, 0)
