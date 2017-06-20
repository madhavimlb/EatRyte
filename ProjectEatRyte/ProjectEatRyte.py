from flask import Flask, render_template,request

app = Flask(__name__)


@app.route('/')
def static_page():
    return render_template('index.html')

if __name__ == '__main__':
    app.debug = True
    app.run()


app = Flask(__name__)
mysql = MySQL(app)


@app.route('/')
def users():
    cur = mysql.connection.cursor()
    cur.execute('''SELECT user, host FROM mysql.user''')
    rv = cur.fetchall()
    return str(rv)

