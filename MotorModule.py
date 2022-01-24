import RPi.GPIO as GPIO
from time import sleep
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

class Motor():
  def __init__(self,enA,enB,In1A,In2A,In1B,In2B):
    self.enA = enA
    self.enB = enB
    self.In1A = In1A
    self.In2A = In2A
    self.In1B = In1B
    self.In2B = In2B
    GPIO.setup(self.enA,GPIO.OUT)
    GPIO.setup(self.enB,GPIO.OUT)
    GPIO.setup(self.In1A,GPIO.OUT)
    GPIO.setup(self.In2A,GPIO.OUT)
    GPIO.setup(self.In1B,GPIO.OUT)
    GPIO.setup(self.In2B,GPIO.OUT)
    self.pwmA = GPIO.PWM(self.enA, 100)
    self.pwmA.start(0)
    self.pwmB = GPIO.PWM(self.enB, 100)
    self.pwmB.start(0)

  def move(self,speed= 0.5,turn = 0, t= 0):
    speed *= 100
    turn *= 100
    left_speed = speed - turn 
    right_speed = speed + turn 
    if left_speed > 100 :
      left_speed = 100
    elif left_speed < -100:
      left_speed = -100
    if right_speed > 100:
      right_speed = 100
    elif right_speed <-100:
      right_speed = -100
    
    self.pwmA.ChangeDutyCycle(abs(left_speed))
    self.pwmB.ChangeDutyCycle(abs(right_speed))

    if left_speed >0:
      GPIO.output(self.In1A, GPIO.HIGH)
      GPIO.output(self.In2A,GPIO.LOW)
    else:
      GPIO.output(self.In1A, GPIO.LOW)
      GPIO.output(self.In2A,GPIO.HIGH)
    
    if right_speed >0:
      GPIO.output(self.In1B,GPIO.HIGH)
      GPIO.output(self.In2B,GPIO.LOW)
    else:
      GPIO.output(self.In1B,GPIO.LOW)
      GPIO.output(self.In2B,GPIO.HIGH)

    sleep(t)
  def stop(self,t=0):
    self.pwmA.ChangeDutyCycle(0)
    self.pwmB.ChangeDutyCycle(0)
    sleep(t)

# def main():
#   motor.move(0.6,0,2)
#   motor.stop(2)
#   motor.move(-0.5,0.2,2)
#   motor.stop(2)

# if __name__ == '__main__':
#   motor = Motor(2,3,4,17,22,27) #RPi pin configuration
#   main()