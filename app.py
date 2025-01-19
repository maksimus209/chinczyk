from flask import Flask, render_template, request, jsonify
from game_logic.game import Game

app = Flask(__name__)

# Inicjalizacja gry dla czterech graczy
game = Game(["red", "blue", "green", "yellow"])

# Trasa gry (obsługuje GET i POST)
@app.route('/game', methods=['GET', 'POST'])
def game_view():
    if request.method == 'POST':
        try:
            data = request.get_json()  # Pobierz dane JSON
            token_index = int(data.get('token_index', 0))  # Wyciągnij 'token_index'
            result = game.play_turn(token_index)  # Wykonaj ruch
            state = game.get_game_state()  # Pobierz aktualny stan gry
            return jsonify({"message": result, "state": state})  # Zwróć wynik i stan gry
        except Exception as e:
            return jsonify({"error": str(e)}), 400  # Obsłuż błędy

    # Obsługa metody GET - wyświetlenie początkowego stanu gry
    state = game.get_game_state()
    return render_template('game.html', state=state)


# Strona startowa
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
