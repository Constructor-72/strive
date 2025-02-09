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

        fetch(`/predict/${carId}`)
            .then(response => response.json())
            .then(data => {
                console.log(`Vorhersage für Auto ${carId}:`, data.prediction);
                if (data.confidence !== undefined) {
                    console.log(`Konfidenz: ${data.confidence.toFixed(2)}%`);
                }

                cardElement.classList.remove('ja', 'nein');
                if (data.prediction === 'Ja') {
                    cardElement.classList.add('ja');
                } else if (data.prediction === 'Nein') {
                    cardElement.classList.add('nein');
                }

                return fetch(`/get_car?id=${carId}`);
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Keine weiteren Autos verfügbar');
                }
                return response.json();
            })
            .then(data => {
                carTitleElement.textContent = data.title;

                let carDetails = `
                    <p><strong>Preis:</strong> ${data.price} €</p>
                    <p><strong>Kilometerstand:</strong> ${data.mileage} km</p>
                    <p><strong>Leistung (Hubraum):</strong> ${data.power} L</p>
                    <p><strong>Erstzulassung:</strong> ${data.firstRegistration}</p>
                    <p><strong>Getriebe:</strong> ${data.transmission}</p>
                    <p><strong>Kraftstofftyp:</strong> ${data.fuel}</p>
                    <p><strong>Kfz-Steuer:</strong> ${data.tax || 'Keine Angabe'} €</p>
                    <p><strong>Verbrauch:</strong> ${data.mpg || 'Keine Angabe'} mpg</p>
                `;
                carDetailsElement.innerHTML = carDetails;

                carImgElement.src = data.image || 'data/gap_filler.jpg';

                loadingOverlay.style.display = 'none'; // Ladeanzeige ausblenden
            })
            .catch(error => {
                console.warn(`Fehler beim Laden von Auto ${carId}:`, error);
                currentCarId++; // Nächstes Auto versuchen
                loadCarData(currentCarId);
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
