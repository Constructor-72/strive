document.addEventListener('DOMContentLoaded', function() {
    let currentCarId = 1; // Start-Id für das erste Auto

    // Elemente
    const carImgElement = document.getElementById('car-img');
    const carTitleElement = document.getElementById('car-title');
    const carDetailsElement = document.getElementById('car-details');
    const likeButton = document.getElementById('like-btn');
    const dislikeButton = document.getElementById('dislike-btn');
    const loadingOverlay = document.getElementById('loading-overlay');
    const cardElement = document.querySelector('.card');

    // Funktion zum Laden eines neuen Autos
    function loadCarData(carId) {
        loadingOverlay.style.display = 'flex'; // Ladeanzeige aktivieren

        // Sende die Anfrage an den Server, um die Vorhersage für das Auto zu bekommen
        fetch(`/predict/${carId}`)
            .then(response => response.json())
            .then(data => {
                console.log(`Vorhersage für Auto ${carId}:`, data.prediction);
                if (data.confidence !== undefined) {
                    console.log(`Konfidenz: ${data.confidence.toFixed(2)}%`);
                }

                // Hintergrundfarbe basierend auf der Vorhersage ändern
                cardElement.classList.remove('ja', 'nein'); // Entferne vorherige Klassen
                if (data.prediction === 'Ja') {
                    cardElement.classList.add('ja');
                } else if (data.prediction === 'Nein') {
                    cardElement.classList.add('nein');
                }

                // Sende die Anfrage an den Server, um die Daten für das Auto zu bekommen
                return fetch(`/get_car?id=${carId}`);
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Keine weiteren Autos verfügbar');
                }
                return response.json();
            })
            .then(data => {
                // Title setzen
                carTitleElement.textContent = data.title; // Titel direkt aus der JSON-Daten

                // Details vorbereiten
                let carDetails = `
                    <p><strong>Preis:</strong> ${data.price}</p>
                    <p><strong>Kilometerstand:</strong> ${data.mileage} km</p>
                    <p><strong>Leistung (PS):</strong> ${data.power} PS</p>
                    <p><strong>Erstzulassung:</strong> ${data.firstRegistration}</p>
                    <p><strong>Getriebe:</strong> ${data.transmission}</p>
                    <p><strong>Farbe:</strong> ${data.color}</p>
                    <p><strong>Vorbesitzer:</strong> ${data.owners}</p>
                `;
                carDetailsElement.innerHTML = carDetails; // HTML-Inhalt mit den Details setzen

                // Bild setzen
                carImgElement.src = data.image;

                loadingOverlay.style.display = 'none'; // Ladeanzeige ausblenden
            })
            .catch(error => {
                console.error('Fehler beim Laden des Autos:', error);
                alert('Fehler: Keine weiteren Autos verfügbar.');
                loadingOverlay.style.display = 'none'; // Ladeanzeige ausblenden
            });
    }

    // Like-Button Klick-Event
    likeButton.addEventListener('click', function() {
        sendFeedback(currentCarId, 'like');
        currentCarId++;
        loadCarData(currentCarId);
    });

    // Dislike-Button Klick-Event
    dislikeButton.addEventListener('click', function() {
        sendFeedback(currentCarId, 'dislike');
        currentCarId++;
        loadCarData(currentCarId);
    });

    // Funktion zum Senden von Feedback
    function sendFeedback(carId, action) {
        fetch('/feedback', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ car_id: carId, action: action })
        })
            .then(response => response.json())
            .then(data => {
                console.log('Feedback gesendet:', data);
            })
            .catch(error => console.error('Fehler beim Senden des Feedbacks:', error));
    }

    // Initiales Auto laden
    loadCarData(currentCarId);
});