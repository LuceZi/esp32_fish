#include <Arduino.h>
#include "driver/mcpwm.h"

#define SERVO_GPIO 4                 // Servo 連接到 GPIO4
#define SERVO_MIN_PULSEWIDTH 1000    // -90° (1.0ms)
#define SERVO_MAX_PULSEWIDTH 2000    // +90° (2.0ms)
#define SERVO_CENTER_PULSEWIDTH 1500 // 0° (1.5ms)
#define SERVO_FREQUENCY 50           // 50Hz (20ms 週期)

void setup()
{
    Serial.begin(115200);

    // 初始化 MCPWM
    mcpwm_gpio_init(MCPWM_UNIT_0, MCPWM0A, SERVO_GPIO);
    mcpwm_config_t pwm_config;
    pwm_config.frequency = SERVO_FREQUENCY;
    pwm_config.cmpr_a = 0;
    pwm_config.cmpr_b = 0;
    pwm_config.counter_mode = MCPWM_UP_COUNTER;
    pwm_config.duty_mode = MCPWM_DUTY_MODE_0;
    mcpwm_init(MCPWM_UNIT_0, MCPWM_TIMER_0, &pwm_config);
}

// **角度 (-90° ~ +90°) 轉換成 PWM 脈衝**
uint32_t angle_to_pulsewidth(int angle)
{
    return SERVO_CENTER_PULSEWIDTH + (angle * (SERVO_MAX_PULSEWIDTH - SERVO_CENTER_PULSEWIDTH) / 90);
}

void set_servo_angle(int angle)
{
    uint32_t pulse_width = angle_to_pulsewidth(angle);
    Serial.printf("Setting Servo to %d° (%dus PWM)\n", angle, pulse_width);
    mcpwm_set_duty_in_us(MCPWM_UNIT_0, MCPWM_TIMER_0, MCPWM_OPR_A, pulse_width);
}

void smooth_servo_move(int start_angle, int end_angle, int step, int delay_time)
{
    if (start_angle < end_angle)
    {
        for (int i = start_angle; i <= end_angle; i += step)
        {
            set_servo_angle(i);
            delay(delay_time);
        }
    }
    else
    {
        for (int i = start_angle; i >= end_angle; i -= step)
        {
            set_servo_angle(i);
            delay(delay_time);
        }
    }
}

void loop()
{

    smooth_servo_move(90, -90, 2, 10); // 右邊 → 左邊
    delay(1000);
    smooth_servo_move(-90, 90, 2, 10); // 左邊 → 右邊
    delay(1000);
}
