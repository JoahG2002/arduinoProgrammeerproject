

const uint8_t DOELPOORT = 11;   // moet een ~ hebben
const uint16_t ONDERGRENS_FADE = 0;
const uint16_t BOVENGRENS_FADE = 255;
const uint8_t VERVAGING_LAMP = 10;


void fade_in_led()
{
  for (uint16_t helderheid = ONDERGRENS_FADE; helderheid < BOVENGRENS_FADE; helderheid++)
  {
    analogWrite(DOELPOORT, helderheid);
    delay(VERVAGING_LAMP);
  }
}


void fade_out_led()
{
  for (uint16_t helderheid = BOVENGRENS_FADE; helderheid > ONDERGRENS_FADE; helderheid--)
  {
    analogWrite(DOELPOORT, helderheid);
    delay(VERVAGING_LAMP);
  }
}

void setup()
{
  pinMode(DOELPOORT, OUTPUT);
}


void loop()
{
  fade_in_led();
  fade_out_led();
}
