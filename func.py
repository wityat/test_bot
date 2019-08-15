from database.database import Database


def chat_id_found(chat_id):
    db = Database()
    db.query("SELECT chat_id FROM profile WHERE chat_id = %s;", (chat_id, ))
    items = [item for item in db.data()]
    db.close()
    return True if len(items) > 0 else False

def chat_id_add(chat_id):
    db = Database()
    db.query("INSERT INTO profile (chat_id) VALUES (%s);", (chat_id, ))
    db.close()

def chat_id_del(chat_id):
    db = Database()
    db.query("DELETE FROM profile WHERE chat_id = %s;", (chat_id, ))
    db.close()

if __name__ == '__main__':
    chat_id_del(446162145)
    chat_id_del(385778185)
    # print(chat_id_found(1231))
    # print(chat_id_add(1231))
    # print(chat_id_found(1231))
    # print(chat_id_del(1231))
    # print(chat_id_found(1231))
