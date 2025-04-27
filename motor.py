import time
import signal
import sys
from Adafruit_PCA9685 import PCA9685

class MotorController:
    def __init__(self, pca, left_forward_ch, left_backward_ch, right_forward_ch, right_backward_ch):
        self.pca = pca
        self.left_forward_ch = left_forward_ch
        self.left_backward_ch = left_backward_ch
        self.right_forward_ch = right_forward_ch
        self.right_backward_ch = right_backward_ch
        
        # Настройка частоты ШИМ (60Hz подходит для большинства двигателей)
        self.pca.set_pwm_freq(60)

    def _set_motor_speed(self, forward_ch, backward_ch, speed):
        speed = max(0, min(100, speed))  # Ограничение скорости 0-100%
        pwm_value = int(speed * 4095 / 100)  # Преобразование в 12-битное значение

        if speed > 0:
            self.pca.set_pwm(forward_ch, 0, pwm_value)
            self.pca.set_pwm(backward_ch, 0, 0)
        else:
            self.pca.set_pwm(forward_ch, 0, 0)
            self.pca.set_pwm(backward_ch, 0, 0)

    def move_forward(self, speed):
        self._set_motor_speed(self.left_forward_ch, self.left_backward_ch, speed)
        self._set_motor_speed(self.right_forward_ch, self.right_backward_ch, speed)

    def move_backward(self, speed):
        self._set_motor_speed(self.left_backward_ch, self.left_forward_ch, speed)
        self._set_motor_speed(self.right_backward_ch, self.right_forward_ch, speed)

    def stop_motors(self):
        self.pca.set_pwm(self.left_forward_ch, 0, 0)
        self.pca.set_pwm(self.left_backward_ch, 0, 0)
        self.pca.set_pwm(self.right_forward_ch, 0, 0)
        self.pca.set_pwm(self.right_backward_ch, 0, 0)

def signal_handler(sig, frame):
    motor_controller.stop_motors()
    sys.exit(0)

if __name__ == "__main__":
    # Инициализация PCA9685
    pca = PCA9685(address=0x40)  # Проверьте адрес вашего устройства!
    
    # Настройка каналов (измените под вашу конфигурацию!)
    # Формат: (левый мотор вперед, левый назад, правый вперед, правый назад)
    motor_controller = MotorController(pca, 0, 1, 2, 3)
    
    # Регистрация обработчика для безопасного завершения
    signal.signal(signal.SIGINT, signal_handler)

    # Пример использования
    try:
        motor_controller.move_forward(50)  # Движение вперед на 50% скорости
        time.sleep(2)
        motor_controller.move_backward(75) # Движение назад на 75% скорости
        time.sleep(2)
    finally:
        motor_controller.stop_motors()