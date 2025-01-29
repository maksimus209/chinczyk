/******************************************************
 * game.js – pełny kod z obsługą dynamicznej aktualizacji
 ******************************************************/

// Zmienna globalna, by pamiętać wybrany pionek
let selectedTokenIndex = null;

/**
 * Funkcja wywoływana po kliknięciu przycisku "Rzuć kostką".
 * Wywołuje endpoint /roll_dice i aktualizuje stan gry oraz komunikaty.
 */
async function handleRollDice() {
  try {
    const response = await fetch("/roll_dice", {
      method: "POST"
    });
    const data = await response.json();

    if (data.error) {
      document.getElementById("message").textContent = data.error;
      return;
    }

    // Wyrzucona liczba oczek
    document.getElementById("dice-value").textContent = data.dice_value;

    // Komunikat z serwera (np. "Nie możesz wyprowadzić pionka...")
    if (data.message) {
      document.getElementById("message").textContent = data.message;
    }

    // Aktualizujemy stan i widok planszy
    updateBoard(data.state);

    // Jeśli data.dice_value < 6 i gracz ma pionek na planszy...
    //   -> zablokuj rollDiceBtn, żeby wymusić ruch pionkiem:
    if (data.dice_value < 6) {
      // Sprawdzamy, czy na pewno gracz ma pionek w polu [0..39],
      // bo jeśli nie – to i tak nic nie zrobi.
      const currentPlayer = data.state.players.find(
        p => p.color === data.state.current_player
      );
      const hasTokenOnBoard = currentPlayer.tokens.some(t => t >= 0 && t < 40);

      if (hasTokenOnBoard) {
        // Zablokuj przycisk
        const rollDiceBtn = document.getElementById("roll-dice-btn");
        rollDiceBtn.disabled = true;
      }
    }

  } catch (error) {
    console.error("Błąd przy rzucaniu kostką:", error);
  }
}

/**
 * Funkcja wywoływana po kliknięciu w pionek na planszy/bazie.
 * Zapisuje tokenIndex wybranego pionka i pozwala przesunąć pionek.
 */
async function handleTokenClick(event) {
  const tokenElement = event.currentTarget;
  const playerColor = tokenElement.getAttribute("data-player");
  const tokenIndex = tokenElement.getAttribute("data-token-index");
  const tokenPos = parseInt(tokenElement.getAttribute("data-position"), 10);
  const diceValue = parseInt(document.getElementById("dice-value").textContent, 10);

  // Aktualny gracz (np. "red", "blue" itp.)
  const currentPlayerColor = document.getElementById("current-player").textContent;

  // Jeśli pionek jest w bazie (-1) i diceValue < 6 -> nie można wyprowadzić
  if (tokenPos === -1 && diceValue < 6) {
    showTemporaryMessage("Nie możesz wyprowadzić tego pionka, proszę wykonać ruch pionkiem na planszy.");
    return;
  }

  // Blokada pionków innego gracza
  if (playerColor !== currentPlayerColor) {
    showTemporaryMessage("Nie są to pionki twojego koloru");
    return;
  }

  // Zapamiętujemy wybrany pionek
  selectedTokenIndex = tokenIndex;
  document.getElementById("message").textContent =
    `Gracz ${currentPlayerColor} wybrał pionek: indeks ${tokenIndex}.`;

  // Odblokowujemy przycisk "Przesuń pionek"
  const moveBtn = document.getElementById("move-token-btn");
  moveBtn.disabled = false;
}

/**
 * Funkcja wywoływana po kliknięciu "Przesuń pionek".
 * Wysyła żądanie POST do /move z wybranym pionkiem i aktualizuje stan gry.
 */
async function handleMoveToken() {
  if (selectedTokenIndex === null) {
    showTemporaryMessage("Nie wybrano pionka do przesunięcia");
    return;
  }

  try {
    const response = await fetch("/move", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ token_index: selectedTokenIndex })
    });
    const data = await response.json();

    if (data.error) {
      document.getElementById("message").textContent = data.error;
      return;
    }

    // Komunikat z serwera (np. "Gracz red: Pionek 0 wyprowadzony na pole 0")
    document.getElementById("message").textContent = data.message;

    // Aktualizujemy stan i widok
    updateBoard(data.state);

    // Sprawdzamy, czy gra się skończyła
    if (data.game_over) {
      alert(`Koniec gry! Wygrał gracz: ${data.winner}`);
      document.getElementById("message").textContent = `Koniec gry! Wygrał gracz: ${data.winner}`;
      document.getElementById("roll-dice-btn").disabled = true;
      document.getElementById("move-token-btn").disabled = true;

      // Pokazujemy przyciski do nowej gry / menu
      const endGameActions = document.getElementById("end-game-actions");
      if (endGameActions) {
        endGameActions.style.display = "block";
      }
    }
    else{
      // Sprawdź, czy dice_value == 6, bo wtedy w tej samej turze
      // można dalej rzucać kostką
      if (data.state.dice_value === 6) {
        // Odblokuj rzut kostką
        document.getElementById("roll-dice-btn").disabled = false;
      } else {
        // Jeżeli tura się skończyła i gracz jest nowy,
        // to nowy gracz też powinien mieć rollDiceBtn odblokowane
        document.getElementById("roll-dice-btn").disabled = false;
      }
    }

  } catch (error) {
    console.error("Błąd przy wywołaniu /move:", error);
  } finally {
    // Niezależnie od wyniku ruchu, resetujemy przycisk i wybrany pionek
    const moveBtn = document.getElementById("move-token-btn");
    moveBtn.disabled = true;
    selectedTokenIndex = null;
  }
}

/**
 * Funkcja do tymczasowego wyświetlania komunikatu (znika po paru sekundach).
 */
function showTemporaryMessage(tempText, duration = 3000) {
  const messageEl = document.getElementById("message");
  const oldMessage = messageEl.textContent;

  messageEl.textContent = tempText;

  setTimeout(() => {
    messageEl.textContent = oldMessage;
  }, duration);
}

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
 * Funkcja updateBoard – dynamicznie aktualizuje planszę, bazy i domki
 * na podstawie obiektu `state` zwróconego przez serwer.
 */
function updateBoard(state) {
  // 1. Czyścimy bazy (elementy .base)
  const bases = document.querySelectorAll(".base");
  bases.forEach(base => {
    base.innerHTML = "";
  });

  // 2. Czyścimy pola planszy (0–39)
  for (let i = 0; i < 40; i++) {
    const cellEl = document.getElementById(`cell-${i}`);
    if (cellEl) {
      cellEl.innerHTML = "";
    }
  }

  // 3. Czyścimy domki
  const homes = document.querySelectorAll(".home-section");
  homes.forEach(home => {
    home.innerHTML = `
      <div class="home ${home.classList[1]}"></div>
      <div class="home ${home.classList[1]}"></div>
      <div class="home ${home.classList[1]}"></div>
      <div class="home ${home.classList[1]}"></div>
    `;
  });

  // 4. Wstawiamy pionki na podstawie state
  state.players.forEach(player => {
    player.tokens.forEach((tokenPos, tokenIndex) => {
      if (tokenPos === -1) {
        // Pionek w bazie
        const baseEl = document.querySelector(`.base.${player.color}`);
        if (baseEl) {
          baseEl.innerHTML += `
            <span
              class="token ${player.color}"
              data-player="${player.color}"
              data-token-index="${tokenIndex}"
              data-position="-1"
            >
              ${player.color[0]}
            </span>
          `;
        }
      } else if (tokenPos >= 0 && tokenPos < 40) {
        // Pionek na planszy
        const cellEl = document.getElementById(`cell-${tokenPos}`);
        if (cellEl) {
          cellEl.innerHTML += `
            <span
              class="token ${player.color}"
              data-player="${player.color}"
              data-token-index="${tokenIndex}"
              data-position="$(tokenPos)"
            >
              ${player.color[0]}
            </span>
          `;
        }
      } else if (tokenPos === -2) {
        // Pionek w domku – tu musisz doprecyzować, jak wstawiasz pionki do domku
        // Na przykład:
        const homeSection = document.querySelector(`.home-section.${player.color}`);
        if (homeSection) {
          // Znajdź pierwsze wolne child .home wewnątrz homeSection i wstaw pionek
          // Poniżej wersja przykładowa:
          const homeCells = homeSection.querySelectorAll(".home");
          for (let h = 0; h < homeCells.length; h++) {
            if (!homeCells[h].hasChildNodes()) {
              homeCells[h].innerHTML = `
                <span
                  class="token ${player.color}"
                  data-player="${player.color}"
                  data-token-index="${tokenIndex}"
                >
                  ${player.color[0]}
                </span>
              `;
              break;
            }
          }
        }
      }
    });
  });

  // 5. Uaktualniamy aktualnego gracza, numer tury i dice_value
  document.getElementById("current-player").textContent = state.current_player;
  document.getElementById("turn-number").textContent = state.turn_number;
  document.getElementById("dice-value").textContent = state.dice_value;

  // 6. Na koniec podpinamy nasłuchiwanie kliknięć do nowo dodanych pionków
  attachTokenClickHandlers();
}

/**
 * Inicjalizacja zdarzeń po załadowaniu DOM.
 * - Podpięcie "Rzuć kostką"
 * - Podpięcie "Przesuń pionek"
 * - Podpięcie kliknięć w pionki
 */
document.addEventListener("DOMContentLoaded", () => {
  // Obsługa "Rzuć kostką"
  const rollDiceBtn = document.getElementById("roll-dice-btn");
  if (rollDiceBtn) {
    rollDiceBtn.addEventListener("click", handleRollDice);
  }

  // Obsługa kliknięć w pionki (pierwsze podpięcie)
  attachTokenClickHandlers();

  // Obsługa "Przesuń pionek"
  const moveBtn = document.getElementById("move-token-btn");
  if (moveBtn) {
    moveBtn.addEventListener("click", handleMoveToken);
  }

  const newGameBtn = document.getElementById("btn-new-game");
  if (newGameBtn) {
    newGameBtn.addEventListener("click", handleNewGame);
  }
});

rollDiceBtn.addEventListener("click", (event) => {
  if (rollDiceBtn.disabled) {
    showTemporaryMessage("Nie możesz rzucić kostką, najpierw wykonaj ruch pionkiem!");
    // Zatrzymaj event
    event.preventDefault();
    return;
  }
  handleRollDice();
});

function handleNewGame() {
  // Najprościej: przeładuj stronę /game z POST, żeby zainicjalizować nową grę
  // (lub jeśli masz inną ścieżkę /new_game, możesz tam przekierować)
  window.location.href = "/"; // np. wróć na stronę główną, a stamtąd user wybierze nową grę
  // lub:
  // window.location.reload();
}


