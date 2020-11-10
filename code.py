import board
import busio
import time

i2c = busio.I2C(board.SCL,board.SDA)

# Get a lock on i2c bus
while not i2c.try_lock():
    pass

# Get a list of devices on i2c bus
devices = [hex(x) for x in i2c.scan()]

result = bytearray(6)

# ISL29125 address, 0x44(68)
# Select configuation-1register, 0x01(01)
# 0x0D(13), Operation: RGB, Range: 10000 lux, Res: 16 Bits
i2c.writeto(0x44, bytes([0x01,0x0D]))

loop = 20
for x in range(loop):
    # Read RGB data from sensor
    time.sleep(0.5)
    i2c.writeto_then_readfrom(0x44, bytes([0x09]),result)

    # Convert the data
    green = result[1] * 256 + result[0]
    red = result[3] * 256 + result[2]
    blue = result[5] * 256 + result[4]

    # Output data to the screen
    print("Green Color luminance : %d lux" %green)
    print("Red Color luminance : %d lux" %red)
    print("Blue Color luminance : %d lux" %blue)

i2c.unlock()