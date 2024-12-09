#include <NewPing.h>


const uint8_t POORT_LEDLICHT = 13;
const uint8_t TRIGGER_PIN = 12;
const uint8_t ECHO_PIN = 11;
const uint8_t MAX_DISTANCE = 200;
const uint16_t SLAAPTIJD_TUSSEN_PING = 2000;
const uint16_t PC_CONNECTION_BOUD = 9600;
const uint8_t DUUR_KNIPPER_LEDLICHT = 100;


NewPing sonar(TRIGGER_PIN, ECHO_PIN, MAX_DISTANCE);


void setup()
{
  pinMode(POORT_LEDLICHT, OUTPUT);

  Serial.begin(PC_CONNECTION_BOUD);
}


double microseconden_naar_centimeter(const uint32_t microseconden)
{
  return ((double)microseconden / 58.773);
}


void loop()
{
  uint32_t afstand_microseconden = sonar.ping();
  double afstand_centimeters = microseconden_naar_centimeter(afstand_microseconden);

  delay(SLAAPTIJD_TUSSEN_PING);

  Serial.print("\nPingwaarde sonar cm: ");
  Serial.println(afstand_centimeters);

  if (afstand_centimeters < 10.0d)
  {
    Serial.println("Dichtbij!\n");

    digitalWrite(POORT_LEDLICHT, HIGH);
    delay(DUUR_KNIPPER_LEDLICHT);
  }
}

