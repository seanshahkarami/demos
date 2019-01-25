#include <Adafruit_SSD1306.h>
#include <DHT.h>
#include <DHT_U.h>
#include <math.h>


Adafruit_SSD1306 display(128, 32, &Wire, 4);
DHT dht(5, DHT11);

int light[128];
int lightpos = 0;
int lightmax = 1;

void setup() {
  SerialUSB.begin(9600);

  dht.begin();

  display.begin(SSD1306_SWITCHCAPVCC, 0x3C);
  display.setTextSize(1);
  display.setTextColor(WHITE);
  display.cp437(true);

  for (int i = 0; i < 128; i++) {
    light[i] = 0;
  }
}

void drawString(const char *s) {
  for (; *s != '\0'; s++) {
    display.write(*s);
  }
}

static const char characters[] = "0123456789";

void drawPositiveNumber(int n) {
  if (n >= 10) {
    drawPositiveNumber(n / 10);
  }

  display.write(characters[n % 10]);
}

void drawNumber(int n) {
  if (n < 0) {
    display.write('-');
    drawPositiveNumber(-n);
  } else {
    drawPositiveNumber(n);
  }
}

float temperature = 0.0;
float humidity = 0.0;

void update_temperature();
void update_humidity();
void (*dht_updater)() = update_temperature;

void update_temperature() {
  temperature = dht.readTemperature();
  dht_updater = update_humidity;
}

void update_humidity() {
  humidity = dht.readHumidity();
  dht_updater = update_temperature;
}

unsigned long dht_last_read_time = 0;

void loop() {
  if (millis() - dht_last_read_time > 1000) {
    dht_updater();
    dht_last_read_time = millis();
  }

  SerialUSB.print("temperature ");
  SerialUSB.println(temperature);
  SerialUSB.print("humidity ");
  SerialUSB.println(humidity);
  
  int level = analogRead(A0);

  if (level > lightmax) {
    lightmax = level;
  }

  light[lightpos] = (level * 8) / lightmax;
  lightpos = (lightpos + 1) % 128;

  float t = (float)millis() / 1000.0;

  display.clearDisplay();

  display.setCursor(50 + cos(t)*4, 20 + sin(t)*4);
  drawString("Hello! ^_^");

  for (int i = 0; i < 128; i++) {
    display.drawPixel(i, 8 - light[(i+lightpos) % 128], WHITE);
  }
  
  display.setCursor(0, 14);
  drawString("T ");
  drawNumber(temperature);
  drawString("C");

  display.setCursor(0, 24);
  drawString("H ");
  drawNumber(humidity);
  drawString("%");
  
  display.display();

  delay(10);
}
