# **KLOKKER: de simpele oplossing voor arbeidsuurregistratie in het mkb**

Midden- en kleinbedrijven (mkb'ers) vormen de ruggengraat van de Nederlandse economie. Toch kampen veel van deze bedrijven — zoals viskramen, fietsenmakers en dönerzaken — met een gemeenschappelijk probleem: het nauwkeurig bijhouden van arbeidsuren. Traditionele methoden zoals papieren notities of tools als Excel en Google Sheets blijken vaak foutgevoelig en kunnen zelfs misbruikt worden. Met Klokker is dat probleem verleden tijd.

### Wat is Klokker?
Klokker is een innovatief, gebruiksvriendelijk inkloksysteem dat speciaal is ontwikkeld voor mkb-bedrijven. Het systeem combineert een compact apparaatje met moderne technologie. Het metalen of plastic kastje bevat een ledlampje, een tagplatform en een lcd-scherm. Hiermee kunnen werknemers eenvoudig in- en uitklokken, terwijl het scherm duidelijke feedback geeft, zoals:
`5 uur 23 min -> €84,23` verdiend.

Daarnaast communiceert Klokker moeiteloos met een PostgreSQL-database via een server, zodat werkgevers altijd toegang hebben tot real-time data over arbeidsuren en loonkosten.

### Voor wie is Klokker geschikt?
Klokker is ontworpen met het mkb in gedachten. Het is ideaal voor bedrijven met een gevarieerd personeelsbestand, zoals studenten met een bijbaan, horecamedewerkers en winkelpersoneel. Voor werkgevers biedt Klokker niet alleen overzicht, maar ook vertrouwen in de nauwkeurigheid van de gegevens.

### Waarom kiezen voor Klokker?
Klokker onderscheidt zich van andere inkloksystemen door zijn eenvoud en slimme functies. Het systeem biedt:

- Directe feedback: het lcd-scherm laat werknemers meteen zien of hun uren zijn geregistreerd.
- Automatische aanpassingen: het systeem houdt rekening met feestdagen, toeslagen voor avonduren en het type functie van de werknemer (bijvoorbeeld manager of schoonmaker).
Betrouwbare gegevensopslag: alle data wordt veilig opgeslagen in een PostgreSQL-database, toegankelijk voor werkgevers wanneer nodig.

Met Klokker kies je voor transparantie, efficiëntie en eenvoud. De arbeidsurenregistratie was nog nooit zo makkelijk!

![Alternative Text](inlokkerProgrammeerprojectArduino.png)
![Alternative Text](PXL_20241209_155214328.jpg)
![Alternative Text](ScreenshotKlokker.png)
![Alternative Text](fastApiRouters.png)

# Screencast (videouitleg project)
_Let op_: het is niet gelukt de zesminutenlimiet te volgen (9 min 21 s). Hieraan ligt ten grondslag dat dit project in feite twee projecten is: een functionerend Arduino-inkloksysteem met een volledig functionerende FastAPI-server als backend. Ondanks het feit dat de video is versneld, was het onmogelijk iedere eigenschap voldoende aan het licht te brengen. In de opdrachtbeschrijving zelf staat immers: _"Always show all features: anything that’s not in the video does not exist."_ Gelieve begrip te hebben voor de omvang van dit project ten aanzien van de opgelegde tijdlimiet.

[![Watch the video](https://img.youtube.com/vi/RMWA1lSlNLs/0.jpg)](https://youtu.be/RMWA1lSlNLs?si=7sysB5itTmAV0ADO)

# Installatiehandleiding
### 1. Vereisten
- Python 3.10+ (te downloaden via python.org);
- PostgreSQL 13+ (te downloaden via postgresql.org);
- Arduino IDE (te downloaden via arduino.cc);
- Git (voor het klonen van de repository);
- een Arduino-compatibele microcontroller met de juiste componenten (zoals een RFID-lezer, sonar (Ultrasonic Sensor HC-SR04) en lcd-scherm (I2C LCD 16x2).

Tenslotte: `pip install -r requirements.txt`.

# Dankbetuiging
- MFRC522 Library: De RFID-lezer code gebruikt de MFRC522 Arduino library, copyright 2014-2021 by Miguel Balboa. Deze is beschikbaar onder de MIT-licentie.
- LiquidCrystal_I2C Library: De LCD-scherm code maakt gebruik van de LiquidCrystal_I2C library, copyright by John Rickman. Deze is beschikbaar onder de GNU General Public License v2.0.
- NewPing Library: De code voor de ultrasone sensor maakt gebruik van de NewPing library, copyright by Tim Eckel. Deze is beschikbaar onder de GNU General Public License v3.0.
