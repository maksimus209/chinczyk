
class Player:
    def __init__(self, color):
        self.color = color
        self.tokens = [-1, -1, -1, -1]  # Pionki (-1 oznacza, że są w schowku)
        self.finished_tokens = 0  # Liczba pionków w domku
        self.rolls_left = 0  # Na starcie 0, ustalimy przy pierwszym rzucie

    def move_token(self, token_index, steps, board):
        """Przesuń pionek o zadaną liczbę pól."""
        current_position = self.tokens[token_index]
        start_position = board.start_fields[self.color]
        max_position = board.max_positions[self.color]

        print(
            f"[DEBUG] Gracz {self.color} – Pionek {token_index}: obecna pozycja {current_position}, ruch o {steps} kroków.")

        # Jeśli pionek jest w schowku, sprawdź czy może wejść na planszę
        if current_position == -1:
            if steps == 6:  # Warunek wyjścia na planszę
                self.tokens[token_index] = start_position
                print(
                    f"[DEBUG] Gracz {self.color} – Pionek {token_index} wyprowadzony na pole {self.tokens[token_index]}.")
                return f"Pionek {token_index} został wyprowadzony na pole {self.tokens[token_index]}"
            else:
                return f"Pionek {token_index} nie może opuścić schowka"

        # Jeśli pionek jest na maksymalnym polu przed startowym
        if current_position == max_position:
            required_steps = 4 - self.finished_tokens  # Liczba oczek potrzebna do wejścia do domku
            if steps == required_steps:
                self.finished_tokens += 1
                self.tokens[token_index] = -2  # Pionek w domku
                print(
                    f"[DEBUG] Gracz {self.color} – Pionek {token_index} wszedł do domku. Suma w domku: {self.finished_tokens}")
                return f"Pionek {token_index} wszedł do domku!"
            else:
                print(
                    f"[DEBUG] Gracz {self.color} – Pionek {token_index} musi wyrzucić {required_steps}, aby wejść do domku.")
                return f"Pionek {token_index} musi wyrzucić {required_steps}, aby wejść do domku"

        # Jeśli ruch przekroczy maksymalne pole, a gracz nie dotarł do domku
        if current_position < max_position and current_position + steps > max_position:
            print(f"[DEBUG] Gracz {self.color} – Pionek {token_index}: za dużo oczek, ruch niemożliwy.")
            return f"Pionek {token_index} nie może wykonać ruchu – za dużo oczek"

        # Standardowy ruch na planszy
        new_position = board.move(current_position, steps)
        print(f"[DEBUG] Gracz {self.color} – Pionek {token_index}: nowa pozycja {new_position}.")

        # 1. Sprawdzamy pole śmiertelne
        if new_position in board.death_fields[self.color]:
            self.tokens[token_index] = -1
            return (f"Pionek {token_index} stanął na śmiertelnym polu {new_position} "
                    f"i wraca do bazy!")

        if new_position in board.safe_fields:
            # Musimy policzyć, ile pionków stoi na tym polu
            total_pawns = 0
            for pl in board.players:
                for opp_token in pl.tokens:
                    if opp_token == new_position:
                        total_pawns += 1

            if total_pawns >= 4:
                # Nie możemy wejść jako piąty pionek
                print(f"[DEBUG] Pole {new_position} jest już zajęte przez 4 pionki!")
                return f"Pionek {token_index} nie może wejść na to pole – jest już pełne (4 pionki)."

            # Inaczej – możemy wejść, ale nie zbijamy pionków
            # POMIJAMY zbijanie. Ustawiamy się normalnie:
            self.tokens[token_index] = new_position
            return f"Pionek {token_index} stanął na bezpiecznym polu {new_position}."

        # Sprawdź, czy na nowej pozycji są pionki innego gracza (lub wielu)
        for opponent in board.players:
            if opponent.color != self.color:  # Sprawdzanie tylko przeciwników
                zapped_count = 0
                for i, opponent_token in enumerate(opponent.tokens):
                    print(
                        f"[DEBUG] Sprawdzanie pionka gracza {opponent.color}: pionek {i} na pozycji {opponent_token}.")
                    if opponent_token == new_position:
                        # Cofnij pionek przeciwnika do schowka
                        opponent.tokens[i] = -1
                        zapped_count += 1

                if zapped_count > 0:
                    # Jeśli zbijamy wszystkie pionki przeciwnika, dopiero teraz
                    # ustawiamy swój pionek na to pole
                    self.tokens[token_index] = new_position

                    print(
                        f"[DEBUG] Gracz {self.color} – Pionek {token_index} zbił {zapped_count} pionków gracza {opponent.color} na polu {new_position}.")

                    # Komunikat zależny od liczby zbitych pionków
                    if zapped_count == 1:
                        return f"Pionek {token_index} zbił pionek gracza {opponent.color}!"
                    else:
                        return f"Pionek {token_index} zbił {zapped_count} pionki gracza {opponent.color}!"

        # Jeśli nie zbiliśmy żadnego pionka, normalnie aktualizujemy pozycję
        self.tokens[token_index] = new_position
        return f"Pionek {token_index} przesunął się na pole {new_position}"

    def is_finished(self):
        """Sprawdź, czy gracz zakończył grę."""
        return self.finished_tokens == 4




