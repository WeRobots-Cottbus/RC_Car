#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile


from pybricks.messaging import BluetoothMailboxServer, TextMailbox, NumericMailbox, BluetoothMailboxClient

def server(): 
    server = BluetoothMailboxServer()
    mboxjoystick = NumericMailbox('Speed', server)
    mboxlenkrad = NumericMailbox('Angle', server)

    print('waiting for connection...')
    server.wait_for_connection()
    ev3 = EV3Brick()
    ev3.speaker.beep(500,100)

    gasm = Motor(Port.A)
    gasm.reset_angle(0)
    lenkm = Motor(Port.B)
    lenkm.reset_angle(0)
    s1 = TouchSensor(Port.S1)
    while True:
        #reset Button status
        reset_pressed = s1.pressed()
        if reset_pressed:
            lenkm.run_target(150,0,Stop.COAST,wait=True)
            lenkm.reset_angle(0)
            lenkm.reset_angle(0)

        #sending speed
        speed = gasm.angle()
        print(speed)
        mboxjoystick.send(float(speed))
        #sending angle
        angle = lenkm.angle()
        print(angle)
        mboxlenkrad.send(float(angle))

def client():
    SERVER = 'server_joy'

    client = BluetoothMailboxClient()
    mboxjoystick = NumericMailbox('Speed', client)
    mboxlenkrad = NumericMailbox('Angle', client)
    speed = 5

    print('establishing connection...')
    client.connect(SERVER)
    ev3 = EV3Brick()
    ev3.speaker.beep(500,100)


    fahrmotor = Motor(Port.A)
    lenkmotor = Motor(Port.B)
    while True:
        speed = mboxjoystick.read()
        angle = mboxlenkrad.read()
        print("Angle: "+str(angle))
        print("Speed: "+str(speed))
        if speed != None:
            speed = int(-speed)
        if speed == None:
            speed = 0
        if angle == None:
            angle = 0
        angle = int(angle*0.7)
        angle = -angle
        speed = speed * 10
        # speed = speed + 45/100 * speed * 4.5/100 * speed * 4.5/100 * speed
        fahrmotor.run(speed)
        if angle > 75:
            angle = 75
        elif angle < -75:
            angle = -75
        lenkmotor.run_target(100,angle, Stop.HOLD, True)
        print("Angleafter: "+str(angle))
        print("Speedafter: "+str(speed))
        
if __name__ == "__main__":
    client()