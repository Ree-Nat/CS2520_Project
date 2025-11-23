"""
NYT Games Clone - Flask Application
Main application entry point for the web-based game suite.
"""

from flask import Flask, render_template, request, session, jsonify, redirect, url_for
import sys
import os

# Add project root to path for imports
sys.path.insert(0, os.path.dirname(__file__))

from wordle.WordleController import WordleController

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')


# ==================== HOMEPAGE ====================

@app.route('/')
def index():
    """Render the homepage with available games."""
    return render_template('index.html')


# ==================== WORDLE GAME ====================

@app.route('/wordle')
def wordle():
    """Initialize or resume Wordle game session."""
    if 'wordle_controller' not in session:
        session['wordle_controller'] = None
    return render_template('wordle.html')


@app.route('/wordle/start', methods=['POST'])
def wordle_start():
    """Start a new Wordle game."""
    controller = WordleController()
    # Store game state in session (simplified for now)
    session['wordle_active'] = True
    session.modified = True
    return jsonify({'status': 'started'})


@app.route('/wordle/guess', methods=['POST'])
def wordle_guess():
    """
    Process a Wordle guess.
    Expects JSON: {'guess': 'apple'}
    Returns: game state with guess evaluation
    """
    data = request.get_json()
    guess = data.get('guess', '').lower()

    if not guess or len(guess) != 5:
        return jsonify({'error': 'Invalid guess length'}), 400

    # Initialize controller if needed
    if 'wordle_controller' not in session:
        session['wordle_controller'] = None

    # TODO: Implement proper session persistence for WordleController
    # For now, this demonstrates the API structure
    controller = WordleController()
    controller.onKeyPress(guess[0])
    controller.onKeyPress(guess[1])
    controller.onKeyPress(guess[2])
    controller.onKeyPress(guess[3])
    controller.onKeyPress(guess[4])
    controller.onKeyPress('ENTER')

    # Get game state
    guesses = controller.getGuesses()
    guess_count = controller.getGuessCount()
    is_won = controller.isWon()
    is_lost = controller.isLost()

    # Format response
    response = {
        'guess_count': guess_count,
        'is_won': is_won,
        'is_lost': is_lost,
        'guesses': [
            {
                'word': g.getGuess() if g else '',
                'evaluation': [g.getLetterEval(i) for i in range(5)] if g else []
            } for g in guesses
        ]
    }

    if is_won or is_lost:
        response['secret_word'] = controller.getSecretWord()

    return jsonify(response)


@app.route('/wordle/reset', methods=['POST'])
def wordle_reset():
    """Reset the Wordle game."""
    session.pop('wordle_controller', None)
    session['wordle_active'] = False
    session.modified = True
    return jsonify({'status': 'reset'})


# ==================== PLACEHOLDER ROUTES (for future games) ====================

@app.route('/spelling-bee')
def spelling_bee():
    """Spelling Bee game (to be implemented)."""
    return render_template('coming_soon.html', game='Spelling Bee')


@app.route('/tictactoe')
def tictactoe():
    """Tic-Tac-Toe game (to be implemented)."""
    return render_template('coming_soon.html', game='Tic-Tac-Toe')


# ==================== ERROR HANDLERS ====================

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    return render_template('500.html'), 500


# ==================== MAIN ====================

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)
