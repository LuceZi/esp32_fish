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


    def send_command(self, text):
        """接收 `proc_data`，字元比對後發送指令"""
        if text is None or text.strip() == "":
            #print("⚠️ 無法發送空指令，忽略")
            return
        
        commands = {"前": "forward" , 
                    "左": "left"    , 
                    "右": "right"   ,
                }

        command = None
        for word in commands:
            if word in text:
                command = commands[word]
                break
        
        if command:
            #print(f"✅ 偵測到指令: {command}")
            if self.ser and self.ser.is_open:
                self.ser.write((command + '\n').encode())
                #print(f"🚀 指令發送成功: {command}")
                return command
        else:
            #print(f"🔍 無法辨識指令：{text}")
            return None

    def close(self):
        """關閉 UART 連線"""
        if self.ser and self.ser.is_open:
            self.ser.close()
            print("🔌 關閉 UART 連線")
