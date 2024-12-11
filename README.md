# **KLOKKER**

# Terugkoppeling coderecensie
<naam1, naam2>

### Probleem 1
De led-fading gebruikt een for-loop met delay — wat blokkerend werkt en de prestaties van de applicatie negatief beïnvloedt. De oplossing hiervoor zou het gebruik van niet-blokkerende timers met `millis()` in plaats van `delay()`. Deze aanpak maakt de led-fading efficiënter en voorkomt blokkering — maar maakt de code complexer.

# Screencast (videouitleg project)
_Let op_: het is niet gelukt de zesminutenlimiet te volgen (9 min 21 s). Hieraan ligt ten grondslag dat dit project in feite twee projecten is: een functionerend Arduino-inkloksysteem met een volledig functionerende FastAPI-server als backend. Ondanks het feit dat de video is versneld, was het onmogelijk iedere eigenschap voldoende aan het licht te brengen. In de opdrachtbeschrijving zelf staat immers: _"Always show all features: anything that’s not in the video does not exist."_ Gelieve begrip te hebben voor de omvang van dit project ten aanzien van de opgelegde tijdlimiet.

[![Watch the video](https://img.youtube.com/vi/RMWA1lSlNLs/0.jpg)](https://youtu.be/RMWA1lSlNLs?si=7sysB5itTmAV0ADO)

# Dankbetuiging

