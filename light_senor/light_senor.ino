

const uint8_t POORT_LICHTSENSOR = A0;
const uint8_t KNOPPOORT = 2;
const uint16_t ONDERGRENS_FADE = 0;
const uint16_t BOVENGRENS_FADE = 255;
const uint8_t VERTRAGING_PRINTS = 1000;
const uint16_t PC_CONNECTION_BOUD = 9600;


void print_lichtwaarde(const uint16_t lichtwaarde)
{
  Serial.print("\nLichtwaarde sensor: ");
  Serial.print(lichtwaarde);
  Serial.print(".\n----------------------------------------------------------------------------------------------\n");
}


void setup()
{
  pinMode(POORT_LICHTSENSOR, INPUT);

  Serial.begin(PC_CONNECTION_BOUD);
}


void loop()
{
  uint16_t lichtwaarde = analogRead(POORT_LICHTSENSOR);

  print_lichtwaarde(lichtwaarde);

  delay(VERTRAGING_PRINTS);
}
