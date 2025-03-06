document.addEventListener('DOMContentLoaded', function() {
    let currentCarId = 1; // Start-Id für das erste Auto
    let carCounter = 0; // Zählt die Anzahl der geladenen Autos
    let cachedCars = []; // Cache für Auto-Daten

    // Elemente
    const carImgElement = document.getElementById('car-img');
    const carTitleElement = document.getElementById('car-title');
    const carDetailsElement = document.getElementById('car-details');
    const loadingOverlay = document.getElementById('loading-overlay');
    const cardElement = document.querySelector('.card');
    const swipeIndicator = document.getElementById('swipe-indicator');

    // Menü-Elemente
    const menuButton = document.getElementById('menu-button');
    const menuDropdown = document.getElementById('menu-dropdown');
    const menuSwipe = document.getElementById('menu-swipe');
    const menuChats = document.getElementById('menu-chats');

    // Chat-Übersicht-Elemente
    const chatOverview = document.getElementById('chat-overview');
    const chatList = document.getElementById('chat-list');
    const backToSwipe = document.getElementById('back-to-swipe');

    // Chatfenster-Elemente
    const chatWindow = document.getElementById('chat-window');
    const chatMessages = document.getElementById('chat-messages');
    const chatInput = document.getElementById('chat-input');
    const sendBtn = document.getElementById('send-btn');
    const closeChatBtn = document.getElementById('close-chat-btn');

    // Detailansicht-Elemente
    const detailView = document.getElementById('detail-view');
    const detailTitle = document.getElementById('detail-title');
    const detailImage = document.getElementById('detail-image');
    const detailInfo = document.getElementById('detail-info');
    const chatBtn = document.getElementById('chat-btn');
    const backBtn = document.getElementById('back-btn');

    // Variable zur Speicherung der aktuellen Chat-Auto-ID
    let currentChatCarId = null;

    // Menü-Button klicken
    menuButton.addEventListener('click', () => {
        menuDropdown.style.display = menuDropdown.style.display === 'block' ? 'none' : 'block';
    });

    // Menüpunkt "Swipen" klicken
    menuSwipe.addEventListener('click', () => {
        menuDropdown.style.display = 'none';
        chatOverview.style.display = 'none';
        chatWindow.style.display = 'none';
        cardElement.style.display = 'flex';
        detailView.style.display = 'none';
    });

    // Menüpunkt "Chats" klicken
    menuChats.addEventListener('click', () => {
        menuDropdown.style.display = 'none';
        cardElement.style.display = 'none';
        detailView.style.display = 'none';
        chatWindow.style.display = 'none';
        chatOverview.style.display = 'flex';
        loadChatOverview();
    });

    // Zurück zum Swipen
    backToSwipe.addEventListener('click', () => {
        chatOverview.style.display = 'none';
        cardElement.style.display = 'flex';
    });

    // Funktion zum Laden der Chat-Übersicht
    function loadChatOverview() {
        fetch('/get_chats')
            .then(response => response.json())
            .then(data => {
                chatList.innerHTML = '';
                const uniqueCarIds = [...new Set(data.map(chat => chat.car_id))]; // Eindeutige Auto-IDs
                uniqueCarIds.forEach(carId => {
                    // Lade die Auto-Daten für den Titel und das Bild
                    fetch(`/get_car?id=${carId}`)
                        .then(response => response.json())
                        .then(carData => {
                            const chatEntry = document.createElement('div');
                            chatEntry.className = 'chat-entry';

                            // Bild des Autos
                            const carImage = document.createElement('img');
                            carImage.src = carData.image || 'data/gap_filler.jpg';
                            carImage.className = 'chat-car-image';

                            // Titel des Autos
                            const carTitle = document.createElement('span');
                            carTitle.textContent = carData.title;

                            // Füge Bild und Titel zum Chat-Eintrag hinzu
                            chatEntry.appendChild(carImage);
                            chatEntry.appendChild(carTitle);

                            // Klick-Event zum Öffnen des Chats
                            chatEntry.addEventListener('click', () => openChat(carId));

                            // Füge den Chat-Eintrag zur Liste hinzu
                            chatList.appendChild(chatEntry);
                        })
                        .catch(error => {
                            console.error('Fehler beim Laden der Auto-Daten:', error);
                        });
                });
            })
            .catch(error => {
                console.error('Fehler beim Laden der Chats:', error);
            });
    }

    // Funktion zum Öffnen eines Chats
    function openChat(carId) {
        currentChatCarId = carId; // Setze die aktuelle Chat-Auto-ID
        chatOverview.style.display = 'none';
        cardElement.style.display = 'none';
        detailView.style.display = 'none';
        chatWindow.style.display = 'flex';
        loadChatMessages(carId);
    }

    // Funktion zum Laden der Chat-Nachrichten
    function loadChatMessages(carId) {
        fetch(`/get_chat_messages/${carId}`)
            .then(response => response.json())
            .then(data => {
                chatMessages.innerHTML = ''; // Leere die Nachrichten vor dem Laden
                data.forEach(chat => {
                    if (chat.car_id === carId) { // Nur Nachrichten für das aktuelle Auto anzeigen
                        const messageElement = document.createElement('div');
                        messageElement.textContent = `Ich: ${chat.message}`;
                        chatMessages.appendChild(messageElement);
                    }
                });
            })
            .catch(error => {
                console.error('Fehler beim Laden der Chat-Nachrichten:', error);
            });
    }

    // Chatfenster schließen und zurück zur Chat-Übersicht
    closeChatBtn.addEventListener('click', () => {
        chatWindow.style.display = 'none';
        chatOverview.style.display = 'flex';
    });

    // Nachricht senden
    sendBtn.addEventListener('click', () => {
        const message = chatInput.value.trim();
        if (message && currentChatCarId) { // Nur senden, wenn eine Nachricht und eine gültige Auto-ID vorhanden sind
            const chatEntry = {
                car_id: currentChatCarId, // Verwende die aktuelle Chat-Auto-ID
                message: message,
                timestamp: new Date().toLocaleString()
            };

            // Nachricht speichern
            fetch('/save_chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(chatEntry)
            })
                .then(response => response.json())
                .then(data => {
                    console.log('Chat gespeichert:', data);
                    // Nachricht im Chatfenster anzeigen
                    const messageElement = document.createElement('div');
                    messageElement.textContent = `Ich: ${message}`;
                    chatMessages.appendChild(messageElement);
                    chatInput.value = ''; // Eingabefeld leeren
                })
                .catch(error => {
                    console.error('Fehler beim Speichern des Chats:', error);
                });
        } else {
            console.warn('Nachricht oder Auto-ID fehlt.');
            console.log('Aktuelle Chat-Auto-ID:', currentChatCarId);
            console.log('Nachricht:', message);
        }
    });

    // Funktion zum Laden eines neuen Autos
    function loadCarData(carId) {
        loadingOverlay.style.display = 'flex'; // Ladeanzeige aktivieren

        // Überprüfen, ob das Auto bereits im Cache ist
        const cachedCar = cachedCars.find(car => car.id === carId);
        if (cachedCar) {
            displayCarData(cachedCar);
            return;
        }

        // Auto-Daten vom Server laden
        fetch(`/predict/${carId}`)
            .then(response => response.json())
            .then(data => {
                console.log(`Vorhersage für Auto ${carId}:`, data.prediction);
                if (data.confidence !== undefined) {
                    console.log(`Konfidenz: ${data.confidence.toFixed(2)}%`);
                }

                // Immer Klassen hinzufügen, aber Farben erst nach 30 Autos aktivieren
                cardElement.classList.remove('ja', 'nein');
                if (data.prediction === 'Ja') {
                    cardElement.classList.add('ja');
                } else if (data.prediction === 'Nein') {
                    cardElement.classList.add('nein');
                }

                // Zähler erhöhen
                carCounter++;

                // Falls 30 Autos geladen wurden, Klasse für sichtbare Farben aktivieren
                if (carCounter >= 30) {
                    cardElement.classList.add('visible-colors');
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
                // Auto-Daten im Cache speichern
                cachedCars.push(data);
                displayCarData(data);
            })
            .catch(error => {
                console.warn(`Fehler beim Laden von Auto ${carId}:`, error);
                currentCarId++;
                loadCarData(currentCarId);
            });
    }

    // Funktion zum Anzeigen der Auto-Daten
    function displayCarData(data) {
        carTitleElement.textContent = data.title;

        // Informationen in zwei Spalten anzeigen
        let carDetails = `
            <div class="car-details">
                <div class="left">
                    <p><strong>Preis:</strong> ${data.price} €</p>
                    <p><strong>Kilometerstand:</strong> ${data.mileage} km</p>
                </div>
                <div class="right">
                    <p><strong>Erstzulassung:</strong> ${data.firstRegistration}</p>
                    <p><strong>Getriebe:</strong> ${data.transmission}</p>
                </div>
            </div>
        `;
        carDetailsElement.innerHTML = carDetails;

        carImgElement.src = data.image || 'data/gap_filler.jpg';

        loadingOverlay.style.display = 'none'; // Ladeanzeige ausblenden
    }

    // Doppelklick für die Detailansicht (Desktop)
    cardElement.addEventListener('dblclick', () => {
        const car = cachedCars.find(car => car.id === currentCarId);
        if (car) {
            showDetailView(car);
        }
    });

    // Long Press für die Detailansicht (Mobile)
    let pressTimer;
    cardElement.addEventListener('touchstart', (e) => {
        pressTimer = setTimeout(() => {
            const car = cachedCars.find(car => car.id === currentCarId);
            if (car) {
                showDetailView(car);
            }
        }, 500); // 500 Millisekunden für Long Press
    });

    cardElement.addEventListener('touchend', () => {
        clearTimeout(pressTimer);
    });

    cardElement.addEventListener('touchmove', () => {
        clearTimeout(pressTimer);
    });

    // Detailansicht anzeigen
    function showDetailView(car) {
        detailTitle.textContent = car.title;
        detailImage.src = car.image || 'data/gap_filler.jpg';

        // Fülle die linke Spalte
        document.getElementById('detail-price').textContent = car.price;
        document.getElementById('detail-mileage').textContent = car.mileage;
        document.getElementById('detail-power').textContent = car.power;
        document.getElementById('detail-registration').textContent = car.firstRegistration;

        // Fülle die rechte Spalte
        document.getElementById('detail-transmission').textContent = car.transmission;
        document.getElementById('detail-fuel').textContent = car.fuel;
        document.getElementById('detail-tax').textContent = car.tax || 'Keine Angabe';
        document.getElementById('detail-mpg').textContent = car.mpg || 'Keine Angabe';

        detailView.style.display = 'flex';
    }

    // Zurück zur Hauptansicht
    backBtn.addEventListener('click', () => {
        detailView.style.display = 'none';
    });

    // Chatfenster öffnen
    chatBtn.addEventListener('click', () => {
        currentChatCarId = currentCarId; // Setze die aktuelle Chat-Auto-ID auf die aktuelle Auto-ID
        chatWindow.style.display = 'flex';
        loadChatMessages(currentChatCarId);
    });

    // Hammer.js für Swipe-Gesten
    const hammer = new Hammer(cardElement);
    hammer.get('pan').set({ direction: Hammer.DIRECTION_ALL, threshold: 30 });

    let deltaX = 0;

    hammer.on('panstart', () => {
        deltaX = 0;
        swipeIndicator.style.opacity = 0;
    });

    hammer.on('pan', (ev) => {
        deltaX = ev.deltaX;
        cardElement.style.transform = `translate(${ev.deltaX}px, ${ev.deltaY}px) rotate(${ev.deltaX / 20}deg)`;

        if (deltaX > 0) {
            swipeIndicator.textContent = "LIKE";
            swipeIndicator.style.color = "#4CAF50";
            swipeIndicator.style.left = "20px";
            swipeIndicator.style.right = "auto";
            swipeIndicator.style.transform = "rotate(-20deg)";
        } else if (deltaX < 0) {
            swipeIndicator.textContent = "NOPE";
            swipeIndicator.style.color = "#F44336";
            swipeIndicator.style.right = "20px";
            swipeIndicator.style.left = "auto";
            swipeIndicator.style.transform = "rotate(20deg)";
        } else {
            swipeIndicator.textContent = "";
        }

        let opacity = Math.min(Math.abs(deltaX) / 150, 1);
        swipeIndicator.style.opacity = opacity;
    });

    hammer.on('panend', (ev) => {
        if (Math.abs(deltaX) > 150 && Math.abs(ev.velocityX) > 0.3) {
            let action = (deltaX > 0) ? 'like' : 'dislike';
            cardElement.style.transition = 'transform 0.5s ease-out';
            cardElement.style.transform = `translate(${deltaX > 0 ? 1000 : -1000}px, ${ev.deltaY}px) rotate(${ev.deltaX / 20}deg)`;

            // Feedback senden
            sendFeedback(currentCarId, action);

            // Nächstes Auto laden
            currentCarId++;
            setTimeout(() => {
                cardElement.style.transition = 'none';
                cardElement.style.transform = 'translate(0,0)';
                loadCarData(currentCarId);
                swipeIndicator.style.opacity = 0;
            }, 500);
        } else {
            cardElement.style.transition = 'transform 0.3s ease-out';
            cardElement.style.transform = 'translate(0,0)';
            swipeIndicator.style.opacity = 0;
            setTimeout(() => cardElement.style.transition = 'none', 300);
        }
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
            .catch(error => {
                console.error('Fehler beim Senden des Feedbacks:', error);
            });
    }

    // Initiales Auto laden
    loadCarData(currentCarId);
});