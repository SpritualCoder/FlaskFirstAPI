from flask import Flask, jsonify, request
from mongoengine import Document, StringField, IntField, EmailField, connect

app = Flask(__name__)

# MongoDB Atlas URI - replace with your connection string
# replace <password> with ur mongodb atlas password 
app.config["MONGO_URI"] = "mongodb+srv://adityarajmathur2005:<password>@students.awnqtqu.mongodb.net/?retryWrites=true&w=majority&appName=Students"

connect(host=app.config["MONGO_URI"], db="students_db")

# Define the Student model
class Student(Document):
    name = StringField(required=True, max_length=100)
    usn = StringField(required=True, unique=True, max_length=20)
    age = IntField(required=True, min_value=0)
    email = EmailField(required=True, unique=True)
    phno = StringField(required=True, max_length=15)
    ip_address = StringField()
    password = StringField(required=True)
    
    meta = {
        'collection': 'students'
    }

@app.route('/')
def home():
    return "Flask API with MongoDB Atlas", 200

# Function to add a student
@app.route('/student', methods=['POST'])
def add_student():
    data = request.json
    try:
        student = Student(
            name=data['name'],
            usn=data['usn'],
            age=data['age'],
            email=data['email'],
            phno=data['phno'],
            ip_address=data['ip_address'],
            password=data['password']
        )
        student.save()
        return jsonify(student.to_json()), 201
    except Exception as e:
        return str(e), 400

# Function to delete a student by usn number
@app.route('/student/<usn>', methods=['DELETE'])
def delete_student(usn):
    try:
        student = Student.objects(usn=usn).first()
        if student:
            student.delete()
            return '', 204
        return 'Student not found', 404
    except Exception as e:
        return str(e), 400

# Function to update a student's information by usn number
@app.route('/student/<usn>', methods=['PUT'])
def update_student(usn):
    data = request.get_json()
    try:
        student = Student.objects(usn=usn).first()
        if student:
            student.update(**data)
            return jsonify(student.to_json()), 200
        return 'Student not found', 404
    except Exception as e:
        return str(e), 400

if __name__ == '__main__':
    app.run(debug=True)
