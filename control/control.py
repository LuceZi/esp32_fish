import serial

class Control:
    def __init__(self, port='COM4', baudrate=115200):
        """初始化 UART 連線"""
        try:
            self.ser = serial.Serial(port, baudrate, timeout=1)
            print(f"🔗 連接至 {port} 成功！")
        except Exception as e:
            print(f"❌ UART 連線失敗: {e}")
            self.ser = None
            raise e

    def send_command(self, command):
        """發送指令到 ESP32"""
        if self.ser and self.ser.is_open:
            self.ser.write((command + '\n').encode())
            print(f"🚀 指令發送成功: {command}")
        else:
            print("⚠️ UART 連線未開啟，無法發送指令")

    def close(self):
        """關閉 UART 連線"""
        if self.ser and self.ser.is_open:
            self.ser.close()
            print("🔌 關閉 UART 連線")
