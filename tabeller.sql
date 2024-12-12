CREATE TABLE events_ny (
    id INT AUTO_INCREMENT PRIMARY KEY,
    dato DATE NOT NULL,
    klokkeslett TIME NOT NULL,
    navn_prosjektet VARCHAR(100) NOT NULL,
    sted VARCHAR(100) NOT NULL,
    notification VARCHAR(50) DEFAULT 'no-notification',
    brukerID INT NOT NULL
);

-- Create the bruker table
CREATE TABLE bruker (
    brukerID INT AUTO_INCREMENT PRIMARY KEY,
    e_post VARCHAR(255) NOT NULL UNIQUE,     
    passord VARCHAR(255) NOT NULL,           
    fornavn VARCHAR(100) NOT NULL,           
    etternavn VARCHAR(100) NOT NULL,         
);

/*Query for å søke et bestemt event fra en bestemt user*/
SELECT * 
FROM events_ny 
WHERE navn_prosjektet = '' 
AND brukerID = (
    SELECT brukerID 
    FROM bruker 
    WHERE fornavn = '' 
    AND etternavn = ''
);

--Hvis man vet bruker ID
SELECT * 
FROM events_ny 
WHERE navn_prosjektet = ''
AND brukerID = 1; 

DESCRIBE bruker;
DESCRIBE events_ny;

SELECT * FROM events_ny;
SELECT * FROM bruker;
