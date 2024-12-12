# Credits: Julian Magnussen Lund
from flask import Flask, jsonify, render_template, request, session
from datetime import datetime, timedelta
import mysql.connector

app = Flask(__name__)
app.secret_key = 'Hei, secret key'  # En tilfeldig nøkkel som brukes til å kryptere informasjonskapslene dine. Nødvendig for session management.

# Kobling til global database
conn = mysql.connector.connect(
    host="88.95.146.186",         
    user="calender_user",     
    password="123",           
    database="calender"       
)

# Global cursor for å utføre spørringer i databasen
cursor = conn.cursor(dictionary=True)  # Returnerer rader som dictionaries i stedet for tuples.

# Login route
@app.route('/login', methods=['POST'])
def login():
    try:
        # Henter JSON-data fra forespørselen.
        data = request.get_json()

        # Sjekker om e-post og passord er oppgitt.
        if 'e_post' not in data or 'passord' not in data:
            return jsonify({"error": "E-post og passord er påkrevd"}), 400

        e_post = data['e_post']  # Henter e-post fra data.
        passord = data['passord']  # Henter passord fra data.

        # Spør databasen etter bruker med gitt e-post.
        query = "SELECT brukerID, passord FROM bruker WHERE e_post = %s"
        cursor.execute(query, (e_post,))
        user = cursor.fetchone()  # Henter første rad fra resultatet.

        if user:
            # Sjekker om passordet matcher.
            if user['passord'] == passord:
                session['brukerID'] = user['brukerID']  # Lagre brukerID i session.
                return jsonify({"message": "Klarte å logge inn YAY!", "redirect": "/calenderen"}), 200
            else:
                return jsonify({"error": "Feil passord."}), 401
        else:
            return jsonify({"error": "Bruker ble ikke funnet."}), 404
    except mysql.connector.Error as e:
        # Logger databasefeil.
        print(f"Feil i databasen under login: {e}")
        return jsonify({"error": "En feil i databasen oppsto"}), 500
    except Exception as e:
        # Logger andre uventede feil.
        print(f"Uforventet feil under login: {e}")
        return jsonify({"error": "Det skjedde en uventet feil"}), 500
    

# Add event route
@app.route('/add_event', methods=['POST'])
def add_event():
    try:
        if 'brukerID' not in session:
            return jsonify({'error': 'Bruker er ikke logget inn'}), 401

        data = request.json
        if not data:
            return jsonify({'error': 'Ingen data mottatt'}), 400

        brukerID = session['brukerID']

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
        conn.commit()

        return jsonify({"message": "Eventet er lagret!"}), 200
    except Exception as e:
        print(f"Error adding event: {e}")
        return jsonify({'error': 'Feil under lagring av event'}), 500




@app.route('/get_events', methods=['GET'])
def get_events():
    try:
        if 'brukerID' not in session:
            return jsonify({'error': 'Not logged in'}), 401
        
        brukerID = session['brukerID']
        query = "SELECT dato, klokkeslett, navn_prosjektet, sted, notification FROM events_ny WHERE brukerID = %s"
        cursor.execute(query, (brukerID,))
        events = cursor.fetchall()
        
        print("Query result:", events)  # Debug print

        # Convert non-serializable fields
        for event in events:
            if isinstance(event.get('dato'), datetime):  # Convert 'dato' to string if it's a datetime
                event['dato'] = event['dato'].strftime('%Y-%m-%d')
            if isinstance(event.get('klokkeslett'), (timedelta, datetime)):  # Handle time-related fields
                event['klokkeslett'] = str(event['klokkeslett'])
        
        return jsonify(events), 200
    except Exception as e:
        print(f"Error fetching events: {e}")
        return jsonify({'error': 'Feil i databasen'}), 500



# Flask route for creating a new user
@app.route('/create_user', methods=['POST'])
def create_user():
    try:
        # Hent data fra forespørselen
        data = request.json

        # Valider påkrevde felter
        required_fields = ['fornavn', 'etternavn', 'e_post', 'passord']
        for field in required_fields:
            if field not in data or not data[field].strip():
                return jsonify({"error": f"Feltet '{field}' er påkrevd."}), 400

        # SQL-spørring for å legge til en ny bruker
        query = """
            INSERT INTO bruker (e_post, passord, fornavn, etternavn)
            VALUES (%s, %s, %s, %s)
        """
        values = (
            data['e_post'],      # E-post
            data['passord'],     # Passord
            data['fornavn'],     # Fornavn
            data['etternavn']    # Etternavn
        )

        # Utfør spørringen
        cursor.execute(query, values)
        conn.commit()  # Lagre endringene i databasen

        # Returner suksessmelding
        return jsonify({"message": "Brukeren ble opprettet!"}), 201

    except mysql.connector.IntegrityError as e:
        # Håndter databasefeil (f.eks. duplisert e-post)
        print(f"Feil i databasen under opprettelse av bruker: {e}")
        return jsonify({"error": "Denne e-postadressen er allerede registrert."}), 409

    except mysql.connector.Error as e:
        # Logger databasefeil
        print(f"Feil i databasen under opprettelse av bruker: {e}")
        return jsonify({"error": "En databasefeil oppsto."}), 500

    except Exception as e:
        # Håndter uventede feil
        print(f"Uforventet feil under opprettelse av bruker: {e}")
        return jsonify({"error": "En uventet feil oppsto."}), 500



@app.route('/sign_up')
def sign_up():
    return render_template('SignUp.html')  # Ensure this is your sign-up HTML file



@app.route('/show_events')
def show_events():
    if 'brukerID' not in session:  # Ensure the user is logged in
        return jsonify({'error': 'Bruker er ikke logget inn'}), 401
    print("Rendering ShowEvents.html")
    return render_template('ShowEvents.html')  # Render the Show Events page



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
    return render_template('index.html')


# Starter Flask-applikasjonen
if __name__ == '__main__':
    try:
        app.run(debug=True)  # Kjører appen i debug-modus for utvikling.
    except Exception as e:
        # Logger feil som oppstår når appen starter.
        print(f"Feilet når starting Flask app: {e}")
        
#host='0.0.0.0'