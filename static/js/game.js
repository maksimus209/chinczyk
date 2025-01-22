// Funkcja wywoływana po kliknięciu przycisku "Rzuć kostką"
async function handleRollDice() {
  try {
    const response = await fetch("/roll_dice", {
      method: "POST"
    });
    const data = await response.json();

    if (data.error) {
      // Obsługa sytuacji, gdy gra jest niezainicjalizowana
      document.getElementById("message").textContent = data.error;
      return;
    }

    // Aktualizujemy w UI wyrzuconą liczbę oczek
    document.getElementById("dice-value").textContent = data.dice_value;

    // Aktualizujemy cały stan gry
    updateBoard(data.state);

  } catch (error) {
    console.error("Błąd przy rzucaniu kostką:", error);
  }
}

// Funkcja do zaktualizowania widoku planszy
function updateBoard(state) {
  // 1. Zmieniamy wyświetlanego aktualnego gracza
  document.getElementById("current-player").textContent = state.current_player;

  // 2. Numer tury
  document.getElementById("turn-number").textContent = state.turn_number;

  // 3. Czyszczenie komunikatów
  document.getElementById("message").textContent = "";

  // 4. Aktualizacja pionków na planszy i w bazie
  //    - Możesz np. wyczyścić zawartość pól i ponownie ustawić pionki
  //    - Ale jeżeli generujesz je przez Jinja2 (na serwerze),
  //      to na tym etapie wystarczyłoby przeładować fragment HTML
  //      lub wstawić nowy HTML przez AJAX.
  //    - Dla prostoty: na razie zostawmy to w spokoju.
}

// Podpinamy event listener do przycisku "Rzuć kostką"
document.addEventListener("DOMContentLoaded", () => {
  // 1. Obsługa rzutu kostką (już mamy z poprzedniego kroku)
  const rollDiceBtn = document.getElementById("roll-dice-btn");
  if (rollDiceBtn) {
    rollDiceBtn.addEventListener("click", handleRollDice);
  }

  // 2. Funkcja, która podłącza nasłuchiwanie kliknięć w pionki
  attachTokenClickHandlers();
});

/**
 * Funkcja, która wyszukuje wszystkie pionki (elementy .token)
 * i podpina zdarzenie onclick do obsługi kliknięcia.
 */
function attachTokenClickHandlers() {
  const tokens = document.querySelectorAll(".token");
  tokens.forEach(tokenElement => {
    tokenElement.addEventListener("click", handleTokenClick);
  });
}

/**
 * Funkcja wywoływana po kliknięciu w pionek
 */
async function handleTokenClick(event) {
  // 1. Pobieramy informację o klikniętym pionku
  const tokenElement = event.currentTarget;
  const playerColor = tokenElement.getAttribute("data-player");
  const tokenIndex = tokenElement.getAttribute("data-token-index");

  // Na razie można dodać informacyjnego console.log
  console.log(`Kliknięty pionek: kolor=${playerColor}, index=${tokenIndex}`);

  // 2. Wywołujemy endpoint "/move"
  try {
    const response = await fetch("/move", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ token_index: tokenIndex })
    });

    const data = await response.json();
    if (data.error) {
      document.getElementById("message").textContent = data.error;
      return;
    }

    // 3. Wyświetlamy komunikat zwrócony przez serwer
    document.getElementById("message").textContent = data.message;

    // 4. Aktualizujemy stan gry w UI
    updateBoard(data.state);

    // 5. Sprawdzamy, czy gra się skończyła
    if (data.game_over) {
      alert(`Koniec gry! Wygrał gracz: ${data.winner}`);
      // Ewentualnie zablokuj przyciski / przejdź do ekranu końcowego
    }

  } catch (error) {
    console.error("Błąd przy wywołaniu /move:", error);
  }
}


