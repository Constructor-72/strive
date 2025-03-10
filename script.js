document.addEventListener('DOMContentLoaded', function() {
    let currentCarId = 1; // Start-Id für das erste Auto
    let carCounter = 0; // Zählt die Anzahl der geladenen Autos
    let cachedCars = []; // Cache für Auto-Daten
    let chatOpenedFrom = null; // Speichert, von wo aus der Chat geöffnet wurde ('detail' oder 'overview')

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
    const menuProfile = document.getElementById('menu-profile');
    const menuAddCar = document.getElementById('menu-add-car'); // Neuer Menüpunkt

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

    // Profilfenster-Elemente
    const profileWindow = document.getElementById('profile-window');
    const loginForm = document.getElementById('login-form');
    const profileInfo = document.getElementById('profile-info');
    const loginUsername = document.getElementById('login-username');
    const loginPassword = document.getElementById('login-password');
    const loginBtn = document.getElementById('login-btn');
    const registerBtn = document.getElementById('register-btn');
    const logoutBtn = document.getElementById('logout-btn');
    const profileUsername = document.getElementById('profile-username');
    const closeProfileBtn = document.getElementById('close-profile-btn'); // Schließen-Button (X)
    const skipDislikesToggle = document.getElementById('skip-dislikes-toggle'); // Toggle-Button für "Dislike"-Fahrzeuge

    // Neue Elemente für das Hinzufügen eines Autos
    const addCarWindow = document.getElementById('add-car-window'); // Fenster zum Hinzufügen eines Autos
    const addCarForm = document.getElementById('add-car-form'); // Formular zum Hinzufügen eines Autos
    const closeAddCarBtn = document.getElementById('close-add-car-btn'); // Schließen-Button für das Formular

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
        profileWindow.style.display = 'none';
        addCarWindow.style.display = 'none'; // Verstecke das Formular
        cardElement.style.display = 'flex';
        detailView.style.display = 'none';
    });

    // Menüpunkt "Chats" klicken
    menuChats.addEventListener('click', () => {
        menuDropdown.style.display = 'none';
        cardElement.style.display = 'none';
        detailView.style.display = 'none';
        chatWindow.style.display = 'none';
        profileWindow.style.display = 'none';
        addCarWindow.style.display = 'none'; // Verstecke das Formular
        chatOverview.style.display = 'flex';
        loadChatOverview();
    });

    // Menüpunkt "Mein Profil" klicken
    menuProfile.addEventListener('click', () => {
        menuDropdown.style.display = 'none';
        cardElement.style.display = 'none';
        detailView.style.display = 'none';
        chatWindow.style.display = 'none';
        chatOverview.style.display = 'none';
        addCarWindow.style.display = 'none'; // Verstecke das Formular
        profileWindow.style.display = 'flex';
        checkLoginStatus();
    });

    // Neuer Menüpunkt "Auto hinzufügen" klicken
    menuAddCar.addEventListener('click', () => {
        menuDropdown.style.display = 'none';
        cardElement.style.display = 'none';
        detailView.style.display = 'none';
        chatWindow.style.display = 'none';
        chatOverview.style.display = 'none';
        profileWindow.style.display = 'none';
        addCarWindow.style.display = 'flex'; // Zeige das Formular an
    });

    // Schließen-Button für das Formular zum Hinzufügen eines Autos
    closeAddCarBtn.addEventListener('click', () => {
        addCarWindow.style.display = 'none';
        cardElement.style.display = 'flex'; // Zurück zur Swipen-Ansicht
    });

    // Schließen-Button (X) im Profilfenster
    closeProfileBtn.addEventListener('click', () => {
        profileWindow.style.display = 'none'; // Verstecke das Profilfenster
        cardElement.style.display = 'flex'; // Zeige den Swipen-Bereich an
    });

    // Zurück zum Swipen (Chat-Übersicht)
    backToSwipe.addEventListener('click', () => {
        chatOverview.style.display = 'none'; // Verstecke die Chat-Übersicht
        cardElement.style.display = 'flex'; // Zeige den Swipen-Bereich an
    });

    // Formular zum Hinzufügen eines Autos absenden
    addCarForm.addEventListener('submit', (e) => {
        e.preventDefault();

        const brand = document.getElementById('brand').value;
        const model = document.getElementById('model').value;
        const price = parseFloat(document.getElementById('price').value);
        const mileage = parseInt(document.getElementById('mileage').value);
        const engineSize = parseFloat(document.getElementById('engineSize').value);
        const year = parseInt(document.getElementById('year').value);
        const transmission = document.getElementById('transmission').value;
        const fuelType = document.getElementById('fuelType').value;
        const tax = parseFloat(document.getElementById('tax').value);
        const mpg = parseFloat(document.getElementById('mpg').value);
        const images = document.getElementById('car-images').files;

        if (images.length > 3) {
            alert('Sie können maximal 3 Bilder hochladen.');
            return;
        }

        const formData = new FormData();
        formData.append('brand', brand);
        formData.append('model', model);
        formData.append('price', price);
        formData.append('mileage', mileage);
        formData.append('engineSize', engineSize);
        formData.append('year', year);
        formData.append('transmission', transmission);
        formData.append('fuelType', fuelType);
        formData.append('tax', tax);
        formData.append('mpg', mpg);

        for (let i = 0; i < images.length; i++) {
            formData.append('images', images[i]);
        }

        fetch('/add_car', {
            method: 'POST',
            body: formData
        })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    alert('Auto erfolgreich hinzugefügt!');
                    addCarWindow.style.display = 'none';
                    cardElement.style.display = 'flex'; // Zurück zur Swipen-Ansicht
                } else {
                    alert('Fehler beim Hinzufügen des Autos.');
                }
            })
            .catch(error => {
                console.error('Fehler:', error);
                alert('Fehler beim Hinzufügen des Autos.');
            });
    });

    // Überprüfe den Anmeldestatus
    function checkLoginStatus() {
        fetch('/check_login')
            .then(response => {
                if (!response.ok) {
                    throw new Error('Fehler beim Überprüfen des Anmeldestatus');
                }
                return response.json();
            })
            .then(data => {
                if (data.logged_in) {
                    loginForm.style.display = 'none';
                    profileInfo.style.display = 'block';
                    profileUsername.textContent = data.username;
                } else {
                    loginForm.style.display = 'block';
                    profileInfo.style.display = 'none';
                    // Standard-Nutzer verwenden
                    sessionStorage.setItem('username', 'guest');
                    profileUsername.textContent = 'Gast';
                }
            })
            .catch(error => {
                console.error('Fehler:', error);
                alert('Fehler beim Überprüfen des Anmeldestatus');
            });
    }

    // Anmelden
    loginBtn.addEventListener('click', () => {
        const username = loginUsername.value.trim();
        const password = loginPassword.value.trim();
        if (username && password) {
            fetch('/login', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ username, password })
            })
                .then(response => response.json())
                .then(data => {
                    if (data.status === 'success') {
                        window.location.reload(); // Seite neu laden
                    } else {
                        alert('Anmeldung fehlgeschlagen');
                    }
                });
        }
    });

    // Registrieren
    registerBtn.addEventListener('click', () => {
        const username = loginUsername.value.trim();
        const password = loginPassword.value.trim();
        if (username && password) {
            fetch('/register', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ username, password })
            })
                .then(response => response.json())
                .then(data => {
                    if (data.status === 'success') {
                        // Automatische Anmeldung nach der Registrierung
                        fetch('/login', {
                            method: 'POST',
                            headers: { 'Content-Type': 'application/json' },
                            body: JSON.stringify({ username, password })
                        })
                            .then(response => response.json())
                            .then(data => {
                                if (data.status === 'success') {
                                    window.location.reload(); // Seite neu laden
                                } else {
                                    alert('Automatische Anmeldung fehlgeschlagen');
                                }
                            });
                    } else {
                        alert('Registrierung fehlgeschlagen');
                    }
                });
        }
    });

    // Abmelden
    logoutBtn.addEventListener('click', () => {
        fetch('/logout', {
            method: 'POST'
        })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    // Verstecke alle anderen Bereiche und zeige den Anmeldebildschirm an
                    cardElement.style.display = 'none'; // Swipen ausblenden
                    detailView.style.display = 'none'; // Detailansicht ausblenden
                    chatWindow.style.display = 'none'; // Chatfenster ausblenden
                    chatOverview.style.display = 'none'; // Chat-Übersicht ausblenden
                    profileWindow.style.display = 'flex'; // Anmeldebildschirm anzeigen

                    // Setze das Anmeldeformular zurück
                    loginUsername.value = '';
                    loginPassword.value = '';
                    checkLoginStatus(); // Aktualisiere den Anmeldestatus
                }
            });
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
                            chatEntry.addEventListener('click', () => openChat(carId, 'overview')); // Öffne den Chat aus der Chat-Übersicht

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
    function openChat(carId, from) {
        currentChatCarId = carId; // Setze die aktuelle Chat-Auto-ID
        chatOpenedFrom = from; // Speichere, von wo aus der Chat geöffnet wurde

        if (from === 'detail') {
            detailView.style.display = 'none'; // Verstecke die Detailansicht
        } else if (from === 'overview') {
            chatOverview.style.display = 'none'; // Verstecke die Chat-Übersicht
        }

        chatWindow.style.display = 'flex'; // Zeige das Chatfenster an
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

    // Chatfenster schließen
    closeChatBtn.addEventListener('click', () => {
        chatWindow.style.display = 'none'; // Verstecke das Chatfenster

        // Entscheide, wohin der Benutzer zurückkehren soll
        if (chatOpenedFrom === 'detail') {
            detailView.style.display = 'flex'; // Zeige die Detailansicht an
        } else if (chatOpenedFrom === 'overview') {
            chatOverview.style.display = 'flex'; // Zeige die Chat-Übersicht an
        }

        chatOpenedFrom = null; // Setze den Zustand zurück
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
            .then(response => {
                if (!response.ok) {
                    throw new Error('Fehler beim Laden der Vorhersage');
                }
                return response.json();
            })
            .then(data => {
                console.log(`Vorhersage für Auto ${carId}:`, data.prediction);
    
                // Überprüfen, ob eine Vorhersage möglich war
                if (data.prediction === 'Keine eindeutige Vorhersage möglich.') {
                    console.warn('Keine Vorhersage möglich, da das Modell noch nicht genügend Daten hat.');
                    // Setze die Vorhersage auf einen Standardwert
                    data.prediction = 'Keine Vorhersage';
                    data.confidence = 0;
                } else if (data.confidence !== undefined) {
                    console.log(`Konfidenz: ${data.confidence.toFixed(2)}%`);
                }
    
                // Überspringe "Dislike"-Fahrzeuge, wenn der Button aktiviert ist und ab dem 30. Fahrzeug
                if (skipDislikesToggle.checked && carCounter >= 30 && data.prediction === 'Nein') {
                    console.log(`Fahrzeug ${carId} wird übersprungen (Dislike-Vorhersage).`);
                    currentCarId++; // Überspringe das aktuelle Fahrzeug
                    loadCarData(currentCarId); // Lade das nächste Fahrzeug
                    return;
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
        detailImage.src = car.image;

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

        // Lade die Bilder für das Auto
        fetch(`/get_car_images/${car.id}`)
            .then(response => response.json())
            .then(data => {
                const images = data.images;
                let currentImageIndex = 0;

                // Funktion zum Wechseln des Bildes
                function changeImage(direction) {
                    currentImageIndex += direction;
                    if (currentImageIndex >= images.length) {
                        currentImageIndex = 0;
                    } else if (currentImageIndex < 0) {
                        currentImageIndex = images.length - 1;
                    }
                    detailImage.src = images[currentImageIndex];
                }

                // Event-Listener für die Pfeiltasten
                document.getElementById('prev-image-btn').addEventListener('click', () => {
                    changeImage(-1);
                });

                document.getElementById('next-image-btn').addEventListener('click', () => {
                    changeImage(1);
                });

                // Event-Listener für die Pfeiltasten (Tastatur)
                document.addEventListener('keydown', (e) => {
                    if (e.key === 'ArrowRight') {
                        changeImage(1);
                    } else if (e.key === 'ArrowLeft') {
                        changeImage(-1);
                    }
                });

                // Event-Listener für Touch-Gesten (Mobile)
                let touchStartX = 0;
                detailImage.addEventListener('touchstart', (e) => {
                    touchStartX = e.touches[0].clientX;
                });

                detailImage.addEventListener('touchend', (e) => {
                    const touchEndX = e.changedTouches[0].clientX;
                    const deltaX = touchEndX - touchStartX;
                    if (deltaX > 50) {
                        changeImage(-1); // Wische nach rechts -> vorheriges Bild
                    } else if (deltaX < -50) {
                        changeImage(1); // Wische nach links -> nächstes Bild
                    }
                });
            })
            .catch(error => {
                console.error('Fehler beim Laden der Bilder:', error);
            });

        detailView.style.display = 'flex';
    }

    // Zurück zur Hauptansicht
    backBtn.addEventListener('click', () => {
        detailView.style.display = 'none';
    });

    // Chatfenster öffnen
    chatBtn.addEventListener('click', () => {
        currentChatCarId = currentCarId; // Setze die aktuelle Chat-Auto-ID auf die aktuelle Auto-ID
        openChat(currentChatCarId, 'detail'); // Öffne den Chat aus der Detailansicht
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