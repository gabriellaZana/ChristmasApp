import pwhash
import dbhandler
import queries
from flask import Flask, render_template, redirect, url_for, request, session, json, jsonify

app = Flask(__name__)

app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'


@app.route("/boards")
def boards():
    if session:
        user_id = session['id']
        user_name = session['user']
        return render_template('boards.html', user_id=user_id, user_name=user_name )
    else:
        return redirect(url_for('login'))


@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = pwhash.hash_password(request.form['password'])
        user_database = dbhandler.query_select('SELECT * FROM users WHERE user_name = %s AND password = %s', (username, password))
        if user_database:
            session_info = user_database[0]
            session['user'] = session_info['user_name']
            session['id'] = session_info['id']
            return redirect(url_for('boards'))
        else:
            return redirect(url_for('login'))
    return render_template('login.html')


@app.route('/registration', methods=['GET', 'POST'])
def registration():
    if request.method == 'POST':
        username = request.form['username']
        password = pwhash.hash_password(request.form['password'])
        dbhandler.query_modify('INSERT INTO users (user_name, password) VALUES (%s, %s)', (username, password))
        return redirect('/')
    return render_template('register.html')


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


# Ajax routes

@app.route('/get_data')
def get_boards():
    data = {'states': [
        {
            "id": 1,
            "name": "New"
        },
        {
            "id": 2,
            "name": "In progress"
        },
        {
            "id": 3,
            "name": "Testing"
        },
        {
            "id": 4,
            "name": "Done"
        }
        ], 'boards': queries.get_boards(), 'cards': queries.get_cards()}
    return jsonify(data)


@app.route('/save_data', methods=['POST'])
def save_data():
    boards = request.json['boards']
    cards = request.json['cards']
    print(boards)
    print(cards)
    queries.clear_cards()
    queries.clear_boards()
    for board in boards:
        queries.save_boards(board['title'], board['user_id'], '1')
    for card in cards:
        queries.save_cards(card['title'], card['board_id'], card['status_id'], card['order_id'])
    return jsonify(boards)


@app.route('/delete-card/', methods=['POST'])
def delete_card():
    id_ = request.json['cardId']
    queries.delete_card(id_)    
    return jsonify(id_)


@app.route('/delete-boards/<board_id>')
def delete_board(board_id):
    queries.delete_boards(board_id)
    return redirect("/boards")


def main():
    app.run(debug=True)

if __name__ == '__main__':
    main()
