import as3935
import pigpio

irq_pin_number = 4  # BCM number (code after GPIO)
bus = 1  # On newer Raspberrys is 1
address = 0x03  # If using MOD-1016 this is the address

sensor = as3935.AS3935(irq_pin_number, bus, address)

# We need to calibrate the sensor first. Use the tuning cap provided
# or calculate it using sensor.calculate_tuning_cap(*args)
sensor.full_calibration(12)

sensor.set_indoors(True)


# Every time you sense a pulse on IRQ it means there is an
# interruption request. You can read it like this:
def irq_callback(gpio, level, tick):
    interruption = sensor.get_interrupt()
    if interruption == as3935.INT_NH:
        print("Noise floor too high")
    elif interruption == as3935.INT_D:
        print("Disturbance detected. Mask it?")
    elif interruption == as3935.INT_L:
        print("Lightning detected!")
        distance = sensor.get_distance()


try:
    cb = sensor.pi.callback(irq_pin_number, pigpio.RISING_EDGE, irq_callback)
    while True:
        pass
finally:
    cb.cancel()
    sensor.pi.stop()
