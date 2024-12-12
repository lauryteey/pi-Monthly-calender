# **Brukerveiledning for Kalenderapplikasjon (Beta version)** 

## **Introduksjon**
Denne brukerveiledningen gjelder for **beta-versjonen** av kalenderapplikasjonen. Applikasjonen er under utvikling, og nye funksjoner vil bli lagt til i fremtidige versjoner. I denne versjonen kan brukeren:

- Opprette brukerkontoer.
- Opprette hendelser med detaljer som dato, tid, beskrivelse og sted.
- Vise en oversikt over alle eventer som brukeren har opprettet.

--- 
Hensikten med applikasjonen er å gi brukeren en enkel måte å organisere sitt daglige liv og arbeidsoppgaver. Alt lagres trygt i en MariaDB/MySQL-database, slik at informasjonen til brukeren er tilgjengelig når brukeren trenger det. Enten det brukes til personlige oppgaver eller profesjonelle arrangementer, er ideen med denne kalenderapplikasjonen laget for å være fleksibel og intuitiv.

---

## **Hva trenger du?**

For å bruke applikasjonen, må du ha følgende:
- Tilgang til en MariaDB/MySQL-database med riktig oppsett.

### **Installasjon**
1. **Last ned applikasjonen:**
   - Applikasjonen ligger på GitHub, klon den til datamaskinen din med:

     ```bash
     git clone https://github.com/lauryteey/Monthly-calender
     ```
   - Eller last ned ZIP-filen og pakk den ut.

### **Installer og sett opp virtuelt miljø**

1. **Opprett et virtuelt miljø:**
   Gå til prosjektmappen og kjør kommandoen:

   - På Windows/macOS/Linux: 

     ```bash
     python -m venv myenv
     ```

2. **Aktiver det virtuelle miljøet:**
   - På Windows:

     ```bash
     .\myenv\Scripts\activate
     ```

   - På macOS/Linux:
     ```bash
     source myenv/bin/activate
     ```

---

### **Installer nødvendige avhengigheter**

- Sørg for at du har en fil kalt `requirements.txt` i prosjektmappen.
- Installer avhengigheter med kommandoen:

   ```bash
   pip install -r requirements.txt
   ````
- Hvis filen requirements.txt mangler, kan du installere de viktigste manuelt:

````bash
pip install flask mysql-connector
pip install Flask
````
   - Deretter gå til mappen der filene ligger.
   - Start applikasjonen:

     ```bash
     python app.py
     ```
   - Åpne nettleseren og gå til ip adressen du får fra flask med ````CTRL + click````



## **Hvordan bruke applikasjonen**

### **1. Logge inn eller registrere deg inn**
For å teste applikasjonen, kan du oprette din eget bruker og deretter logge inn.

- Gå til innloggingssiden og legg til nødvendige informajson, for eksempel: 
- **E-post:** `test_user@gmail.com`
- **Passord:** `123`
- Klikk på **Logg inn**.
- Hvis du har skrevet riktig informasjon, vil du bli sendt til kalendersiden. Hvis ikke, vil en feilmelding vises.

---
### **3. Vise kalenderen**
- Etter at du logger inn, vil du se kalenderen.
- Du kan se både forrige og fremtidige datoer.
- Du kan se eventene du lager ved å klikke på **Vise eventer**

---

### **2. Opprette en ny hendelse**
1. Klikk på datoen du vil legge en event til.
2. Fyll ut skjemaet:

   - **Dato og tid**: Velg dato og tid for hendelsen.
   - **Navn på hendelsen**: Beskriv hva hendelsen handler om.
   - **Sted**: Skriv inn hvor hendelsen finner sted.
   - **Påminnelse**: Velg når du vil ha en påminnelse før hendelsen.

3. Klikk **Lagre** for å lagre hendelsen.

---

## **Funksjoner forklart**

### **a. Logg inn og registrer deg**
- lar brukeren lage sitt eget bruker 
- Bruker e-post og passord for å bekrefte hvem brukeren er og gir deg tilgang til calenderen.
- Hvis brukeren finnes i databasen og passordet er riktig, får du tilgang til kalenderen.

### **b. Opprette hendelser**
- Lagrer informasjon om hendelser i databasen.
- Brukes for å holde oversikt over hva som skjer og når.

### **c. Kalender**
- Gir deg tilgang til å navigere mellom datoer.
- Viser dagens dato, oppdateres daglig. 

### **d. Vise eventer**
- Viser en liste over eventer som brukeren oppretter 
- Lar deg legge til flere eventer 

### **e. Påminnelser**
- **(Kommende funksjon)**: Sender e-postpåminnelser 1 time eller 10 minutter før hendelsen starter.


---

## **Kommende funksjoner**
- **Påminnelser:** E-postpåminnelser vil bli sendt 1 time eller 10 minutter før en hendelse.
- **Redigere og slette eventer:** Brukere vil kunne oppdatere eller fjerne eksisterende hendelser.
- **Logge seg ut:** Brukere kan logge seg in og ut når som helst.

---

## **Vanlige problemer og løsninger**

### Problem: Får ikke logget inn.
- **Løsning**: Sørg for at e-postadressen og passordet er riktig. Hvis problemet vedvarer, kontakt administrator.

### Problem: Hendelser lagres ikke.
- **Løsning**: Sjekk at databasen er riktig konfigurert og aktiv.

### Problem: Feil under tilkobling til databasen.
- **Løsning**: Forsikre deg om at MariaDB/MySQL-serveren kjører, og at brukerrettighetene er satt opp korrekt.

---

## **Kontaktinformasjon**
Hvis du trenger hjelp eller du vil gi meg din mening om aplikasjonen, vennligst kontakt meg på **laurafabiola.s.a@gmail.com**.

