from Adafruit_PCA9685 import PCA9685

pca = PCA9685(address=0x40, busnum=1)  # Для Raspberry Pi 4 используйте busnum=1
pca.set_pwm_freq(60)
print("Успешная инициализация!")
