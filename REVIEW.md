
# Terugkoppeling coderecensie
<naam1, naam2>

### Probleem 1
De led-fading gebruikt een for-loop met delay — wat blokkerend werkt en de prestaties van de applicatie negatief beïnvloedt. De oplossing hiervoor zou het gebruik van niet-blokkerende timers met `millis()` in plaats van `delay()`. Deze aanpak maakt de led-fading efficiënter en voorkomt blokkering — maar maakt de code complexer.

### Probleem 2
Overmatig gebruik: globale variabelen zoals `tag_id` en `werknemers` verhogen de kans op onverwachte bijwerkingen en maken debugging moeilijker. Het gebruik van lokale variabelen en parameters kan de scope van deze gegeven eventueel beperken. Het is alleen zo dat het gebruik van globale variable Arduino-eigen is: `.ino`-bestanden staan geen `main`-functie toe — louter de ingangfuncties `setup` en `loop`. Het creëren van variable die meerdere lussen mee moeten gaan, omdat op hen gebouwd moet worden, is daarom eigenlijk alleen mogelijk met deze globale variabelen. Om dit globalevariableprobleem op te lossen, zou het hele programma herschreven moeten worden in C++ met de `avr/io.h`.

### Probleem 3
Het gebruik van`String.h`: `Strings` gebruiken veel meer werkgeheugen dan `const char*`. Juist op Arduino's is de hoeveelheid werkgeheugen beperkt. Het zou daarom verstandiger zijn om de `Strings` te vervangen. Dit voorstel lijkt deugzaam, maar ziet de variabele aard van de uitvoer van het Python-programma over het hoofd. Dit programma geeft strings terug van diverse lengte en het is onmogelijk voor de Arduino om te weten hoe lang deze zullen zijn. `String.h` wordt om deze reden dus terecht gebruikt. Zou `const char*` of `char string[]` worden gebruikt, dan zouden deze moeten beschikken over een vrij grote buffer voor de onbekende hoeveelheid karakters — wat in principe weer neerkomt op een `String`.  

### Probleem 4
De gehardcode limiet werknemers (`Werknemer werknemers[10];`): het aantal werknemers dat zou kunnen inklokken is hierdoor beperkt tot de waarde die staat gehardcoded in de broncode (het `.ino`-bestand). Hoewel deze feedback hout snijdt, is het niet zou makkelijk als het lijkt om een alternatief te implementeren: tijdens de productie van het product is reeds gepoogd C++'s `std::vector` te gebruiken, maar Arduino ondersteunt deze headerbestanden niet. Het is ook om deze reden dat Arduino `String.h` gebruikt in plaats van C++'s _'echte'_ `<string.h>`. Wederom zou het programmeren herschreven moeten worden in C++ in plaats van de huidige Arduino-abractietaal.
