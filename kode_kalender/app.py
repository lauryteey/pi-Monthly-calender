# Credits: Julian Magnussen Lund
from flask import Flask, jsonify, render_template, request, session
from datetime import datetime, timedelta
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash

# Oppretter en Flask-applikasjon
app = Flask(__name__, template_folder="./templates")
app.secret_key = 'Hei, secret key'  # En tilfeldig nøkkel som brukes for å kryptere sessions (brukerdata som lagres midlertidig).

# Kobler til en global MySQL-database
conn = mysql.connector.connect(
    host="localhost",         # Databasens adresse (lokal maskin)
    user="calender_user",     # Brukernavnet til databasen.
    password="123",           # Passordet til databasen.
    database="calender"       # Navnet på databasen som brukes.
)

# Oppretter en global cursor for å kjøre SQL-spørringer
cursor = conn.cursor(dictionary=True)  # Konfigurerer til å returnere resultater som dictionaries (nøkkel-verdi-par).

# Rute for innlogging
@app.route('/login', methods=['POST'])
def login():
    try:
        # Henter data som sendes i forespørselen (JSON-format).
        data = request.get_json()

        # Sjekker om nødvendige felter finnes i forespørselen.
        if 'e_post' not in data or 'passord' not in data:
            return jsonify({"error": "E-post og passord er påkrevd"}), 400

        e_post = data['e_post']  # Leser e-post fra forespørselen.
        passord = data['passord']  # Leser passord fra forespørselen.

        # Sjekker om e-posten finnes i databasen.
        query = "SELECT brukerID, passord FROM bruker WHERE e_post = %s"
        cursor.execute(query, (e_post,))
        user = cursor.fetchone()  # Henter resultatet fra databasen.

        if user:
            # Sjekker om passordet stemmer ved hjelp av hashing.
            if check_password_hash(user['passord'], passord):
                session['brukerID'] = user['brukerID']  # Lagre brukerID i session (midlertidig lagring).
                return jsonify({"message": "Klarte å logge inn YAY!", "redirect": "/calenderen"}), 200
            else:
                return jsonify({"error": "Feil passord."}), 401
        else:
            return jsonify({"error": "Bruker ble ikke funnet."}), 404
    except mysql.connector.Error as e:
        # Feil relatert til databasen er her.
        print(f"Feil i databasen under login: {e}")
        return jsonify({"error": "En feil i databasen oppsto"}), 500
    except Exception as e:
        # Andre uventede feil håndteres her.
        print(f"Uforventet feil under login: {e}")
        return jsonify({"error": "Det skjedde en uventet feil"}), 500

# Rute for å legge til et arrangement
@app.route('/add_event', methods=['POST'])
def add_event():
    try:
        # Sjekker om brukeren er logget inn.
        if 'brukerID' not in session:
            return jsonify({'error': 'Bruker er ikke logget inn'}), 401

        # Henter data fra forespørselen (JSON-format).
        data = request.json
        if not data:
            return jsonify({'error': 'Ingen data mottatt'}), 400

        brukerID = session['brukerID']  # Henter brukerID fra session.

        # SQL-spørring for å legge til arrangementet i databasen.
        query = """
            INSERT INTO events_ny (dato, klokkeslett, navn_prosjektet, sted, notification, brukerID)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        values = (
            data['dato'],               
            data['klokkeslett'],        
            data['navn_prosjektet'],    
            data['sted'],               
            data['notification'],       
            brukerID                    
        )
        cursor.execute(query, values)
        conn.commit()  # Lagrer endringene i databasen YIPIIE.

        return jsonify({"message": "Eventet er lagret!"}), 200
    except Exception as e:
        print(f"Error adding event: {e}")
        return jsonify({'error': 'Feil under lagring av event'}), 500

# Rute for å hente brukerens arrangementer.
@app.route('/get_events', methods=['GET'])
def get_events():
    try:
        # Sjekker om brukeren er logget inn.
        if 'brukerID' not in session:
            return jsonify({'error': 'Not logged in'}), 401
        
        brukerID = session['brukerID']  # Henter brukerID fra session.
        query = "SELECT dato, klokkeslett, navn_prosjektet, sted, notification FROM events_ny WHERE brukerID = %s"
        cursor.execute(query, (brukerID,))
        events = cursor.fetchall()  # Henter alle arrangementer for brukeren.

        # Konverterer data til lesbart format hvis nødvendig.
        for event in events:
            if isinstance(event.get('dato'), datetime):  # Konverterer dato til streng.
                event['dato'] = event['dato'].strftime('%Y-%m-%d')
            if isinstance(event.get('klokkeslett'), (timedelta, datetime)):  # Konverterer klokkeslett.
                event['klokkeslett'] = str(event['klokkeslett'])
        
        return jsonify(events), 200
    except Exception as e: #kjedelig feilhåndetring, hvis databasen klarer seg ikke 
        print(f"Error fetching events: {e}")
        return jsonify({'error': 'Feil i databasen'}), 500

# Rute for å opprette en ny bruker
@app.route('/create_user', methods=['POST'])
def create_user():
    try:
        # Henter data som sendes i forespørselen (JSON-format)
        data = request.get_json()

        # Sjekker om alle nødvendige felt er med i forespørselen
        if not all(key in data for key in ('e_post', 'passord', 'fornavn', 'etternavn')):
            return jsonify({"error": "E-post, passord, fornavn og etternavn er påkrevd"}), 400

        e_post = data['e_post']  # Henter e-post fra forespørselen
        passord = data['passord']  # Henter passord fra forespørselen
        fornavn = data['fornavn']  # Henter fornavn fra forespørselen
        etternavn = data['etternavn']  # Henter etternavn fra forespørselen

        # Sjekker om e-posten allerede finnes i databasen
        query = "SELECT e_post FROM bruker WHERE e_post = %s"
        cursor.execute(query, (e_post,))
        if cursor.fetchone():
            return jsonify({"error": "E-posten er allerede registrert"}), 409

        # Genererer et hashed passord for sikker lagring
        hashed_passord = generate_password_hash(passord)

        # SQL-spørring for å legge til ny bruker
        query = """
            INSERT INTO bruker (e_post, passord, fornavn, etternavn)
            VALUES (%s, %s, %s, %s)
        """
        values = (e_post, hashed_passord, fornavn, etternavn)
        cursor.execute(query, values)
        conn.commit()  # Lagrer endringene i databasen

        return jsonify({"message": "Brukeren ble opprettet!"}), 201
    except mysql.connector.Error as e:
        # Håndterer databasefeil
        print(f"Databasefeil under oppretting av bruker: {e}")
        return jsonify({"error": "En feil oppsto med databasen"}), 500
    except Exception as e:
        # Håndterer andre uventede feil
        print(f"Uventet feil under oppretting av bruker: {e}")
        return jsonify({"error": "Det oppsto en uventet feil"}), 500


@app.route('/sign_up')
def sign_up():
    return render_template('signUp.html')  



@app.route('/show_events')
def show_events():
    if 'brukerID' not in session:  #Gjør sikker at brukeren er logget in. 
        return jsonify({'error': 'Bruker er ikke logget inn'}), 401
    print("Rendering ShowEvents.html")
    return render_template('ShowEvents.html')  # Viser show events side.



# Default route (Hjemmeside)
@app.route('/')
def home():
    # Viser innloggingssiden.
    return render_template('logIn.html')


# Kalenderens hovedside
@app.route('/calenderen')
def calenderen():
    # Sjekker om brukeren er logget inn.
    if 'brukerID' not in session:
        return jsonify({'error': 'Bruker er ikke logget inn'}), 401
    # Viser kalendersiden hvis brukeren er logget inn.
    return render_template('Index.html')


# Starter Flask-applikasjonen
if __name__ == '__main__':
    try:
        app.run(debug=True)  # Kjører appen i debug-modus for utvikling.
    except Exception as e:
        # Logger feil som oppstår når appen starter.
        print(f"Feilet når starting Flask app: {e}")
 
 
        
#host='0.0.0.0' - Usikker måte å hoste nettside (anbefales og ikke gjøre)
