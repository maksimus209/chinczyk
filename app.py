from flask import Flask, render_template, request, jsonify
from game_logic.game import Game

app = Flask(__name__)

# Inicjalizacja gry dla czterech graczy
game = Game(["red", "blue", "green", "yellow"])


@app.route("/roll_dice", methods=["POST"])
def roll_dice():
    global game
    if game is None:
        return jsonify({"error": "Gra nie jest zainicjalizowana."}), 400

    # Rzucamy kostką
    dice_value = game.roll_dice()

    # Pobieramy aktualny stan gry
    state = game.get_game_state()

    # Zwracamy wynik w formacie JSON
    return jsonify({
        "dice_value": dice_value,
        "state": state
    })

@app.route("/move", methods=["POST"])
def move_token():
    global game
    if game is None:
        return jsonify({"error": "Gra nie jest zainicjalizowana."}), 400

    # Odczytujemy token_index z JSON
    data = request.get_json()
    if not data or "token_index" not in data:
        return jsonify({"error": "Brak token_index w żądaniu"}), 400

    token_index = int(data["token_index"])

    # Wywołujemy logikę gry
    result_message = game.play_turn(token_index)
    state = game.get_game_state()

    # Sprawdź, czy ktoś wygrał (opcjonalnie)
    game_over = False
    winner = None
    for p in game.players:
        if p.is_finished():
            game_over = True
            winner = p.color
            break

    return jsonify({
        "message": result_message,
        "state": state,
        "game_over": game_over,
        "winner": winner
    })


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
