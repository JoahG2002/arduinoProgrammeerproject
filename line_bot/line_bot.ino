

const uint8_t LINKERSENSOR = A2;
const uint8_t RECHTERSENSOR = A3;

const uint8_t MOTOR_RECHTS_PWM = 5;
const uint8_t MOTOR_LINKS_PWM = 6;
const uint8_t RECHTSMOTOR_RICHTING = 4;
const uint8_t LINKSMOTOR_RICHTING = 7;
	
const uint8_t KRUISSNELHEID = 200;
const uint8_t DRAAISNELHEID = 150;

const uint8_t BAUDVERBINDING = 9600;
const uint8_t SLAAPTIJD_TUSSEN_SENORLEZING_MILISECONDEN = 10;


void ga_rechtdoor();
void ga_naar_rechts();
void ga_naar_links();
void stop_motoren();
void print_sensorstati(const uint8_t status_linkersensor, const uint8_t status_rechtersensor);


void setup()
{
  pinMode(LINKERSENSOR, INPUT);
  pinMode(RECHTERSENSOR, INPUT);
  
  pinMode(MOTOR_RECHTS_PWM, OUTPUT);
  pinMode(MOTOR_LINKS_PWM, OUTPUT);
  pinMode(RECHTSMOTOR_RICHTING, OUTPUT);
  pinMode(LINKSMOTOR_RICHTING, OUTPUT);
  
  Serial.begin(BAUDVERBINDING);
}


void loop()
{
  uint8_t status_linkersensor = digitalRead(LINKERSENSOR);
  uint8_t status_rechtersensor = digitalRead(RECHTERSENSOR);
  
  print_sensorstati(status_linkersensor, status_rechtersensor);
  
  if ((status_linkersensor == LOW) && (status_rechtersensor == LOW))
    ga_rechtdoor();
  else if ((status_linkersensor == HIGH) && (status_rechtersensor == LOW))
    ga_naar_rechts();
  else if ((status_linkersensor == LOW) && (status_rechtersensor == HIGH))
    ga_naar_links();
  else
    stop_motoren();
  
  delay(SLAAPTIJD_TUSSEN_SENORLEZING_MILISECONDEN);
}


void print_sensorstati(const uint8_t status_linkersensor, const uint8_t status_rechtersensor)
{
  Serial.print("Links: ");
  Serial.print(status_linkersensor);

  Serial.print("; rechts: ");
  Serial.print(status_rechtersensor);
  Serial.print("\n-------------------------------------------------------------------\n");
}


void ga_rechtdoor()
{
  digitalWrite(RECHTSMOTOR_RICHTING, HIGH);
  digitalWrite(LINKSMOTOR_RICHTING, LOW);
  
  analogWrite(MOTOR_RECHTS_PWM, KRUISSNELHEID);
  analogWrite(MOTOR_LINKS_PWM, KRUISSNELHEID);
}


void ga_naar_rechts()
{
  digitalWrite(RECHTSMOTOR_RICHTING, LOW);
  digitalWrite(LINKSMOTOR_RICHTING, LOW);
  
  analogWrite(MOTOR_RECHTS_PWM, DRAAISNELHEID);
  analogWrite(MOTOR_LINKS_PWM, KRUISSNELHEID);
}


void ga_naar_links()
{
  digitalWrite(RECHTSMOTOR_RICHTING, HIGH);
  digitalWrite(LINKSMOTOR_RICHTING, HIGH);
  
  analogWrite(MOTOR_RECHTS_PWM, KRUISSNELHEID);
  analogWrite(MOTOR_LINKS_PWM, DRAAISNELHEID);
}


void stop_motoren()
{
  analogWrite(MOTOR_RECHTS_PWM, 0);
  analogWrite(MOTOR_LINKS_PWM, 0);
}
