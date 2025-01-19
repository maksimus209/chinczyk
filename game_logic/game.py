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
    print("\n--- Test gry dla czterech graczy ---")
    game = Game(["red", "blue", "green", "yellow"])

    # Wyprowadzenie pionków przez wszystkich graczy
    game.players[0].tokens[0] = -1  # Red
    game.players[1].tokens[0] = -1  # Blue
    game.players[2].tokens[0] = -1  # Green
    game.players[3].tokens[0] = -1  # Yellow

    # Symulacja kilku rund
    for turn in range(1, 10):
        print(f"Tura {turn}: Gracz {game.players[game.current_player_index].color}")
        game.dice_value = 6 if turn <= 4 else (turn % 6 + 1)  # 6 dla początkowych tur, później zmienne wartości
        token_index = 0
        result = game.play_turn(token_index)
        print(result)
        print("Stan gry:", game.get_game_state())

    # Zakończenie testu
    print("Test gry dla czterech graczy zakończony.")








