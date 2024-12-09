

const uint8_t DOELPOORT = 13;
const uint16_t VERTRAGING_KNIPPER_MILISECONDEN = 100;


void knipper_led()
{
  digitalWrite(DOELPOORT, HIGH);

  delay(VERTRAGING_KNIPPER_MILISECONDEN);

  digitalWrite(DOELPOORT, LOW);

  delay(VERTRAGING_KNIPPER_MILISECONDEN);
}


void setup()
{
  pinMode(DOELPOORT, OUTPUT);
}


void loop()
{
  knipper_led();
}
