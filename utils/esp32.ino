#include <Arduino.h>
#include <HardwareSerial.h>

#define LED_PIN 2 // ESP32 的內建 LED，某些板子沒有內建 LED，可改接其他腳位
// 定義 Servo 相關參數
const int servoPin = 4; // Servo 接在 GPIO4
const int pwmChannel = 0;
const int pwmFreq = 50;       // Servo 通常使用 50Hz PWM 頻率
const int pwmResolution = 16; // 16-bit 解析度（ESP32 的 LEDC 支援 16-bit）

// 角度對應的 PWM 值（根據 Servo 需求調整）
const int minPulse = 500;  // 0°（500us）
const int maxPulse = 2500; // 180°（2500us）

HardwareSerial mySerial(2); // 使用 UART2（GPIO16 RX, GPIO17 TX）

int angleToPWM(int angle);
void led_output(void);

void setup()
{
    pinMode(LED_PIN, OUTPUT); // 設定 LED_PIN 為輸出模式

    mySerial.begin(115200, SERIAL_8N1, 16, 17); // 設定 UART2, GPIO16 RX, GPIO17 TX
    Serial.begin(115200);

    // 設定 PWM 來控制 Servo
    ledcSetup(pwmChannel, pwmFreq, pwmResolution);
    ledcAttachPin(servoPin, pwmChannel);

    Serial.println("ESP32 Servo Control Ready.");
}

void loop()
{

    if (mySerial.available())
    {
        String command = mySerial.readStringUntil('\n'); // 讀取到換行符號
        command.trim();                                  // 去掉首尾空格

        Serial.print("Received: ");
        Serial.println(command);

        if (command == "forward")
        {
            Serial.println("Moving Forward");
            // 這裡加上馬達控制的程式
        }
        else if (command == "backward")
        {
            Serial.println("Moving Backward");
            // 這裡加上馬達控制的程式
        }
        else if (command == "stop")
        {
            Serial.println("Stopping");
            // 這裡加上馬達停止的程式
        }
    }
}

int angleToPWM(int angle)
{
    return map(angle, 0, 180, (minPulse * 65536) / 20000, (maxPulse * 65536) / 20000);
}

void led_output(void)
{
    digitalWrite(LED_PIN, HIGH); // 亮燈
    delay(500);                  // 延遲 500 毫秒
    digitalWrite(LED_PIN, LOW);  // 熄滅
    delay(500);                  // 延遲 500 毫秒
}
