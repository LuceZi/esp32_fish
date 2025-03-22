import time
from audio.processor import SpeechProcessor
from control.control import Control

if __name__ == "__main__":
    try:
        print("🚀 啟動語音辨識系統...")    
        print("🎤 語音辨識系統啟動，請開始說話...")
        
        # 創建語音處理器
        speech_processor = SpeechProcessor(buffer_size=4, buffer_step=2)    
        # 創建控制器
        control = Control()  

        # 設定語音辨識結果的回調函數
        speech_processor.command_callback = control.send_command
        # 啟動錄音與語音辨識（**會開一個背景執行緒**）
        speech_processor.start_recording()

        while True:
            time.sleep(1)  # 輪巡偵測語音指令

    except KeyboardInterrupt:
        print("\n🛑 停止語音辨識")
        speech_processor.stop_recording()
        control.close()
    
    except Exception as e:
        print(f"❌ 發生錯誤：{e}")

    finally:
        print("🔚 程式結束 =====================================")
        
