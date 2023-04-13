from flask import Flask,request,jsonify
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash,check_password_hash

app = Flask(__name__)
app.config['MONGO_DBNAME'] = 'test'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/APIREST'

mongo = PyMongo(app)

@app.route('/users', methods=['POST'])
def create_user():
    username = request.json['username']
    password = request.json['password']
    email = request.json['email']

    if username and email and password:
        has_password = generate_password_hash(password)
        id = mongo.db.users.insert_one(
                {'username': username,'email': email,'password': has_password}
        ).inserted_id
        response = {
            'id': str(id),
            'username': username,
            'password': has_password,
            'email' : email
        }
        return response
    else:
        response = {'message':'llenar todos los campos por favor'}
        return response
    
@app.route('/producto', methods=['POST'])
def create_producto():
    producto = request.json['producto']
    precio = request.json['precio']
    catalogo = request.json['catalogo']
    stop = request.json['stop']

    if producto and precio and catalogo and stop:
        id = mongo.db.producto.insert_one(
                {'producto': producto,'precio': precio,'catalogo': catalogo, 'stop': stop}
        ).inserted_id
        response = {
            'id': str(id),
            'producto': producto,
            'precio': precio,
            'catalogo' : catalogo,
            'stop' : stop
        }
        return response
    else:
        response = {'message':'llenar todos los campos por favor'}
        return response

@app.errorhandler(404)
def not_found(error = None):
    response = jsonify({
        'message': 'Resourse Not Found: '+ request.url,
        'status' : 404
    })
    response.status_code = 404
    return response


if __name__ == "__main__":
    app.run(debug=True)