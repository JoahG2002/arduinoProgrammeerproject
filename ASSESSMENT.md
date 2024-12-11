# ASSESSMENT.md

Dit document biedt een overzicht van de belangrijkste aspecten van mijn project, zowel op het gebied van functionaliteit als de ontwerpbeslissingen die ik heb genomen. Dit om ervoor te zorgen dat tijdens de beoordeling niets belangrijks over het hoofd wordt gezien.

---

## **Bekijk de video**
De video in de `README.md` geeft een uitgebreid overzicht van alle functionaliteiten en eigenschappen van mijn project. Hoewel de video iets langer is dan de richtlijn, bevat deze essentiële toelichtingen over ontwerpkeuzes en implementaties. Ik raad aan deze te bekijken voor een volledig begrip van het project. Het bekijken van de video is *_essentieel_* voor het begrip van Klokker. 

---

## Hoogtepunten van de Applicatie

### 1. **Inklokfunctionaliteit met sonarsensor**
- **Wat:** het inkloksysteem herkent medewerkers via een RFID-tag of hand en controleert op aanwezigheid met een sonarsensor. 
- **Waarom bijzonder:** dit voegt een extra verificatielaag toe door zowel fysieke aanwezigheid als de juiste identificatie te controleren.
- **Relevant:** zie `loop()` in `klokker.ino` voor de logica en implementatie.

### 2. **Automatische uurregistratie en berekeningen**
- **Wat:** het systeem berekent gewerkte uren, inclusief toeslagen voor feestdagen en avonduren, en registreert deze in een PostgreSQL-database.
- **Waarom bijzonder:** de automatische integratie met feestdagen en rollen is zeldzaam in eenvoudige Arduino-gebaseerde systemen.
- **Relevant:** zie de `calculate_working_hours()`- en `add_bonus()`-functies in `main.py`.

### 3. **Heldere Feedback met LCD-scherm**
- **Wat:** het lcd-scherm toont direct feedback zoals _"Ingeklokt!"_ en werktijden met verdiensten (`x uur -> y EUR`).
- **Waarom bijzonder:** de eenvoud en duidelijkheid maken het gebruiksvriendelijk voor werknemers.
- **Relevant:** zie de implementatie van `geef_string_weer_op_lcd()` in de Arduino-code.

---

## Grote Ontwerpbeslissingen

### 1. **Gebruik van PostgreSQL boven andere databases**
- **Waarom deze beslissing?** PostgreSQL biedt robuuste ondersteuning voor complexe queries en schaalbaarheid, wat essentieel was voor toekomstige uitbreidingen.
- **Wat was niet handig?** Aanvankelijk gebruikte ik SQLite, maar dit bleek onvoldoende voor multi-user access en ingewikkelde dataverwerking.
- **Waarom is PostgreSQL beter?** Met PostgreSQL kon ik eenvoudig functies implementeren zoals het berekenen van overuren en feestdagentoeslagen. Tot nu toe blijft dit een goede keuze.

### 2. **FastAPI voor de backend**
- **Waarom deze beslissing?** FastAPI biedt uitstekende ondersteuning voor asynchrone taken en is goed gedocumenteerd.
- **Wat was niet handig?** Mijn eerste idee was een eenvoudige Flask-app. Dit bleek lastig bij schaalbaarheid en integratie met asynchrone taken zoals dataverwerking.
- **Waarom is FastAPI beter?** FastAPI is sneller en flexibeler. Het helpt ook om te voldoen aan moderne API-standaarden zoals OpenAPI.

### 3. **Hand- en sonarcombinatie**
- **Waarom deze beslissing?** De rfid-522-taglezer is defect gebleken uit meerdere toetsen. De toevoeging van een sonarsensor voorkomt dit door fysieke aanwezigheid te eisen.
- **Wat was niet handig?** Het idee om alleen RFID te gebruiken maakte het systeem onbetrouwbaar.
- **Waarom is de nieuwe oplossing beter?** Dit systeem biedt een unieke combinatie van veiligheid en gebruiksgemak.

---

## Conclusie
Deze lijst benadrukt wat mijn project bijzonder maakt en legt uit waarom de ontwerpkeuzes de beste oplossing waren voor het probleem. De bovenstaande aspecten vormen de kern van mijn project en verdienen extra aandacht tijdens de beoordeling.
