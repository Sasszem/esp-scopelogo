#include <driver/dac.h>

extern char data[];
extern int sizes[];
extern int starts[];
extern int count;

int selected_index = 0;

const int BUTTON_PIN = 13;

void setup() {
  // put your setup code here, to run once:
  dac_output_enable(DAC_CHANNEL_1);
  dac_output_enable(DAC_CHANNEL_2);
  pinMode(BUTTON_PIN, INPUT_PULLUP);
  pinMode(LED_BUILTIN, OUTPUT);
  digitalWrite(LED_BUILTIN, LOW);
}

int handle_button() {
  static int last_change;
  static bool last_value;
  int new_value = digitalRead(BUTTON_PIN);
  if (new_value != last_value && (millis()-last_change) > 100) {
    last_value = new_value;
    last_change = millis();
    if (!new_value) {
      return true;
    }
  }
  return false;
}

void loop() {
  // put your main code here, to run repeatedly:
  // draw a circle
  int limit = sizes[selected_index];
  char* data_start = &data[starts[selected_index] * 2];
  for (int i = 0; i<limit;i++) {
    dac_output_voltage(DAC_CHANNEL_1, data_start[2*i]);
    dac_output_voltage(DAC_CHANNEL_2, data_start[2*i+1]);
    delayMicroseconds(1); // nagy hogy lássuk
  }
  
  if (handle_button())
    selected_index = (selected_index + 1) % count;
  
}
