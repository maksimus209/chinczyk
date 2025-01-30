class Board:
    def __init__(self):
        # Pola planszy jako lista (0–39: zwykłe pola)
        self.fields = [None] * 40  # Pola główne (zwykłe)

        # Pola startowe dla każdego gracza
        self.start_fields = {
            "red": 0,       # Pole startowe gracza czerwonego
            "blue": 10,     # Pole startowe gracza niebieskiego
            "green": 20,    # Pole startowe gracza zielonego
            "yellow": 30    # Pole startowe gracza żółtego
        }

        # Ostatnie pole przed polem startowym
        self.max_positions = {
            "red": 39,      # Maksymalne pole dla gracza czerwonego
            "blue": 9,      # Maksymalne pole dla gracza niebieskiego
            "green": 19,    # Maksymalne pole dla gracza zielonego
            "yellow": 29    # Maksymalne pole dla gracza żółtego
        }

        # Domki dla każdego gracza
        self.homes = {
            "red": [40, 41, 42, 43],
            "blue": [44, 45, 46, 47],
            "green": [48, 49, 50, 51],
            "yellow": [52, 53, 54, 55]
        }

        # Pola domków są strefami bezpiecznymi
        self.safe_zones = self.homes

        self.death_fields = {
            "red": [1, 38],
            "blue": [11, 8],
            "green": [21, 18],
            "yellow": [31, 28]
        }

        self.safe_fields = [5, 15, 25, 35]

    def is_safe_field(self, position):
        """Sprawdź, czy pole jest bezpieczne (należy do domku)."""
        for home_fields in self.homes.values():
            if position in home_fields:
                return True
        return False

    def move(self, current_position, steps):
        """
        Przesunięcie pionka o zadaną liczbę kroków.
        Obsługuje cykliczne przejście po planszy (0–39).
        """
        new_position = (current_position + steps) % 40  # Ruch po planszy w pętli
        return new_position
