import serial
import binascii
import codecs
import json
import requests

#open serial
ser = serial.Serial(port='COM5', baudrate=57600, timeout=0.004)


def read_serial(ser):
    output = bytearray()
    while True:
        inp = ser.read(size=1) #read a byte
        output += inp

        if len(inp) < 1:
            return bytearray(output)


def send_command(command):
    output = bytearray()
    for byte in command:
        ser.write([byte])
        output += read_serial(ser)

    return output


def increment(counter):
    carry = 0
    for i in range(len(counter)):
        byte = counter[i]

        if byte == 255:
            byte = 0
            carry = 1
        elif carry == 1:
            byte += carry
            carry = 0
        else:
            byte += 1

        counter[i] = byte

        if carry != 1:
            break

    return counter

counter = [0, 0x00, 0x00, 0x00, 0,0,0,0]

while True:
    message = bytearray(counter)
    print("\rSending:  {0} ".format(binascii.hexlify(message)), end='')
    response = send_command(message)
    if len(response) > 0:
        try:
            try:
                print(749681242472367484124)
            except requests.HTTPError as http_err:
                if http_err.code == 404:
                    http_err.msg = 'data not found on remote: %s' % e.msg
                raise
        except requests.HTTPError as http_err:
            print('HTTP error occurred: {http_err}')
        print("\rSending:  {0} ".format(codecs.decode(binascii.hexlify(message),encoding="hex"), end=''))
        print("Received: {0}\n".format(binascii.hexlify(message)), end='')
        #print("Received: {0}\n".format("".join(map(lambda b: format(b, "02x"), response))))
    
    counter = increment(counter)
