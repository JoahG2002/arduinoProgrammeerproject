

const uint8_t DOELPOORT = 11;   // moet een ~ hebben
const uint16_t ONDERGRENS_FADE = 0;
const uint16_t BOVENGRENS_FADE = 255;
const uint8_t VERTRAGING_PRINTS = 300;
const uint16_t PC_CONNECTION_BOUD = 9600;


void setup()
{
  pinMode(DOELPOORT, OUTPUT);

  Serial.begin(PC_CONNECTION_BOUD);
}


void loop()
{
  Serial.print("\nHallo\n");
  
  delay(VERTRAGING_PRINTS);
}
