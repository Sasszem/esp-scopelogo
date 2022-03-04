#include <driver/dac.h>

extern char shape[];
extern int length;

void setup() {
  // put your setup code here, to run once:
  dac_output_enable(DAC_CHANNEL_1);
  dac_output_enable(DAC_CHANNEL_2);
  
}

void loop() {
  // put your main code here, to run repeatedly:
  // draw a circle
  for (int i = 0; i<length;i++) {
    dac_output_voltage(DAC_CHANNEL_1, shape[2*i]);
    dac_output_voltage(DAC_CHANNEL_2, shape[2*i+1]);
    delayMicroseconds(1); // nagy hogy lássuk
  }
}
