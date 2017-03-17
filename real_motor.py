from motor import Motor
import RPi.GPIO as GPIO

class RealMotor(Motor):

    MAX_LEFT_VALUE = 0.036
    MAX_RIGHT_VALUE = 0.045
    CENTER = 0.0408
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
        self.motor = GPIO.PWM(pin_motor_pwm, CLOCK)
        self.stearing = GPIO.PWM(pin_servo_pwm, CLOCK)


    def set_motor_params(self, pwm, in1, in2):
        Motor.set_motor_params(self, pwm, in1, in2)
        GPIO.output(self.in1, 1) if in1 else GPIO.output(self.in1, 0)
        GPIO.output(self.in2, 1) if in1 else GPIO.output(self.in2, 0)
        self.motor.start(0)
        self.motor.ChangeDutyCycle(pwm)
    

    def set_steering_params(self, steering_in_percent):
        Motor.set_steering_params(self, steering_in_percent)
        stearing_value = 0
        if steering_in_percent > 0:
            steering_in_percent = min(stearisteering_in_percent, 1)
            stearing_value = CENTER - (CENTER - MAX_LEFT_VALUE) * abs(steering_in_percent)
        elif stearing_value < 0:
            steering_in_percent = max(steering_in_percent, -1)
            stearing_value = CENTER + (MAX_RIGHT_VALUE - CENTER) * abs(steering_in_percent)
        else:
            stearing_value = CENTER
        
        self.stearing.start(pwm)

    def sleep
        self.motor.stop()
        self.stearing.stop()
        GPIO.output(self.in1, 0)
        GPIO.output(self.in2, 0)