from flask import Flask, render_template, request, redirect, url_for,session
from flask_pymongo import PyMongo
import pymongo

app = Flask(__name__)

app.secret_key = "TeamoDios123"

myClient = pymongo.MongoClient("mongodb://admin:keajse21*@54.237.158.84:27017")

myDb = myClient["reservationapp"] #Database
myCollection = myDb["reservation"] #Collection

#app.config["MONGO_URI"] = "mongodb://admin:keajse21*@54.237.158.84:27017/reservationapp"
#mongo = PyMongo(app)

@app.route('/prueba') #decorador
def hello_world():
    return render_template("index.html", people=[{"name": "Kea","age":33},{"name": "Adriana","age":35},{"name": "Omar","age":34}])

@app.route('/formulario') #decorador
def formulario():
    return render_template('formulario.html', )

@app.route('/home') #decorador
def home():
    return render_template('galeria.html')


@app.route('/')
def index():
    return render_template('login.html')

@app.route('/login', methods=["POST"])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        rol = request.form['rol']      
        session['username']= email
        session['rol']= rol
        return redirect(url_for('products'))
    else:
        return "bad request"


@app.route('/products')
def products():
    if 'username' in session and session['rol'] == 'admin':
        return render_template('products.html')
    else:
        return redirect(url_for('index'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))



if __name__ == "__main__":
    app.run(debug=True)



