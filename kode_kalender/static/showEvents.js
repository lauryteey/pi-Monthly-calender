// Kjører scripten når DOM er ferdig lastet
document.addEventListener("DOMContentLoaded", function () {
    // Validerer at elementer som kreves er tilgjengelige
    if (validateElement()) {
        fetchEvents(); // Henter eventer hvis validering er ok
    }

    // Legger til event på "Legg til event"-knappen for å gå til kalenderen
    const addEventBtn = document.getElementById("add-event-btn");
    if (addEventBtn) {
        addEventBtn.addEventListener("click", () => {
            window.location.href = "/calenderen"; // Går til kalenderens URL
        });
    }
});

// Validerer at nødvendige elementer finnes i DOM
const validateElement = () => {
    const eventsList = document.getElementById("event-list");
    if (!eventsList) {
        console.error("Element med id 'event-list' ble ikke funnet!");
        return false;
    }
    return true;
};

// Funksjon for å hente eventer fra serveren og vise dem i HTML
async function fetchEvents() {
    try {
        // Sender forespørsel til serveren for å hente eventer
        const response = await fetch("/get_events");
        if (!response.ok) {
            throw new Error(`Feil ved henting av eventer: HTTP ${response.status}`); // Kaster en spesifikk feil hvis forespørselen mislykkes
        }

        // Konverterer JSON-respons til et JavaScript-objekt
        const events = await response.json();

        // Henter HTML-elementet der eventer skal vises
        const eventsList = document.getElementById("event-list");

        // Genererer HTML-struktur for hver event og oppdaterer innholdet
        eventsList.innerHTML = events.map(event => {
            return `
                <div class="event-box">
                    <p><strong>Dato:</strong> ${event.dato}</p> 
                    <p><strong>Klokkeslett:</strong> ${event.klokkeslett || "Ikke spesifisert"}</p> 
                    <p><strong>Navn:</strong> ${event.navn_prosjektet || "Ikke spesifisert"}</p> 
                    <p><strong>Sted:</strong> ${event.sted || "Sted ikke tilgjengelig"}</p> 
                    <p><strong>Varsling:</strong> ${event.notification}</p> 
                </div>
            `;
        }).join(""); // Slår sammen alle HTML-strukturer til én streng
    } catch (error) {
        // feilhåndtering
        console.error("En feil oppsto under henting av eventer:", error.message);
    }
}



