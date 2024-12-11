# **KLOKKER**

# Terugkoppeling coderecensie
<naam1, naam2>

### Probleem 1
De led-fading gebruikt een for-loop met delay — wat blokkerend werkt en de prestaties van de applicatie negatief beïnvloedt. De oplossing hiervoor zou het gebruik van niet-blokkerende timers met `millis()` in plaats van `delay()`. Deze aanpak maakt de led-fading efficiënter en voorkomt blokkering — maar maakt de code complexer.

### Probleem 1
Overmatig gebruik: globale variabelen zoals `tag_id` en `werknemers` verhogen de kans op onverwachte bijwerkingen en maken debugging moeilijker. Het gebruik van lokale variabelen en parameters kan de scope van deze gegeven eventueel beperken. Het is alleen zo dat het gebruik van globale variable Arduino-eigen is: `.ino`-bestanden staan geen `main`-functie toe — louter de ingangfuncties `setup` en `loop`. Het creëren van variable die meerdere lussen mee moeten gaan, omdat op hen gebouwd moet worden, is daarom eigenlijk alleen mogelijk met deze globale variabelen. Om dit globalevariableprobleem op te lossen, zou het hele programma herschreven moeten worden in C++ met de `avr/io.h`.

# Screencast (videouitleg project)
_Let op_: het is niet gelukt de zesminutenlimiet te volgen (9 min 21 s). Hieraan ligt ten grondslag dat dit project in feite twee projecten is: een functionerend Arduino-inkloksysteem met een volledig functionerende FastAPI-server als backend. Ondanks het feit dat de video is versneld, was het onmogelijk iedere eigenschap voldoende aan het licht te brengen. In de opdrachtbeschrijving zelf staat immers: _"Always show all features: anything that’s not in the video does not exist."_ Gelieve begrip te hebben voor de omvang van dit project ten aanzien van de opgelegde tijdlimiet.

[![Watch the video](https://img.youtube.com/vi/RMWA1lSlNLs/0.jpg)](https://youtu.be/RMWA1lSlNLs?si=7sysB5itTmAV0ADO)

# Dankbetuiging

