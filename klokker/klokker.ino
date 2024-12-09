#include <SPI.h>
#include <time.h>
#include <String.h>
#include <MFRC522.h>
#include <LiquidCrystal_I2C.h>


const uint8_t POORT_LEDLAMPJE_ROOD = 6;
const uint8_t POORT_LEDLAMPJE_BLAUW = 7;
const uint8_t SS_POORT = 10;
const uint8_t RST_POORT = 9;

const uint16_t BAUDVERBINDING = 9600;
const uint16_t ONDERGRENS_LAMPHELDERHEID = 0;
const uint16_t BOVENGRENS_LAMPHELDERHEID = 255;
const uint8_t VERVAGING_LAMP_MILISECONDEN = 2;
const uint16_t WACHTTIJD_OP_SERVER_MILISECONDEN = 550;
const uint16_t SLAAPTIJD_TUSSEN_SCANS = 2000;
const uint8_t MAXIMUMAANTAL_WERKNEMERS = 10;
const uint8_t RIJLENGTE_LCD_SCHERM = 16;
const uint8_t AANTAL_RIJEN_LCD_SCHERM = 2;


struct Werknemer
{
  String id;
  double starttijd_dienst;
};


Werknemer werknemers[MAXIMUMAANTAL_WERKNEMERS];
uint8_t aantal_werknemers = 0;


bool geef_tag_id();
void verwijder_werknemer();
bool werknemer_bestaat_al();
void verwerk_serverreactie();
void voer_taglezertoets_uit();
double geef_starttijd_werknemer();
void geef_reactie_weer_op_lcd(const char* string);
void knipper_ledlampje(const uint8_t poort_ledlampje);
void update_starttijd_werknemer(const double startijd);
void stuur_dienstgegevens_naar_python(const double starttijd_dienst, const double nu);


MFRC522 taglezer(SS_POORT, RST_POORT);
MFRC522::MIFARE_Key sleutel;


LiquidCrystal_I2C lcd_scherm(0x27, RIJLENGTE_LCD_SCHERM, AANTAL_RIJEN_LCD_SCHERM);

byte readCard[4];
String tag_id;


void setup()
{
  pinMode(POORT_LEDLAMPJE_BLAUW, OUTPUT);
  pinMode(POORT_LEDLAMPJE_ROOD, OUTPUT);

  Serial.begin(BAUDVERBINDING);

  SPI.begin();

  taglezer.PCD_Init();

  lcd_scherm.init();
  lcd_scherm.backlight();
  lcd_scherm.setCursor(0, 0);
}


void loop()
{
  // voer_taglezertoets_uit();
  
  if (geef_tag_id())
  {    
    Serial.println(tag_id);

    double nu = (double)time(NULL);
 
    if (!werknemer_bestaat_al())
    {

      update_starttijd_werknemer(nu);

      return;
    }

    double starttijd_dienst = geef_starttijd_werknemer();
    verwijder_werknemer();

    stuur_dienstgegevens_naar_python(starttijd_dienst, nu);

    delay(WACHTTIJD_OP_SERVER_MILISECONDEN);

    verwerk_serverreactie();
  }

  geef_reactie_weer_op_lcd("hallo.");

  Serial.print("Gelezen tag-id: ");
  Serial.print(tag_id);

  delay(SLAAPTIJD_TUSSEN_SCANS);

  return;
}


bool geef_tag_id()
{
  if (!taglezer.PICC_IsNewCardPresent())
  {
    Serial.println("Geen nieuwe kaart.\n");

    return false;
  }

  if (!taglezer.PICC_ReadCardSerial())  // er is geen kaart/tag of deze is niet leesbaar
  {
    Serial.print("Fout bij lezen van de kaart.\n");

    return true;
  }

  tag_id = "leeg";

  for (uint8_t i = 0; i < 4; i++)
  {
    Serial.print("UID Byte ");
    Serial.print(i);
    Serial.print(": ");
    Serial.println(taglezer.uid.uidByte[i], HEX);

    tag_id.concat(String(taglezer.uid.uidByte[i], HEX));
  }

  tag_id.toUpperCase();

  taglezer.PICC_HaltA();

  return true;
}


void verwerk_serverreactie()
{
  if (Serial.available() == 0)
  {
    geef_reactie_weer_op_lcd("FOUT: dienst niet geregistreerd.");

    return;
  }

  String serverreactie = Serial.readString();
  
  if (serverreactie == "-1")
  {
    geef_reactie_weer_op_lcd("FOUT: dienst niet geregistreerd.");
    
    knipper_ledlampje(POORT_LEDLAMPJE_ROOD);

    return;
  }

  if (serverreactie[0] == 'D')
  {
    geef_reactie_weer_op_lcd(serverreactie.c_str()); // Dienst te kort.

    knipper_ledlampje(POORT_LEDLAMPJE_ROOD);

    return;
  }

  knipper_ledlampje(POORT_LEDLAMPJE_BLAUW);

  geef_reactie_weer_op_lcd(serverreactie.c_str());  // "<uur> h <minuut> min -> <00.00> EUR"

  return;
}


void geef_reactie_weer_op_lcd(const char* string)
{
  lcd_scherm.clear();
  
  lcd_scherm.print(string);
}


void knipper_ledlampje(const uint8_t poort_ledlampje)
{
  for (uint16_t helderheid = ONDERGRENS_LAMPHELDERHEID; helderheid < BOVENGRENS_LAMPHELDERHEID; helderheid++)
  {
    analogWrite(poort_ledlampje, helderheid);
    delay(VERVAGING_LAMP_MILISECONDEN);
  }

  for (uint16_t helderheid = BOVENGRENS_LAMPHELDERHEID; helderheid > ONDERGRENS_LAMPHELDERHEID; helderheid--)
  {
    analogWrite(poort_ledlampje, helderheid);
    delay(VERVAGING_LAMP_MILISECONDEN);
  }
}


void stuur_dienstgegevens_naar_python(const double starttijd_dienst, const double nu)
{
  Serial.print('$');
  Serial.print(tag_id);
  Serial.print(',');
  Serial.print(starttijd_dienst);
  Serial.print(',');
  Serial.print(nu);
  Serial.print("\n");
}


bool werknemer_bestaat_al()
{
  for (uint8_t i = 0; i < aantal_werknemers; i++)
  {
    if (werknemers[i].id == tag_id)
      return true;
  }

  return false;
}


void update_starttijd_werknemer(const double starttijd)
{  
  for (uint8_t i = 0; i < aantal_werknemers; i ++)
  {
    if (werknemers[i].id == tag_id)
    {
      werknemers[i].starttijd_dienst = starttijd;

      return;
    }
  }

  if (aantal_werknemers < MAXIMUMAANTAL_WERKNEMERS)
  {
    werknemers[aantal_werknemers] = {tag_id, starttijd};
    
    aantal_werknemers++;
  }
}


double geef_starttijd_werknemer()
{
  for (uint8_t i = 0; i < aantal_werknemers; i++)
  {
    if (werknemers[i].id == tag_id)
    {
      return werknemers[i].starttijd_dienst;
    }
  }

  return 0.0d;
}


void verwijder_werknemer()
{
  for (uint8_t i = 0; i < aantal_werknemers; i++)
  {
    if (werknemers[i].id == tag_id)
    {
      for (uint8_t j = i; j < aantal_werknemers - 1; j++)
        werknemers[j] = werknemers[j + 1];

      aantal_werknemers--;

      return;
    }
  }
}


void voer_taglezertoets_uit()
{
  if (!taglezer.PCD_PerformSelfTest())
    Serial.println("taglezer zelftest mislukt!");
  else
    Serial.println("taglezer zelftest geslaagd.");
}
