#include <Servo.h>


Servo servomotor;


const uint8_t POORT_SERVOMOTOR = 11;
const uint8_t POORT_LICHTSENSOR1 = A0;
const uint8_t POORT_LICHTSENSOR2 = A1;
const uint8_t MINIMUMGRAAD_SERVO = 0;
const uint8_t MAXIMUMGRAAD_SERVO = 180;
const uint8_t MINIMAAL_VERSCHIL_LICHTWAARDE_VOOR_BEWEGING = 2;
const uint8_t MINIMALE_LICHTWAARDE_VOOR_BEWEGING = 15;
const uint16_t PC_CONNECTION_BOUD = 9600;
const uint32_t SLAAPTIJD_TUSSEN_LUSSEN_MILISECONDEN = 10000;


void setup()
{
  Serial.begin(PC_CONNECTION_BOUD);

  servomotor.attach(POORT_SERVOMOTOR);
  
  delay(SLAAPTIJD_TUSSEN_LUSSEN_MILISECONDEN / 2);
}


void print_draai_informatie(const uint8_t graad)
{
  Serial.print("Motor beweegt richting ");
  Serial.print(graad);
  Serial.print(" ...\n");
}


void draai_servomotor(const uint8_t graad_nieuwe_positie)
{
  if (servomotor.read() == graad_nieuwe_positie)
  {
    Serial.print("Motor al op positie; geen beweging vereist.\n");

    return;
  }

  servomotor.write(graad_nieuwe_positie);
}


void loop()
{
  uint16_t lichtwaarde_sensor1 = analogRead(POORT_LICHTSENSOR1);
  uint16_t lichtwaarde_sensor2 = analogRead(POORT_LICHTSENSOR2);

  if ((lichtwaarde_sensor1 < MINIMALE_LICHTWAARDE_VOOR_BEWEGING) && (lichtwaarde_sensor2 < MINIMALE_LICHTWAARDE_VOOR_BEWEGING))
    Serial.print("Zowel de waarde van lichtsenor 1 als 2 is te laag voor enige beweging.\n");

  if ((lichtwaarde_sensor1 > lichtwaarde_sensor2) && ((lichtwaarde_sensor1 - lichtwaarde_sensor2) > MINIMAAL_VERSCHIL_LICHTWAARDE_VOOR_BEWEGING))
  {
    Serial.print("Lichtsensor1 is het grootst.\n");

    print_draai_informatie(MINIMUMGRAAD_SERVO);
    draai_servomotor(MINIMUMGRAAD_SERVO);
  }
  else if ((lichtwaarde_sensor2 > lichtwaarde_sensor1) && ((lichtwaarde_sensor2 - lichtwaarde_sensor1) > MINIMAAL_VERSCHIL_LICHTWAARDE_VOOR_BEWEGING))
  {
    Serial.print("Lichtsensor2 is het grootst.\n");
    
    print_draai_informatie(MAXIMUMGRAAD_SERVO);
    draai_servomotor(MAXIMUMGRAAD_SERVO);
  }
  else
  {
    Serial.print("Geen sensor is significant lichter dan de ander; geen beweging vereist.\n");
  }

  Serial.print("\n---------------------------------------------------------------------------\n");

  delay(SLAAPTIJD_TUSSEN_LUSSEN_MILISECONDEN);
}
