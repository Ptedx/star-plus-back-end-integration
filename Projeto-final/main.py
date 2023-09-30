import pickle
import bcrypt
from flask import Flask, request, render_template, redirect
from sqlalchemy import create_engine, Integer, Column, String, inspect
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
def checarBd(consulta):
    exist = session.query(registro).filter_by(email=consulta).first()
    return exist

def loadSalt():
    with open ('Projeto-final\salt.pikle', 'rb') as file:
        salt =pickle.load(file)
    return salt

def verify_password(hashed_password, password):
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)

Base = declarative_base()
app = (Flask(__name__, template_folder='templates', static_folder='static'))

connection = create_engine('mysql+mysqlconnector://root:@localhost/registro')
Session = sessionmaker(bind=connection)
session = Session()

class registro(Base):
    __tablename__ = 'registros'

    id = Column(Integer, autoincrement=True, primary_key=True)
    email = Column(String(255))
    senha = Column(String(255))

if not inspect(connection).has_table(registro.__tablename__):
    Base.metadata.create_all(bind=connection)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login')
def logar():
    return render_template('login.html')

@app.route('/check', methods=['POST'])
def check():
    if request.method == 'POST':
        exist = checarBd(request.form['email'])
        if exist:
            if verify_password(exist.senha.encode('UTF-8'),request.form['senha']):
                return redirect('login_success')
            else:
                return redirect('error')
        else:
            return redirect('error_login')
    
@app.route('/login_success')
def login_passar():
    return render_template('login_success.html')
@app.route('/error_login')
def rejeitar_login():
    return render_template('error_login.html')

@app.route('/error_register')
def rejeitar_register():
    return render_template('error_register.html')

@app.route('/register')
def entrar_registro():
    return render_template('register.html')

@app.route('/error')
def rejeitar():
    return render_template('error.html')

@app.route('/registrar', methods=['POST'])
def registrar():
    if request.method == 'POST':
        exist = checarBd(request.form['email'])
        if not exist:
            senha_encode = bcrypt.hashpw(request.form['senha'].encode('UTF-8'), loadSalt())
            novo_registro = registro(email=request.form['email'], senha=senha_encode)
            session.add(novo_registro)
            session.commit()
            return redirect('register_success')
        else:
            return redirect('error_register')

@app.route('/register_success')
def register_passar():
    return render_template('register_success.html')

app.run(host='localhost', port='5500', debug=True)