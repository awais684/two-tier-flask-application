import os
from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_mysqldb import MySQL

app = Flask(__name__)

# Configure MySQL from environment variables
app.config['MYSQL_HOST'] = os.environ.get('MYSQL_HOST', 'localhost')
app.config['MYSQL_USER'] = os.environ.get('MYSQL_USER', 'default_user')
app.config['MYSQL_PASSWORD'] = os.environ.get('MYSQL_PASSWORD', 'default_password')
app.config['MYSQL_DB'] = os.environ.get('MYSQL_DB', 'default_db')



# import boto3

# def get_ssm_parameter(name, with_decryption=True):
#     ssm = boto3.client('ssm', region_name='us-east-1')  # ✅ match your region
#     response = ssm.get_parameter(Name=name, WithDecryption=with_decryption)
#     return response['Parameter']['Value']

# # Fetch DB config from Parameter Store
# app.config['MYSQL_HOST'] = get_ssm_parameter('/myapp/db/MYSQL_HOST')
# app.config['MYSQL_USER'] = get_ssm_parameter('/myapp/db/MYSQL_USER')
# app.config['MYSQL_PASSWORD'] = get_ssm_parameter('/myapp/db/MYSQL_PASSWORD')
# app.config['MYSQL_DB'] = get_ssm_parameter('/myapp/db/MYSQL_DB')



# Initialize MySQL
mysql = MySQL(app)

def init_db():
    with app.app_context():
        cur = mysql.connection.cursor()
        cur.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id INT AUTO_INCREMENT PRIMARY KEY,
            message TEXT
        );
        ''')
        mysql.connection.commit()  
        cur.close()

@app.route('/')
def hello():
    cur = mysql.connection.cursor()
    cur.execute('SELECT message FROM messages')
    messages = cur.fetchall()
    cur.close()
    return render_template('index.html', messages=messages)

@app.route('/submit', methods=['POST'])
def submit():
    new_message = request.form.get('new_message')
    cur = mysql.connection.cursor()
    cur.execute('INSERT INTO messages (message) VALUES (%s)', [new_message])
    mysql.connection.commit()
    cur.close()
    return jsonify({'message': new_message})

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=True)

