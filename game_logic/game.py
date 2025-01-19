from game_logic.board import Board
from game_logic.player import Player

import random

class Game:
    def __init__(self, player_colors):
        self.board = Board()
        self.players = [Player(color) for color in player_colors]
        self.current_player_index = 0  # Gracz, który ma aktualnie turę
        self.dice_value = 0  # Wynik rzutu kostką
        self.board.players = self.players

    def roll_dice(self):
        """Rzut kostką i zwrócenie wyniku."""
        self.dice_value = random.randint(1, 6)
        return self.dice_value

    def next_player(self):
        """Przejście do następnego gracza."""
        self.current_player_index = (self.current_player_index + 1) % len(self.players)

    def play_turn(self, token_index):
        """Wykonanie tury gracza."""
        player = self.players[self.current_player_index]
        dice = self.roll_dice()
        result = player.move_token(token_index, dice, self.board)

        # Sprawdź, czy gracz wygrał
        if player.is_finished():
            return f"Gracz {player.color} wygrał grę!"

        # Jeśli ruch był niemożliwy, tura przepada
        if "nie może wykonać ruchu" in result or "nie może opuścić schowka" in result:
            self.next_player()
            return f"Gracz {player.color}: {result}. Tura przechodzi na kolejnego gracza."

        # Jeśli gracz wyrzucił 6, ma dodatkowy ruch
        if dice == 6:
            return f"Gracz {player.color}: {result}. Wyrzucono 6 – gracz rzuca ponownie."

        # Przejście do kolejnego gracza
        self.next_player()
        return f"Gracz {player.color}: {result}"

    def get_game_state(self):
        """Pobierz aktualny stan gry."""
        return {
            "current_player": self.players[self.current_player_index].color,
            "dice_value": self.dice_value,
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













