#include "MPU9250.h"
#include <SoftWire.h>
#include <AsyncDelay.h>

SoftWire sw(29, 30);
char swTxBuffer[64];    // These buffers must be at least as large as
char swRxBuffer[64];    // the largest read or write you perform.

MPU9250Setting setting;
MPU9250_<SoftWire> mpu;

void setup() {
    Serial.begin(115200);
    sw.setTxBuffer(swTxBuffer, sizeof(swTxBuffer));
    sw.setRxBuffer(swRxBuffer, sizeof(swRxBuffer));
    sw.setDelay_us(5);
    sw.begin();
    delay(2000);

    if (!mpu.setup(0x68, setting, sw)) {  // change to your own address
        while (1) {
            Serial.println("MPU connection failed. Please check your connection with `connection_check` example.");
            delay(5000);
        }
    }
}

void loop() {
    if (mpu.update()) {
        static uint32_t prev_ms = millis();
        if (millis() > prev_ms + 500) {
            print_data();
            prev_ms = millis();
        }
    }
}

void print_data() {
    Serial.print("Yaw, Pitch, Roll: ");
    Serial.print(mpu.getYaw(), 2);
    Serial.print(", ");
    Serial.print(mpu.getPitch(), 2);
    Serial.print(", ");
    Serial.println(mpu.getRoll(), 2);

    Serial.print("Gyro:             ");
    Serial.print(mpu.getGyroX(), 2);
    Serial.print(", ");
    Serial.print(mpu.getGyroY(), 2);
    Serial.print(", ");
    Serial.println(mpu.getGyroZ(), 2);

    Serial.print("Magnet:           ");
    Serial.print(mpu.getMagX(), 2);
    Serial.print(", ");
    Serial.print(mpu.getMagY(), 2);
    Serial.print(", ");
    Serial.println(mpu.getMagZ(), 2);

    Serial.print("LinearAcceleration: ");
    Serial.print(mpu.getLinearAccX(), 2);
    Serial.print(", ");
    Serial.print(mpu.getLinearAccY(), 2);
    Serial.print(", ");
    Serial.println(mpu.getLinearAccZ(), 2);

    Serial.print("Acceleration:       ");
    Serial.print(mpu.getAccX(), 2);
    Serial.print(", ");
    Serial.print(mpu.getAccY(), 2);
    Serial.print(", ");
    Serial.println(mpu.getAccZ(), 2);
    Serial.println();
}
