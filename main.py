from audio.processor import SpeechProcessor
import time

def main():
    print("🎤 語音辨識系統啟動，請開始說話...")
    
    # 創建語音處理器
    speech_processor = SpeechProcessor()

    # 啟動錄音
    speech_processor.start_recording()

    try:
        while True:
            time.sleep(1)  # 每秒辨識一次
            command = speech_processor.get_command()
            if command:
                print(f"✅ 偵測到語音指令: {command}")
            else:
                print(f"{command}")
                print("⏳ 目前沒有偵測到指令...")
    
    except KeyboardInterrupt:
        print("\n🛑 停止語音辨識")
        speech_processor.stop_recording()

if __name__ == "__main__":
    main()
