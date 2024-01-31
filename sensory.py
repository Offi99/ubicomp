import max7219
from machine import Pin, SPI, ADC, I2S
import time
import machine
from rotary_irq_esp import RotaryIRQ

spi = SPI(1, baudrate=10000000, polarity=1, phase=0, sck=Pin(4), mosi=Pin(2))
ss = Pin(5, Pin.OUT)
display = max7219.Matrix8x8(spi, ss, 1)

micro = ADC(Pin(35))

button = Pin(10, Pin.IN)
vibration = Pin(26, Pin.IN)
light = ADC(Pin(39))
white = Pin(22, Pin.OUT)
white.value(0)
blue = Pin(21, Pin.OUT)
blue.value(0)
yellow = Pin(17, Pin.OUT)
yellow.value(0)
red = Pin(23, Pin.OUT)
red.value(0)
green = Pin(19, Pin.OUT)
green.value(0)
orange = Pin(33, Pin.OUT)
orange.value(0)


r = RotaryIRQ(pin_num_clk=27, 
              pin_num_dt=13, 
              min_val=0, 
              max_val=15, 
              reverse=True, 
              range_mode=RotaryIRQ.RANGE_WRAP)

display.fill(0)
display.brightness(1)
display.show()

rot_old = r.value()
button_old = button.value()

def on(bright):
    display.fill(1)
    display.brightness(bright)
    display.show()
    
def off():
    display.fill(0)
    display.show()
    white.value(0)
    blue.value(0)
    yellow.value(0)
    red.value(0)
    green.value(0)
    orange.value(0)
    
while True:
  button_state = button.value()
  if button_state != button_old:
      button_old = button_state
      if button_state == 0:
          print("Push it!")
          yellow.value(1)
          on(15)
          time.sleep(1)
  if vibration.value() != 0:
      print("Shake it!")
      blue.value(1)
      on(15)
      time.sleep(1)
  if light.read() < 3000:
      print("Touch it!")
      white.value(1)
      on(15)
      time.sleep(1)
  if micro.read() > 500:
      print("Clap it!")
      orange.value(1)
      on(15)
      time.sleep(1)
  rot_new = r.value()
  if rot_old != rot_new:
      if rot_new > rot_old:
          if rot_old == 0 and rot_new == 15:
              red.value(1)
              print("Spin it - left!")
          else:
              green.value(1)
              print("Spin it - right!")
      elif rot_new < rot_old:
          if rot_old == 15 and rot_new == 0:
              green.value(1)
              print("Spin it - right!")
          else:
              red.value(1)
              print("Spin it - left!")
      on(rot_new)
      time.sleep(1)
      rot_old = rot_new
  off()
  time.sleep(0.01)