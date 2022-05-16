from flask import Flask, jsonify
from flask_restful import Api, Resource, reqparse, request, fields, marshal_with, marshal
from flask_sqlalchemy import SQLAlchemy
from werkzeug.exceptions import HTTPException
from werkzeug.exceptions import default_exceptions



app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)




@app.errorhandler(Exception)
def handle_error(e):
    code = 500
    if isinstance(e, HTTPException):
        code = e.code
    return jsonify(error=str(e)), code

for ex in default_exceptions:
    app.register_error_handler(ex, handle_error)


# Database Models

# User Model
class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    lastName = db.Column(db.String(20))
    firstName = db.Column(db.String(20))
    emails = db.relationship('Email', backref='user', lazy='select')    
    phoneNumbers = db.relationship('Phonenumber', backref='user', lazy='select')

    def __repr__(self):
        return 'Id: {}, last_name: {},firstName: {}'.format(self.id, self.lastName, self.firstName)


# Email model
class Email(db.Model):
    __tablename__ = 'email'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return 'Id: {}, email: {}'.format(self.id, self.email)


# Phonenumber Model
class Phonenumber(db.Model):
    __tablename__ = 'phonenumber'
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.String(10), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),nullable=False)
    
    def __repr__(self):
        return 'Id: {}, number: {}'.format(self.id, self.number)


db.create_all()

#### PhoneNumber Drivercode

# Serializing Objects
phonenumbers_fields = {
    'id': fields.Integer,
    
    'number': fields.String,
    'user_id': fields.Integer
}

phonenumbers_list_fields = {
    'count': fields.Integer,
    'number': fields.List(fields.Nested(phonenumbers_fields)),
}

# Argumnets parsing 
phonenumber_post_parser = reqparse.RequestParser()
phonenumber_post_parser.add_argument('number', type=str, required=True,  help='phonenumber parameter is required')
phonenumber_post_parser.add_argument('user_id', type=int, required=True,
                              help='user_id parameter is required')

# Class Phone Number                        
class PhonenumberResource(Resource):
    def get(self, number_id=None):
        if number_id:
            number = Phonenumber.query.filter_by(id=number_id).first()
            return marshal(number, phonenumbers_fields)
        else:
            args = request.args.to_dict()
         
            args.pop('limit', None)
            args.pop('offset', None)

            number = Phonenumber.query.filter_by(**args).order_by(Phonenumber.id)
           
            number = number.all()

            return marshal({
                'count': len(number),
                'number': [marshal(t, phonenumbers_fields) for t in number]
            }, phonenumbers_list_fields)

    @marshal_with(phonenumbers_fields)
    def post(self):
        args = phonenumber_post_parser.parse_args()

        number = Phonenumber(**args)
        db.session.add(number)
        db.session.commit()

        return number, 201

    @marshal_with(phonenumbers_fields)
    def put(self, number_id=None):
        Number = Phonenumber.query.get(number_id)

        if 'number' in request.form:
            Number.number = request.form['number']
            
        

        
        db.session.commit()
        return Number ,204

    @marshal_with(phonenumbers_fields)
    def delete(self, number_id=None):
        Number = Phonenumber.query.get(number_id)

        db.session.delete(Number)
        db.session.commit()

        return Number ,204



#### Email Drivercode

# Serializing Objects
email_fields = {
    'id': fields.Integer,
    'email': fields.String,
    
    'user_id': fields.Integer
}

email_list_fields = {
    'count': fields.Integer,
    'email': fields.List(fields.Nested(email_fields)),
}


# Argumnets parsing 
email_post_parser = reqparse.RequestParser()
email_post_parser.add_argument('email', type=str, required=True, 
                              help='email parameter is required')

email_post_parser.add_argument('user_id', type=int, required=True, 
                              help='user_id parameter is required')

# Class Email
class EmailsResource(Resource):
    def get(self, email_id=None):
        if email_id:
            email = Email.query.filter_by(id=email_id).first()
            return marshal(email, email_fields)
        else:
            args = request.args.to_dict()
           

            email = Email.query.filter_by(**args).order_by(Email.id)
            
            email = email.all()

            return marshal({
                'count': len(email),
                'email': [marshal(t, email_fields) for t in email]
            }, email_list_fields)

    @marshal_with(email_fields)
    def post(self):
        args = email_post_parser.parse_args()

        email = Email(**args)
        db.session.add(email)
        db.session.commit()

        return email, 201

    @marshal_with(email_fields)
    def put(self, email_id=None):
        email = Email.query.get(email_id)

        if 'email' in request.form:
            email.email = request.form['email']        

        db.session.commit()
        return email, 204

    @marshal_with(email_fields)
    def delete(self, email_id=None):
        email = Email.query.get(email_id)

        db.session.delete(email)
        db.session.commit()

        return email , 204


        
#### User Drivercode

# Serializing Objects
user_fields = {
    'id': fields.Integer,
    'lastName': fields.String,
    'firstName':fields.String,

    'emails': fields.List(fields.Nested({'id': fields.Integer,
                                        'email': fields.String,
                                        })),
    'phoneNumbers': fields.List(fields.Nested({'id': fields.Integer,
                                        'number': fields.String,
                                        })),
}

user_list_fields = {
    'count': fields.Integer,
    'users': fields.List(fields.Nested(user_fields)),
}


# Argumnets parsing 
user_post_parser = reqparse.RequestParser()

user_post_parser.add_argument('firstName', type=str, required=True, 
                              help='name parameter is required')
user_post_parser.add_argument('lastName', type=str, required=True, 
                              help='name parameter is required')


#User Class
class UsersResource(Resource):
    def get(self, user_id=None):
        if user_id:
            user = User.query.filter_by(id=user_id).first()
            return marshal(user, user_fields)
        else:
            args = request.args.to_dict()           

            user = User.query.filter_by(**args).order_by(User.id)          

            user = user.all()

            return marshal({
                'count': len(user),
                'users': [marshal(u, user_fields) for u in user]
            }, user_list_fields)

    @marshal_with(user_fields)
    def post(self):
        args = user_post_parser.parse_args()

        user = User(**args)
        db.session.add(user)
        db.session.commit()

        return user, 201

    @marshal_with(user_fields)
    def put(self, user_id=None):
        user = User.query.get(user_id)
        
        if 'firstName' in request.form:
            user.firstName = request.form['firstName']
        if 'lastName' in request.form:
            user.lastName = request.form['lastName']

        db.session.commit()
        return user, 204

    @marshal_with(user_fields)
    def delete(self, user_id=None):
        user = User.query.get(user_id)

        db.session.delete(user)
        db.session.commit()

        return user, 204



# Endpoints Routing
api.add_resource(UsersResource, '/users', '/users/<int:user_id>')
api.add_resource(EmailsResource, '/Email', '/Email/<int:email_id>')
api.add_resource(PhonenumberResource, '/PhoneNumber', '/PhoneNumber/<int:number_id>')


if __name__ == '__main__':
    app.run(debug=True)
