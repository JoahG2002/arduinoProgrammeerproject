#include <Servo.h>


Servo controlemotor;


const uint8_t POORT_CONTROLEMOTOR = 9;
const uint8_t ONDERGRENS_GRAAD_DRAAI = 0;
const uint8_t BOVENGRENS_GRAAD_DRAAI = 180;
const uint8_t SLAAPTIJD_TUSSEN_DRAAI = 1000;
const uint16_t PC_CONNECTION_BOUD = 9600;


void setup()
{
  controlemotor.attach(POORT_CONTROLEMOTOR);

  Serial.begin(PC_CONNECTION_BOUD);
}


void draai_motor_volledig()
{
  controlemotor.write(ONDERGRENS_GRAAD_DRAAI);

  delay(SLAAPTIJD_TUSSEN_DRAAI);

  controlemotor.write(BOVENGRENS_GRAAD_DRAAI);
  delay(SLAAPTIJD_TUSSEN_DRAAI);
}


void loop()
{
  Serial.print("\nDe motor draait.\n");
  
  draai_motor_volledig();
}
