
class Player:
    def __init__(self, color):
        self.color = color
        self.tokens = [-1, -1, -1, -1]  # Pionki (-1 oznacza, że są w schowku)
        self.finished_tokens = 0  # Liczba pionków w domku

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

        # Sprawdź, czy na nowej pozycji jest pionek innego gracza
        for opponent in board.players:
            if opponent.color != self.color:  # Sprawdzanie przeciwników
                for i, opponent_token in enumerate(opponent.tokens):
                    print(
                        f"[DEBUG] Sprawdzanie pionka gracza {opponent.color}: pionek {i} na pozycji {opponent_token}.")
                    if opponent_token == new_position:  # Jeśli na tej samej pozycji co obecny pionek
                        opponent.tokens[i] = -1  # Cofnij pionek przeciwnika do schowka
                        print(
                            f"[DEBUG] Gracz {self.color} – Pionek {token_index} zbił pionek gracza {opponent.color} na polu {new_position}.")
                        self.tokens[token_index] = new_position
                        return f"Pionek {token_index} zbił pionek gracza {opponent.color}!"

        # Aktualizacja pozycji pionka
        self.tokens[token_index] = new_position
        return f"Pionek {token_index} przesunął się na pole {new_position}"


    def is_finished(self):
        """Sprawdź, czy gracz zakończył grę."""
        return self.finished_tokens == 4




