from flask import Flask, render_template, request, redirect, url_for,session
from flask_pymongo import PyMongo, ObjectId
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

@app.route('/reservations', methods=['POST'])
def createReservation():
    if request.method == 'POST':
    #print(request.json)
        myReservation ={
            'name': request.form['firstName'],
            'lastname': request.form['lastName'],
            'email': request.form['email'],
            'password': request.form['password'],
            'username': request.form['username'],
            'country': request.form['country'],
            'city': request.form['city'],
            'role': request.form['rol']

        }
        
        result = myCollection.insert_one(myReservation)
        print(result)      
        return redirect(url_for('index'))
    else:
        return "bad request"

@app.route('/readAllData', methods=['GET'])
def readAllData():
    result = myCollection.find() #SELECT * FROM table_name
    for document in result:  
        #print(document)  
        print(document)      
    #return jsonify(result)

#readAllData()

@app.route('/findById/<_id>', methods=['GET'])
def findById():
    query = {"_id": ObjectId("60af18403cb99910fe698593")}
    result = myCollection.find_one(query)
    print(result)
    return (result)

#findById()

#findById@app.route('/update' , methods=['PUT'])
def updateData():
    query = {"_id": ObjectId("60b1701f92331894089be768")}
    newValues = {"$set":{"name": "Maria Teresa", "lastname": "Gomez", "email": "mariaca@gmail.com", "password": "MiDiosymitodo", "username": "mariaca"}} #El set es obligatorio.
    myCollection.update_one(query, newValues)
    print("Registro actualizado")

#updateData()

def deleteData():
    query = {"_id": ObjectId("60b1701f92331894089be768")}
    myCollection.delete_one(query)
    print("Registro borrado")

deleteData()

if __name__ == "__main__":
    app.run(debug=True)