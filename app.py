from flask import Flask, render_template, request, jsonify
from game_logic.game import Game

app = Flask(__name__)

# Inicjalizacja gry dla czterech graczy
game = Game(["red", "blue", "green", "yellow"])

# Trasa gry (obsługuje GET i POST)
@app.route('/game', methods=['GET', 'POST'])
def game_view():
    if request.method == 'GET':
        # Pobieranie stanu gry i renderowanie strony
        state = game.get_game_state()
        return render_template('game.html', state=state)
    elif request.method == 'POST':
        # Tymczasowa obsługa POST
        return "POST nie jest obecnie obsługiwane", 405

# Strona startowa
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
