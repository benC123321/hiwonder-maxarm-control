import RPi.GPIO as GPIO

GPIO_PIN = 17  # BCM GPIO 17


class GPIOHandler:
    def __init__(self, pin: int = GPIO_PIN):
        self._pin = pin
        self._state = False
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self._pin, GPIO.OUT, initial=GPIO.LOW)

    def toggle(self) -> bool:
        self._state = not self._state
        GPIO.output(self._pin, GPIO.HIGH if self._state else GPIO.LOW)
        return self._state

    def cleanup(self):
        GPIO.cleanup(self._pin)
