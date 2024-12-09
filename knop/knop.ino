

const uint8_t POORT_LEDLICHT = 13;
const uint8_t KNOPPOORT = 2;
const uint8_t VERTRAGING_PRINTS = 1000;
const uint16_t PC_CONNECTION_BOUD = 9600;


void setup()
{
  pinMode(KNOPPOORT, INPUT);
  pinMode(POORT_LEDLICHT, OUTPUT);

  Serial.begin(PC_CONNECTION_BOUD);
}


void loop()
{
  uint8_t knop_aan = digitalRead(KNOPPOORT);

  Serial.print("\nKnopstatus: ");
  Serial.print(knop_aan);
  Serial.print(".\n--------------------------------------------------------------------------------------\n");

  digitalWrite(POORT_LEDLICHT, knop_aan);

  delay(VERTRAGING_PRINTS);
}
