#include <Arduino.h>
#include <HardwareSerial.h>
#include "driver/mcpwm.h"

// ESP32 的內建 LED，某些板子沒有內建 LED，可改接其他腳位
#define LED_PIN 2

// 定義 Servo 相關參數
#define SERVO1_GPIO 4  // Servo1 連接 GPIO4
#define SERVO2_GPIO 5  // Servo2 連接 GPIO5

#define SERVO_MIN_PULSEWIDTH 1000     // -90° (1.0ms)
#define SERVO_MAX_PULSEWIDTH 2000     // +90° (2.0ms)
#define SERVO_CENTER_PULSEWIDTH 1500  // 0° (1.5ms)
#define SERVO_FREQUENCY 50            // 50Hz (20ms 週期)


uint32_t angle_to_pulsewidth(int angle);
void set_servo_angle(int servo_id, int angle);
void smooth_servo_move(int servo_id, int start_angle, int end_angle, int step, int delay_time);
void led_output(void);

void setup() {
  pinMode(LED_PIN, OUTPUT);  // 設定 LED_PIN 為輸出模式

  Serial.begin(115200);

  // 初始化 Servo1
  mcpwm_gpio_init(MCPWM_UNIT_0, MCPWM0A, SERVO1_GPIO);
  mcpwm_config_t pwm_config;
  pwm_config.frequency = SERVO_FREQUENCY;
  pwm_config.cmpr_a = 0;
  pwm_config.cmpr_b = 0;
  pwm_config.counter_mode = MCPWM_UP_COUNTER;
  pwm_config.duty_mode = MCPWM_DUTY_MODE_0;
  mcpwm_init(MCPWM_UNIT_0, MCPWM_TIMER_0, &pwm_config);

  // 初始化 Servo2
  mcpwm_gpio_init(MCPWM_UNIT_1, MCPWM0A, SERVO2_GPIO);
  mcpwm_init(MCPWM_UNIT_1, MCPWM_TIMER_0, &pwm_config);

  Serial.println("ESP32 Dual Servo Control Ready.");
}

void loop() {

  if (Serial.available()) {
    String command = Serial.readStringUntil('\n');  // 讀取到換行符號
    command.trim();                                 // 去掉首尾空格

    Serial.print("Received: ");
    Serial.println(command);

    if (command == "forward") {
      Serial.println("Moving Forward");
      forward_g(5);
      // 這裡加上馬達控制的程式
    } else if (command == "left") {
      Serial.println("left");
      left_g();
      forward_g(5);
      set_servo_angle(2, 0);
      // 這裡加上馬達控制的程式
    } else if (command == "right") {
      Serial.println("right");
      right_g();
      forward_g(5);
      set_servo_angle(2, 0);
      // 這裡加上馬達停止的程式
    }
  }
}

int gaptime = 5;
int step_set = 5;


// **角度 (-90° ~ +90°) 轉換成 PWM 脈衝**
uint32_t angle_to_pulsewidth(int angle) {
  return SERVO_CENTER_PULSEWIDTH + (angle * (SERVO_MAX_PULSEWIDTH - SERVO_CENTER_PULSEWIDTH) / 90);
}

// **設定 Servo 角度**
void set_servo_angle(int servo_id, int angle) {
  uint32_t pulse_width = angle_to_pulsewidth(angle);
  Serial.printf("Servo %d -> %d° (%dus PWM)\n", servo_id, angle, pulse_width);

  if (servo_id == 1) {
    mcpwm_set_duty_in_us(MCPWM_UNIT_0, MCPWM_TIMER_0, MCPWM_OPR_A, pulse_width);
  } else if (servo_id == 2) {
    mcpwm_set_duty_in_us(MCPWM_UNIT_1, MCPWM_TIMER_0, MCPWM_OPR_A, pulse_width);
  }
}

// **平滑控制 Servo 移動**
void smooth_servo_move(int servo_id, int start_angle, int end_angle, int step, int delay_time) {
  if (start_angle < end_angle) {
    for (int i = start_angle; i <= end_angle; i += step) {
      set_servo_angle(servo_id, i);
      delay(delay_time);
    }
  } else {
    for (int i = start_angle; i >= end_angle; i -= step) {
      set_servo_angle(servo_id, i);
      delay(delay_time);
    }
  }
}

void forward_g(int times) {
  for (int i = 0; i < times; i++) {
    smooth_servo_move(1, 0, 90, step_set, gaptime);
    delay(500);
    smooth_servo_move(1, 90, -90, step_set, gaptime);
    delay(500);
    smooth_servo_move(1, -90, 0, step_set, gaptime);
  }
}

void left_g(void) {
  set_servo_angle(2, 0);
  smooth_servo_move(2, 0, 60, step_set, gaptime);
  delay(100);
}

void right_g(void) {
  set_servo_angle(2, 0);
  smooth_servo_move(2, 0, -60, step_set, gaptime);
  delay(100);
}

void led_output(void) {
  digitalWrite(LED_PIN, HIGH);  // 亮燈
  delay(100);                   // 延遲 500 毫秒
  digitalWrite(LED_PIN, LOW);   // 熄滅
  delay(400);                   // 延遲 500 毫秒
  digitalWrite(LED_PIN, HIGH);  // 亮燈
  delay(100);                   // 延遲 500 毫秒
  digitalWrite(LED_PIN, LOW);   // 熄滅
  delay(400);                   // 延遲 500 毫秒
}
