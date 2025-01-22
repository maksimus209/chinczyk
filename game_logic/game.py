from game_logic.board import Board
from game_logic.player import Player

import random

class Game:
    def __init__(self, player_colors):
        self.board = Board()
        self.players = [Player(color) for color in player_colors]
        self.current_player_index = 0  # Gracz, który ma aktualnie turę
        self.dice_value = 0  # Wynik rzutu kostką
        self.turn_number = 1  # Numer tury
        self.board.players = self.players
        self.rolls_left = 0  # <-- NOWE: liczba rzutów pozostałych w tej turze

    def roll_dice(self):
        """
        Rzut kostką z uwzględnieniem:
          - 3 prób, jeśli wszystkie pionki są w bazie
          - możliwości kolejnego rzutu, gdy wypadnie 6
          - brak 'next_player()' przy wyrzuceniu <6 i nie-wszystkie w bazie
            (to robimy w play_turn)
        """
        current_player = self.players[self.current_player_index]
        all_in_base = all(token == -1 for token in current_player.tokens)

        # Jeśli zaczyna się nowa tura (rolls_left == 0),
        # ustalamy, ile rzutów przysługuje
        if self.rolls_left == 0:
            if all_in_base:
                # Gracz ma trzy próby na wyrzucenie 6
                self.rolls_left = 3
            else:
                # Gracz ma 1 rzut, dopóki nie wypadnie 6 (obsłużymy to w play_turn)
                self.rolls_left = 1

        # Wykonujemy rzut
        self.dice_value = random.randint(1, 6)
        message = f"Wylosowano {self.dice_value}."

        # 1. Gdy wszystkie pionki są w bazie i nie wypadło 6
        if all_in_base and self.dice_value != 6:
            self.rolls_left -= 1  # zużywamy 1 rzut
            if self.rolls_left > 0:
                # Są jeszcze próby
                message = "Nie możesz wyprowadzić pionka z domu, rzuć jeszcze raz."
            else:
                # Trzecia próba nieudana -> next_player()
                self.next_player()
                message = (
                    "Nie możesz wyprowadzić pionka z domu, kolejka przechodzi do "
                    f"następnego gracza: {self.players[self.current_player_index].color}"
                )
                self.rolls_left = 0

        # 2. Obsługa wypadnięcia 6
        elif self.dice_value == 6:
            # Jeśli NIE wszystkie pionki w bazie
            if not all_in_base:
                # Pozostawiamy graczowi prawo do kolejnego rzutu (1 rzut)
                # (Zależnie od preferencji, można dać 2, ale zwykle wystarczy 1,
                # bo za każdym razem, gdy wypadnie 6, logika w play_turn
                # i tak nie zmienia gracza.)
                self.rolls_left = 1

            message = (
                f"Gracz {current_player.color} wylosował 6 – "
                "proszę wybrać pionek lub rzuć kostką ponownie."
            )

        # 3. W pozostałych przypadkach (dice < 6 i not all_in_base)
        #    - NIE kończymy tury tu! Zrobimy to w play_turn().
        #    - Dlatego brak next_player().
        return self.dice_value, message

    def next_player(self):
        """Przejście do następnego gracza."""
        self.current_player_index = (self.current_player_index + 1) % len(self.players)
        if self.current_player_index == 0:  # Zwiększ numer tury, gdy wracamy do pierwszego gracza
            self.turn_number += 1

    def play_turn(self, token_index):
        """
        Wykonanie tury gracza z wykorzystaniem self.dice_value
        (ustawionego wcześniej przez roll_dice()).
        """
        player = self.players[self.current_player_index]
        dice = self.dice_value  # Kostka została wylosowana w roll_dice()

        result = player.move_token(token_index, dice, self.board)

        # Sprawdź, czy gracz wygrał (wszystkie pionki w domku)
        if player.is_finished():
            return f"Gracz {player.color} wygrał grę!"

        # Jeśli ruch był niemożliwy (np. "nie może opuścić schowka" bez 6),
        # przechodzimy do następnego gracza.
        if "nie może wykonać ruchu" in result or "nie może opuścić schowka" in result:
            self.next_player()
            return f"Gracz {player.color}: {result}. Tura przechodzi na kolejnego gracza."

        # Jeśli wyrzucił 6, tura trwa – gracz może wykonać kolejny rzut.
        if dice == 6:
            return f"Gracz {player.color}: {result}. Wyrzucono 6 – gracz rzuca ponownie."

        # W przeciwnym wypadku (dice < 6), kończymy turę i przechodzimy do kolejnego gracza
        self.next_player()
        return f"Gracz {player.color}: {result}"

    def choose_computer_move(self, player):
        """Prosta logika AI dla ruchu komputera."""
        for i, token in enumerate(player.tokens):
            if token == -1 and self.dice_value == 6:  # Wyprowadzenie pionka
                return i
            elif token >= 0:  # Wybór pionka na planszy
                return i
        return 0  # Domyślnie wybierz pierwszy pionek

    def get_game_state(self):
        """Pobierz aktualny stan gry."""
        return {
            "current_player": self.players[self.current_player_index].color,
            "dice_value": self.dice_value,
            "turn_number": self.turn_number,  # Dodaj numer tury do stanu gry
            "players": [
                {
                    "color": player.color,
                    "tokens": player.tokens,
                    "finished_tokens": player.finished_tokens,
                }
                for player in self.players
            ],
        }


if __name__ == "__main__":
    print("\n--- Test dwóch czerwonych pionków wprowadzanych do domku ---")
    game = Game(["red", "blue"])

    # Ustawienie pozycji: pierwszy pionek czerwony na pozycji 39, drugi na pozycji 37
    game.players[0].tokens[0] = 39  # Pionek 0 (czerwony) na polu 39
    game.players[0].tokens[1] = 37  # Pionek 1 (czerwony) na polu 37

    # Symulacja wprowadzenia pierwszego pionka (potrzebuje wyrzucić 4)
    game.dice_value = 4
    result = game.play_turn(0)  # Ruch pionka 0 (czerwony)
    print(result)
    print("Stan gry po ruchu pierwszego pionka:", game.get_game_state())

    # Symulacja wprowadzenia drugiego pionka (potrzebuje wyrzucić 2, bo jest na pozycji 37)
    game.dice_value = 2
    result = game.play_turn(1)  # Ruch pionka 1 (czerwony)
    print(result)
    print("Stan gry po ruchu drugiego pionka:", game.get_game_state())

    # Próba ponownego ruchu (dla potwierdzenia, że pionki są w domku i nie mogą już się poruszać)
    game.dice_value = 3
    result = game.play_turn(0)  # Próba ruchu dla pierwszego pionka
    print(result)

    game.dice_value = 3
    result = game.play_turn(1)  # Próba ruchu dla drugiego pionka
    print(result)













