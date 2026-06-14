from gpiozero import DigitalOutputDevice

GPIO_PIN = 17  # BCM GPIO 17


class GPIOHandler:
    def __init__(self, pin: int = GPIO_PIN):
        self._device = DigitalOutputDevice(pin, initial_value=False)

    def toggle(self) -> bool:
        self._device.toggle()
        return bool(self._device.value)

    def cleanup(self):
        self._device.close()
