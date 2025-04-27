import time
import signal
import sys
from Adafruit_PCA9685 import PCA9685
import Adafruit_GPIO.I2C as I2C  # Добавляем необходимый импорт

class MotorController:
    def __init__(self, pca, left_forward_ch, left_backward_ch, right_forward_ch, right_backward_ch):
        self.pca = pca
        self.channels = {
            'left_forward': left_forward_ch,
            'left_backward': left_backward_ch,
            'right_forward': right_forward_ch,
            'right_backward': right_backward_ch
        }
        self.pca.set_pwm_freq(60)

    def _set_motor(self, forward_ch, backward_ch, speed):
        speed = max(-100, min(100, speed))
        pwm_value = int(abs(speed) * 4095 / 100)

        if speed > 0:
            self.pca.set_pwm(forward_ch, 0, pwm_value)
            self.pca.set_pwm(backward_ch, 0, 0)
        elif speed < 0:
            self.pca.set_pwm(forward_ch, 0, 0)
            self.pca.set_pwm(backward_ch, 0, pwm_value)
        else:
            self.pca.set_pwm(forward_ch, 0, 0)
            self.pca.set_pwm(backward_ch, 0, 0)

    def move_forward(self, speed):
        self._set_motor(self.channels['left_forward'], 
                       self.channels['left_backward'], speed)
        self._set_motor(self.channels['right_forward'], 
                       self.channels['right_backward'], speed)

    def move_backward(self, speed):
        self.move_forward(-speed)

    def stop_motors(self):
        for ch in self.channels.values():
            self.pca.set_pwm(ch, 0, 0)

def signal_handler(sig, frame):
    motor_controller.stop_motors()
    sys.exit(0)

if __name__ == "__main__":
    try:
        # Инициализация PCA9685 с явным указанием шины
        i2c_device = I2C.get_i2c_device(address=0x40, busnum=1)
        pca = PCA9685(i2c=i2c_device)
        
        # Настройка каналов (проверьте свои подключения!)
        motor_controller = MotorController(pca, 
                                          left_forward_ch=0,
                                          left_backward_ch=1,
                                          right_forward_ch=2,
                                          right_backward_ch=3)

        signal.signal(signal.SIGINT, signal_handler)

        print("Starting motor test...")
        motor_controller.move_forward(100)
        time.sleep(2)
        motor_controller.move_backward(100)
        time.sleep(2)

    except Exception as e:
        print(f"Error: {str(e)}")
    finally:
        motor_controller.stop_motors()
        print("Motors stopped")