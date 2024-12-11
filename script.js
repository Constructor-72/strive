document.addEventListener('DOMContentLoaded', function() {
    let currentCarId = 1; // Start-Id für das erste Auto
    const likedCars = [];
    const dislikedCars = [];

    // Elemente
    const carImageElement = document.getElementById('car-image');
    const carImgElement = document.getElementById('car-img');
    const carInfoElement = document.getElementById('car-info');
    const carTitleElement = document.getElementById('car-title');
    const carDetailsElement = document.getElementById('car-details');
    const carIdElement = document.getElementById('car-id');
    const likeButton = document.getElementById('like-btn');
    const dislikeButton = document.getElementById('dislike-btn');
    const loadingOverlay = document.getElementById('loading-overlay');

    // Funktion zum Laden eines neuen Autos
    function loadCarData(carId) {
        loadingOverlay.style.display = 'flex'; // Ladeanzeige aktivieren

        // Sende die Anfrage an den Server, um die Daten für das Auto zu bekommen
        fetch(`/get_car?id=${carId}`)
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    alert('Fehler beim Laden des Autos');
                    return;
                }

                // Daten für das Auto anzeigen
                const car = data;
                carImgElement.src = car.image;
                carTitleElement.textContent = `Auto ${car.id}`;
                carDetailsElement.innerHTML = car.details;
                carIdElement.textContent = car.id;

                loadingOverlay.style.display = 'none'; // Ladeanzeige ausblenden
            })
            .catch(error => {
                console.error('Fehler beim Laden des Autos:', error);
                loadingOverlay.style.display = 'none'; // Ladeanzeige ausblenden
            });
    }

    // Like-Button Klick-Event
    likeButton.addEventListener('click', function() {
        likedCars.push(currentCarId);
        console.log('Gelikt:', currentCarId);
        // console.log('Gelikte Autos:', likedCars);

        // Nächsten Datensatz laden
        currentCarId++;
        loadCarData(currentCarId);
    });

    // Dislike-Button Klick-Event
    dislikeButton.addEventListener('click', function() {
        dislikedCars.push(currentCarId);
        console.log('Gedisliked:', currentCarId);
        // console.log('Gedislikte Autos:', dislikedCars);

        // Nächsten Datensatz laden
        currentCarId++;
        loadCarData(currentCarId);
    });

    // Initiales Auto laden
    loadCarData(currentCarId);
});
