from audio.processor import SpeechProcessor
import time
import serial
import time

# 設定 UART 連接（請根據你的 ESP32 連接埠修改）
connect_port = 'COM4'

def send_command(ser, command):
    ser.write((command + '\n').encode())  # 發送指令，加上換行符
    print(f"Sent: {command}")  # 顯示發送的指令

def main(ser):

    print("🎉 連接成功！")
    print("🎤 語音辨識系統啟動，請開始說話...")
    
    # 創建語音處理器
    speech_processor = SpeechProcessor()

    # 啟動錄音
    speech_processor.start_recording()

    try:
        while True:
            time.sleep(1)  # 輪巡偵測語音指令
            command = speech_processor.get_command()
            if command:
                print(f"✅ 偵測到語音指令: {command}")
                send_command(ser, command)

            #else:
                #print("⏳ 目前沒有偵測到指令...")
    
    except KeyboardInterrupt:
        print("\n🛑 停止語音辨識")
        speech_processor.stop_recording()

if __name__ == "__main__":
    ser = None  # 預先定義變數，避免未定義錯誤
    try:
        ser = serial.Serial(connect_port, 115200, timeout=1) # 初始化 UART 連接
        print("🚀 啟動語音辨識系統...")
        print(f"🔗 連接至 {connect_port}...")
        time.sleep(2)  # 等待連接穩定
        main(ser)

    except Exception as e:
        print(f"❌ 發生錯誤：{e}")

    finally:
        if ser and ser.is_open:  # 確保 ser 存在且已打開
            ser.close()
            print("🔌 關閉連接")
        
