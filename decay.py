#!/bin/bash
import math,os,sys,socket,fcntl,struct,smbus,serial,select,curses
import time as t
from datetime import datetime
now=datetime.now()

command=('sudo numlockx on &')
os.system(command)
os.system('exit')

I2C_ADDR  = 0x27 # Check if correct
LCD_WIDTH = 16
LCD_CHR = 1
LCD_CMD = 0
LCD_LINE_1 = 0x80 # LCD RAM address for the 1st line
LCD_LINE_2 = 0xC0 # LCD RAM address for the 2nd line
LCD_BACKLIGHT  = 0x08  # On
#LCD_BACKLIGHT = 0x00  # Off
ENABLE = 0b00000100
E_PULSE = 0.0005
E_DELAY = 0.0005
bus = smbus.SMBus(1) # Some Raspberry pi models use 0 instead

def lcd_byte(bits, mode):
  bits_high = mode | (bits & 0xF0) | LCD_BACKLIGHT
  bits_low = mode | ((bits<<4) & 0xF0) | LCD_BACKLIGHT
  bus.write_byte(I2C_ADDR, bits_high)
  lcd_toggle_enable(bits_high)
  bus.write_byte(I2C_ADDR, bits_low)
  lcd_toggle_enable(bits_low)

def lcd_toggle_enable(bits):
  t.sleep(E_DELAY)
  bus.write_byte(I2C_ADDR, (bits | ENABLE))
  t.sleep(E_PULSE)
  bus.write_byte(I2C_ADDR,(bits & ~ENABLE))
  t.sleep(E_DELAY)

def lcd_string(message,line):
  message = message.ljust(LCD_WIDTH," ")
  lcd_byte(line, LCD_CMD)
  for i in range(LCD_WIDTH):
    lcd_byte(ord(message[i]),LCD_CHR)

def initialise():
  lcd_byte(0x33,LCD_CMD) # 110011 Initialise
  lcd_byte(0x32,LCD_CMD) # 110010 Initialise
  lcd_byte(0x06,LCD_CMD) # 000110 Cursor move direction
  lcd_byte(0x0C,LCD_CMD) # 001100 Display On,Cursor Off, Blink Off 
  lcd_byte(0x28,LCD_CMD) # 101000 Data length, number of lines, font size
  lcd_byte(0x01,LCD_CMD) # 000001 Clear display

# Decay constant value in min^-1 for each isotope
def decay_constant(isotope):
        if isotope==  "Tc-99m":
                return 0.0019231651
        elif isotope=="Ga-67 ":
                return 0.0001475771
        elif isotope=="I-123":
                return 0.0008738618
        elif isotope=="I-131":
                return 0.0000599801
        elif isotope=="F-18 ":
                return 0.0063024839
        elif isotope=="Y-90 ":
                return 0.0001805071
        elif isotope=="Cr-51 ":
                return 0.0000173758
        elif isotope=="In-111":
                return 0.0001716234
        else:
            while 1:
                lcd_byte(0x01,LCD_CMD)
                lcd_string("Isotope ",LCD_LINE_1)
                lcd_string("not stored ",LCD_LINE_2)
                t.sleep (1)
                lcd_byte(0x01,LCD_CMD)
                main()
                
def main():
  global LCD_BACKLIGHT, hour, minute
  try:
    while 1:
          key=curses.initscr()
          curses.cbreak()
          curses.noecho()
          key.keypad(1)
          key.nodelay(1)
          for i in range(120):         # Change value to modify the time before screen turns off
              current_time=str(datetime.now().time())
              os.system('cls' if os.name=='nt' else 'clear')
              ser = serial.Serial('/dev/ttyS0', 9600)     # Depending on Raspberry model ttySO might be ttyserial0 or ttyAMA0 instead. Check dose calibrator manual for serial connection parameters
              t.sleep(1)
              data=ser.read(17).strip().decode()

              # VDC-404 sends data as "<isotope>: <activity> <unit>". To modify for other dose calibrators parse the string it sends accordingly to extract the isotope, activity (Ao) and unit data              
              Ao=data[data.index(":")+1:data.index(" ",6)]
              unit=data[data.index(" ",6)+1:data.index(" ",6)+4]
              isotope=data[0:data.index(":")]

              # Decay calculation
              t0=60*int(current_time[0:2])+int(current_time[3:5])
              t1=int(hour)*60+int(minute)
              A=float(Ao)*math.exp(-decay_constant(isotope)*(t1-t0))

              # Output strings for each LCD line
              output_line1=str(round(A,1))+" "+str(unit)
              for i in range(11-len(output_line1)):
                output_line1+=" "
              output_line1+=str(hour)+":"+str(minute)

              output_line2=str(isotope)
              for i in range(11-len(isotope)):
                output_line2+=" "
              output_line2+=str(current_time)[0:5]

              lcd_string(output_line1,LCD_LINE_1)
              lcd_string(output_line2,LCD_LINE_2)

              # Monitors keypresses. "-" restarts the program to adjust CPU time
              k=key.getch()-48
              if k==-3:
                curses.nocbreak()
                start()
              if -1<k<10:
                  key.nodelay(0)
                  decay_time=str(k)
                  output_line1=output_line1[0:11]
                  output_line1+=str(k)
                  lcd_string(output_line1,LCD_LINE_1)
                  for i in range(3):
                      k=key.getch()-48
                      if -1<k<10:
                        decay_time+=str(k)
                        output_line1+=str(k)
                        if i==0:
                          output_line1+=":"
                        lcd_string(output_line1,LCD_LINE_1)
                  key.nodelay(1)
                  if int(decay_time[0:2])<25 and int(decay_time[2:4])<60:
                    hour=decay_time[0:2]
                    minute=decay_time[2:4]
                  main()

          # Turns off the screen and waits for input
          LCD_BACKLIGHT = 0x00
          initialise()
          while True:
            k=key.getch()
            if k>-1:
              LCD_BACKLIGHT = 0x08
              initialise()
              break

  except:
    main()

def start():
  global hour, minute
  try:
    lcd_byte(0x01,LCD_CMD)

    # CPU time adjust
    while 1:
      lcd_string("Current time?",LCD_LINE_1)
      key=curses.initscr()
      curses.cbreak()
      curses.noecho()
      key.keypad(1)
      key.nodelay(1)
      k=key.getch()-48
      if -1<k<10:
                  key.nodelay(0)
                  corrected_time=str(k)
                  output_line2=""
                  output_line2+=str(k)
                  lcd_string(output_line2,LCD_LINE_2)
                  for i in range(3):
                      k=key.getch()-48
                      if -1<k<10:
                        corrected_time+=str(k)
                        output_line2+=str(k)
                        if i==0:
                          output_line2+=":"
                        lcd_string(output_line2,LCD_LINE_2)
                  key.nodelay(1)
                  if int(corrected_time[0:2])<25 and int(corrected_time[2:4])<60:
                    h=corrected_time[0:2]
                    m=corrected_time[2:4]

                    command='sudo date -s " '+h+":"+m+'"&'
                    os.system(command)
                    os.system('exit')
                    ser = serial.Serial('/dev/ttyS0', 9600)
                    t.sleep(0.5)
                    data=ser.read(17).strip().decode()
                    current_time=str(datetime.now().time())
                    hour=current_time[0:2]
                    minute=current_time[3:5]
                    lcd_byte(0x01,LCD_CMD)
                    main()
                  lcd_byte(0x01,LCD_CMD)
  except:
    start()


initialise()
t.sleep(E_DELAY)
start()

