// Oppretter en ny dato som representerer dagens dato
let date = new Date(); // Nåværende dato og tid
let year = date.getFullYear(); // Henter året fra dagens dato
let month = date.getMonth(); // Henter måneden (0 = Januar, 11 = Desember)

// Henter HTML-elementer som skal brukes i kalenderen
const day = document.querySelector(".calendar-dates"); // Elementet der datoene i kalenderen skal vises
const currentdate = document.querySelector(".calendar-current-date"); // Elementet som viser måned og år (f.eks. "Desember 2024")
const prenexIcons = document.querySelectorAll(".calendar-navigation span"); // Navigasjonsknappene for å gå til forrige/neste måned

// En liste over månedene som brukes for å vise navnene på månedene
const months = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
];

// Funksjon som lager HTML for en enkelt dato i kalenderen
const createDateElement = (dayNumber, isActive = false, isInactive = false) => {
    // Hvis datoen er dagens dato, legger vi til klassen "active"
    const activeClass = isActive ? "active" : "";

    // Hvis datoen tilhører forrige eller neste måned, legger vi til klassen "inactive"
    const inactiveClass = isInactive ? "inactive" : "";

    // Returnerer HTML for datoen med de relevante klassene
    return `<li class="${activeClass} ${inactiveClass}">${dayNumber}</li>`;
};

// Funksjon som legger til datoene fra forrige måned som vises i kalenderen
const addPreviousMonthDays = (dayone, monthlastdate) => {
    let result = ""; // Starter med en tom string som skal inneholde datoene

    // For hver dag i forrige måned som må vises i starten av kalenderen:
    for (let i = dayone; i > 0; i--) { // Går bakover fra første ukedag (eks. Mandag = 1)
        result += createDateElement(monthlastdate - i + 1, false, true); // Legger til en inaktiv dato fra forrige måned
    }

    return result; // Returnerer alle datoene fra forrige måned som en HTML-string
};

// Funksjon som legger til datoene for aktuell måned
const addCurrentMonthDays = (lastdate, currentdate, month, year) => {
    let result = ""; // Starter med en tom string

    // Legger til hver dato i måneden
    for (let i = 1; i <= lastdate; i++) {
        // Sjekker om den aktuelle datoen er dagens dato
        const isToday = i === currentdate.getDate() && month === currentdate.getMonth() && year === currentdate.getFullYear();

        // Legger til datoen med "active"-klasse hvis det er dagens dato
        result += createDateElement(i, isToday);
    }

    return result; // Returnerer alle datoene for inneværende måned som en HTML-string
};

// Funksjon som legger til datoene for neste måned
const addNextMonthDays = (dayend) => {
    let result = ""; // Starter med en tom string

    // Legger til datoer fra neste måned for å fylle opp kalenderen
    for (let i = dayend; i < 6; i++) { // Går framover til lørdag (kolonne 6)
        result += createDateElement(i - dayend + 1, false, true); // Legger til inaktive datoer fra neste måned
    }

    return result; // Returnerer alle datoene fra neste måned som en HTML-string
};

// Hovedfunksjon som bygger og oppdaterer kalenderen
const manipulate = () => {
    const currentdateObj = new Date(); // Oppretter et nytt objekt for dagens dato
    const dayone = new Date(year, month, 1).getDay(); // Finner hvilken ukedag den første dagen i måneden er (0 = Søndag)
    const lastdate = new Date(year, month + 1, 0).getDate(); // Finner siste dato i måneden (f.eks. 30 for November)
    const dayend = new Date(year, month, lastdate).getDay(); // Finner hvilken ukedag den siste dagen i måneden er
    const monthlastdate = new Date(year, month, 0).getDate(); // Finner siste dato i forrige måned

    // Legger til datoer fra forrige måned, inneværende måned, og neste måned
    let lit = addPreviousMonthDays(dayone, monthlastdate); // Legger til inaktive datoer fra forrige måned
    lit += addCurrentMonthDays(lastdate, currentdateObj, month, year); // Legger til datoer for aktuell måned
    lit += addNextMonthDays(dayend); // Legger til inaktive datoer fra neste måned

    // Oppdaterer kalenderens visning i HTML
    currentdate.innerText = `${months[month]} ${year}`; // Viser aktuell måned og år i kalenderens overskrift
    day.innerHTML = lit; // Oppdaterer datoene som vises i kalenderen
};

// Funksjon som legger til klikk på hendelser for datoene i kalenderen
const attachDateListeners = () => {
    const dates = document.querySelectorAll(".calendar-dates li"); // Henter alle datoelementer
    dates.forEach(date => { // For hver dato:
        date.addEventListener("click", () => { // Legger til klikk-hendelse
            const selectedDate = date.innerText.trim(); // Henter den valgte datoen som tekst
            console.log("Dato klikket:", selectedDate); // Logger valgt dato i konsollen
            showEventPopup(selectedDate); // Viser pop-up med hendelser for den valgte datoen
        });
    });
};

// Kaller hovedfunksjonen for å bygge kalenderen
manipulate();
attachDateListeners(); // Legger til klikk på hendelser for datoene

// Navigasjonsknappene: Bytter mellom forrige og neste måned
prenexIcons.forEach(icon => {
    icon.addEventListener("click", () => {
        month = icon.id === "calendar-prev" ? month - 1 : month + 1; // Går til forrige eller neste måned

        if (month < 0 || month > 11) { // Hvis måneden går utenfor januar/desember:
            date = new Date(year, month, 1); // Oppdaterer datoobjektet til riktig år og måned
            year = date.getFullYear(); // Oppdaterer år
            month = date.getMonth(); // Oppdaterer måned
        }

        manipulate(); // Oppdaterer kalenderen med den nye måneden
        attachDateListeners(); // Legger til klikkbare hendelser igjen
    });
});



// Legger til en submit-hendelse for event-skjemaet
document.getElementById('event-form').addEventListener('submit', async function (e) {
    e.preventDefault(); // Hindrer standard skjemaoppførsel (GET)

    const eventName = document.getElementById('event-name').value; // Henter navn på hendelse
    const eventDate = document.getElementById('event-date').value; // Henter dato og tid for hendelse
    const eventPlace = document.getElementById('event-place').value; // Henter sted for hendelse

    if (!eventName || !eventDate || !eventPlace) { // Sjekker at nødvendige felter er fylt ut
        alert("Vennligst fyll ut alle nødvendige felter."); // Feilmelding hvis felter mangler
        return;
    }

    const formData = {
        dato: eventDate.split('T')[0],       // Dato
        klokkeslett: eventDate.split('T')[1],// Klokkeslett
        navn_prosjektet: eventName, // Navn på prosjektet
        sted: eventPlace,
        notification: document.getElementById('notification').value // Varsling
    };


    try {
        const response = await fetch('/add_event', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(formData), // Sender JSON-data
        });

        const result = await response.json();

        if (response.ok) {
            alert('Eventet ble lagret Yay!'); // Melding om at det klartes
            hideEventPopup(); // Skjuler pop-up
        } else {
            alert(result.error || 'Kunne ikke lagre eventen womp womp.'); // Feilmelding fra serveren
        }
    } catch (error) {
        console.error('Feil under lagring:', error); // Logger feil
        alert('En feil oppsto. Vennligst prøv igjen.'); // Viser generell feilmelding
    }
});

// Funksjon for å vise pop-up for å legge til hendelser
const showEventPopup = (selectedDate) => {
    const popup = document.getElementById("event-modal"); // Henter pop-up-elementet i HTML
    if (!popup) {
        console.error("Pop-up-elementet finnes ikke!");
        return;
    }

    // Henter input-feltet for dato og lager rikitg dato basert på valgt måned og år
    const eventDateInput = document.getElementById("event-date");
    const formattedDate = `${year}-${String(month + 1).padStart(2, "0")}-${String(selectedDate).padStart(2, "0")}T12:00`;

    popup.classList.remove("hidden"); // Viser pop-up
    eventDateInput.value = formattedDate; // Setter den valgte datoen i skjemaet
};


// Funksjon for å skjule pop-up
const hideEventPopup = () => {
    const popup = document.getElementById("event-modal");
    if (popup) popup.classList.add("hidden"); // Legger til "hidden"-klassen for å skjule pop-up
};

// Går til  "Legg til arrangement"-knappen til kalenderens side
document.getElementById('add-event-btn').addEventListener('click', () => {
    window.location.href = '/calenderen'; // Går til kalenderens URL
});




