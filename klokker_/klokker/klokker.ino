#include <SPI.h>
#include <String.h>
#include <MFRC522.h>
#include <NewPing.h>
#include <Arduino.h>
#include <LiquidCrystal_I2C.h>


const uint8_t POORT_LEDLAMPJE_ROOD = 2;
const uint8_t POORT_LEDLAMPJE_BLAUW = 4;
const uint8_t SS_POORT = 10;
const uint8_t RST_POORT = 9;
const uint8_t POORT_SONARTRIGGER = 9;
const uint8_t POORT_SONARECHO = 8;

const double TIJDSTEMPEL_START_ARDUINO = 1733842112.0000255;
const uint16_t BAUDVERBINDING = 9600;
const uint8_t RIJLENGTE_LCD_SCHERM = 16;
const uint8_t AANTAL_RIJEN_LCD_SCHERM = 2;
const uint8_t MAXIMALE_AFSTAND_SONAR_CM = 200;
const uint8_t MAXIMUMAANTAL_WERKNEMERS = 10;
const uint16_t ONDERGRENS_LAMPHELDERHEID = 0;
const uint8_t VERVAGING_LAMP_MILISECONDEN = 2;
const uint16_t BOVENGRENS_LAMPHELDERHEID = 255;
const uint16_t WACHTTIJD_OP_SERVER_MILISECONDEN = 550;
const double GRENSAFSTAND_AANRAKING_SONARSENSOR = 3.0d;
const uint16_t SLAAPTIJD_TUSSEN_SCANS_MILISECONDEN = 2000;
const uint16_t SECONDEN_DIENSTDATA_ZICHTBAAR_MILISECONDEN = 3000;


struct Werknemer
{
  String id;
  double starttijd_dienst;
};


//bool geef_tag_id();
bool aanraking_tag(const double afstand_cm);
void verwijder_werknemer();
void vul_array_werknemers();
bool werknemer_bestaat_al();
void verwerk_serverreactie();
inline void leeg_lcd_scherm();
//void voer_taglezertoets_uit();
double geef_starttijd_werknemer();
void geef_string_weer_op_lcd(const char* string);
void knipper_ledlampje(const uint8_t poort_ledlampje, const uint8_t op_rij);
void update_of_voeg_starttijd_werknemer_toe(const double startijd);
void stuur_dienstgegevens_naar_python(const double starttijd_dienst, const double nu);
inline double microseconden_naar_centimeter(const uint32_t microseconden);

//MFRC522 taglezer(SS_POORT, RST_POORT);
//MFRC522::MIFARE_Key sleutel;


NewPing sonarsensor(POORT_SONARTRIGGER, POORT_SONARECHO, MAXIMALE_AFSTAND_SONAR_CM);


LiquidCrystal_I2C lcd_scherm(0x27, RIJLENGTE_LCD_SCHERM, AANTAL_RIJEN_LCD_SCHERM);

byte readCard[4];
String tag_id = "M12093100202JKJDSK4KJSAEW";


Werknemer werknemers[MAXIMUMAANTAL_WERKNEMERS];
uint8_t aantal_werknemers = 0;


void setup()
{
  pinMode(POORT_LEDLAMPJE_BLAUW, OUTPUT);
  pinMode(POORT_LEDLAMPJE_ROOD, OUTPUT);

  Serial.begin(BAUDVERBINDING);

  SPI.begin();

  vul_array_werknemers();

  //taglezer.PCD_Init();

  lcd_scherm.init();
  lcd_scherm.backlight();
  lcd_scherm.setCursor(0, 0); // rij 0, karakter (vak) 0
}


void loop()
{
  // voer_taglezertoets_uit();
  double afstand_tot_sonar_cm = microseconden_naar_centimeter(sonarsensor.ping());
  
  if (aanraking_tag(afstand_tot_sonar_cm))
  {    
    double nu = geef_tijdstempel_nu();
 
    if (!werknemer_bestaat_al())
    {
      update_of_voeg_starttijd_werknemer_toe(nu);

      geef_string_weer_op_lcd("Ingeklokt!", 1);

      knipper_ledlampje(POORT_LEDLAMPJE_BLAUW);

      return;
    }
    else
    {
      double starttijd_dienst = geef_starttijd_werknemer();
      verwijder_werknemer();

      stuur_dienstgegevens_naar_python(starttijd_dienst, nu);

      delay(WACHTTIJD_OP_SERVER_MILISECONDEN);
      verwerk_serverreactie();
    }
  }

  delay(SLAAPTIJD_TUSSEN_SCANS_MILISECONDEN);
  leeg_lcd_scherm();

  return;
}


bool aanraking_tag(const double afstand_cm)
{
  if (afstand_cm < GRENSAFSTAND_AANRAKING_SONARSENSOR)
    return true;

  return false;
}


void verwerk_serverreactie()
{
  if (Serial.available() == 0)
  {
    geef_string_weer_op_lcd("Registratiefout!", 1);

    knipper_ledlampje(POORT_LEDLAMPJE_ROOD);

    return;
  }

  String serverreactie = Serial.readStringUntil('\n');
  
  if (serverreactie == "-1")
  {
    geef_string_weer_op_lcd("Registratiefout!", 1);
    
    knipper_ledlampje(POORT_LEDLAMPJE_ROOD);

    return;
  }

  String werktijd_van_server;
  String euros_verdiend;
  uint8_t i = 0;
  
  // reactieformaat server: {uren_gewerkt} h {overige_minuten} min@+{euros_verdiend} EUR
  while ((serverreactie[i] != '@') && (serverreactie[i] != '\0'))
  {
    werktijd_van_server += serverreactie[i];

    i++;
  }
  werktijd_van_server += " ->";

  if (serverreactie[i] == '@')
    i++;

  while (serverreactie[i] != '\0')
  {
    euros_verdiend += serverreactie[i];
    i++;
  }

  // "<uur> h <minuut> min -> +<00.00> EUR"
  geef_string_weer_op_lcd(werktijd_van_server.c_str(), 1);
  geef_string_weer_op_lcd(euros_verdiend.c_str(), 2);  

  knipper_ledlampje(POORT_LEDLAMPJE_BLAUW);

  delay(SECONDEN_DIENSTDATA_ZICHTBAAR_MILISECONDEN);
  leeg_lcd_scherm();

  return;
}


inline void leeg_lcd_scherm()
{
  lcd_scherm.clear();
}


void geef_string_weer_op_lcd(const char* string, const uint8_t op_rij)
{
  if (op_rij == 1)
    lcd_scherm.setCursor(0, 0);
  else if (op_rij == 2)
    lcd_scherm.setCursor(0, 1);

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


void vul_array_werknemers()
{
  for (uint8_t i = 0; i < MAXIMUMAANTAL_WERKNEMERS; i++)
    werknemers[i] = {"leeg", 0.0d};
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


void update_of_voeg_starttijd_werknemer_toe(const double starttijd)
{  
  for (uint8_t i = 0; i < aantal_werknemers; i ++)
  {
    if (werknemers[i].id == tag_id)
    {
      werknemers[i].starttijd_dienst = starttijd;

      return;
    }
  }

  for (uint8_t i = 0; i < MAXIMUMAANTAL_WERKNEMERS; i++)
  {
    if (werknemers[i].id == "leeg")
    {
      werknemers[aantal_werknemers] = {tag_id, starttijd};
    
      aantal_werknemers++;

      return;
    }
  }

  return;
}


double geef_starttijd_werknemer()
{
  for (uint8_t i = 0; i < aantal_werknemers; i++)
  {
    if (werknemers[i].id == tag_id)
      return werknemers[i].starttijd_dienst;
  }

  return 0.0d;
}


void verwijder_werknemer()
{
  for (uint8_t i = 0; i < aantal_werknemers; i++)
  {
    if (werknemers[i].id == tag_id)
    {
      werknemers[i].id = "leeg";
      werknemers[i].starttijd_dienst = 0.0d;

      aantal_werknemers--;

      return;
    }
  }
}


inline double microseconden_naar_centimeter(const uint32_t microseconden)
{
  return ((double)microseconden / 58.773);
}


double geef_tijdstempel_nu()
{
  uint32_t verstreken_tijd_sinds_start_arduino_miliseconden = millis();
  double nu = TIJDSTEMPEL_START_ARDUINO + (double)(verstreken_tijd_sinds_start_arduino_miliseconden / 1000l);

  return nu;
}


//void voer_taglezertoets_uit()
//{
//  if (!taglezer.PCD_PerformSelfTest())
//    Serial.println("taglezer zelftest mislukt!");
//  else
//    Serial.println("taglezer zelftest geslaagd.");
//}


//bool geef_tag_id()
//{
//  if (!taglezer.PICC_IsNewCardPresent())
//  {
//    Serial.println("Geen nieuwe kaart.\n");

//    return false;
//  }

//  if (!taglezer.PICC_ReadCardSerial())  // er is geen kaart/tag of deze is niet leesbaar
//  {
//    Serial.print("Fout bij lezen van de kaart.\n");

//    return true;
//  }

//  tag_id = "leeg";

//  for (uint8_t i = 0; i < 4; i++)
//    tag_id.concat(String(taglezer.uid.uidByte[i], HEX));

//  tag_id.toUpperCase();

//  taglezer.PICC_HaltA();

//  return true;
//}
