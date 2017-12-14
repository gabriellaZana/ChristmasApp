import dbhandler


def get_boards():
    return dbhandler.query_select('''SELECT * FROM boards''')


def get_cards():
    return dbhandler.query_select('''SELECT * FROM cards''')


def save_boards(title, user_id, is_active):
    dbhandler.query_modify('INSERT INTO boards (title, is_active, user_id) VALUES (%(title)s, %(isactive)s, %(userid)s);',
                           variables={'title': title, 'isactive': is_active, 'userid': user_id})



def save_cards(title, board_id, status_id, order_id):
    dbhandler.query_modify('INSERT INTO cards (title, board_id, status_id, order_id) VALUES (%(title)s, %(board)s, %(status)s, %(order)s);', 
                           variables={'title': title, 'board': board_id, 'status': status_id, 'order': order_id})


def clear_boards():
    dbhandler.query_modify('DELETE FROM boards; ALTER SEQUENCE boards_id_seq RESTART WITH 1;')


def clear_cards():
    dbhandler.query_modify('DELETE FROM cards; ALTER SEQUENCE cards_id_seq RESTART WITH 1;')


def delete_card(id_):
    dbhandler.query_modify('DELETE FROM cards WHERE id=%(id)s;', variables={'id': id_})

    
def delete_boards(board_id):
    dbhandler.query_modify('''DELETE FROM cards WHERE board_id=%(board_id)s;
                              DELETE FROM boards WHERE id=%(board_id)s;''', variables={'board_id': board_id})
