import serial
import time

# 設定 UART 連接（請根據你的 ESP32 連接埠修改）
ser = serial.Serial('COM4', 115200, timeout=1)  # Windows 可能是 COM3, COM4
# ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=1)  # Linux/Mac 可能是 ttyUSB0, ttyS0

time.sleep(2)  # 等待連接穩定

def send_command(command):
    ser.write((command + '\n').encode())  # 發送指令，加上換行符
    print(f"Sent: {command}")

# 測試發送指令
send_command("forward")
time.sleep(2)
send_command("backward")
time.sleep(2)
send_command("stop")

ser.close()
