from flask import Flask, render_template, request, jsonify
from game_logic.game import Game

app = Flask(__name__)

# Inicjalizacja gry dla czterech graczy
game = Game(["red", "blue", "green", "yellow"])

# Trasa gry (obsługuje GET i POST)
@app.route('/game', methods=['GET', 'POST'])
def game_view():
    global game
    if request.method == 'POST':
        mode = request.form.get('mode')  # Tryb gry
        players_count = int(request.form.get('players', 4))  # Domyślnie 4 graczy

        # Kolory graczy (ustalamy maksymalnie 4 kolory)
        all_colors = ["red", "blue", "green", "yellow"]
        player_colors = all_colors[:players_count]  # Wybieramy tyle kolorów, ilu graczy

        # Inicjalizujemy grę
        game = Game(player_colors)
        game.mode = mode  # Przechowujemy tryb gry w obiekcie gry
        state = game.get_game_state()
        return render_template('game.html', state=state)

    elif request.method == 'GET':
        if game is None:
            return "Gra jeszcze się nie rozpoczęła!", 400
        state = game.get_game_state()
        return render_template('game.html', state=state)


# Strona startowa
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
