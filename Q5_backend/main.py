from flask import Flask, request, jsonify
import sqlite3
import os

from enc_utils import *
from db_utils import *
from country_codes import all_codes

app = Flask(__name__)
enc_key = None
enc_key_file = 'key'
db_file = 'creds.db'


def insert_dummy_data(db_file, enc_key):
    dummy_data = [
        ('galvin', 'sg', '123456'),
        ('rde', 'in', 'rdedev')
    ]

    dummy_data  = [
        (name, country_code, encrypt_passwd(passwd, enc_key))
        for name, country_code, passwd in dummy_data
    ]

    try:
        db_conn = sqlite3.connect(db_file)
        sql = """
        insert into login (name, country_code, passwd)
        values (?, ?, ?)
        """
        db_conn.executemany(sql, dummy_data)
        db_conn.commit()
        db_conn.close()
    except sqlite3.Error as e:
        return str(e)


def init_setup():
    create_db(db_file)
    create_enc_key(enc_key_file)
    create_table(db_file)
    insert_dummy_data(db_file, read_enc_key_file(enc_key_file))


def validate_user(login_id, login_passwd):
    provided_country_code = login_id[:2]
    if provided_country_code.upper() not in all_codes:
        return 'Wrong country code'

    
    db_entry = get_entry(db_file, login_id[2:])
    if len(db_entry) == 0:
        return 'User not found'

    db_entry = db_entry[0]
    encypted_passwd = db_entry[-1]
    decrypted_passwd = decrypt_passwd(encypted_passwd, enc_key)
    if login_passwd != decrypted_passwd:
        return 'Incorrect Password'
    
    return 'Authenticated'
    

@app.route('/validate', methods=['POST'])
def validation_endpoint():
    login_id = request.form['login_id']
    login_passwd = request.form['login_passwd']
    return jsonify({'Status': validate_user(login_id, login_passwd)})



if __name__ == '__main__':
    if (not os.path.isfile(db_file)) or (not os.path.isfile(enc_key_file)):
        init_setup()

    enc_key = read_enc_key_file(enc_key_file)
    app.run(debug=True)

    



