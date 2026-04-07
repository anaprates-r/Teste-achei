# configuração geral da aplicação
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os

#__________INITIALISATIONS____________________
app = Flask(__name__)

app.config['CORS_HEADERS'] = 'Content-Type'

CORS(
    app,
    resources={r"/*": {"origins": "*"}},
    supports_credentials=True
)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:Petsaude2026@db.ndkttgicirrqfaclpptq.supabase.co:5432/postgres"
#app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


ALLOWED_EXTENSIONS = {'xls','xlsx'}
app.config['UPLOAD_FOLDER'] ="/upload"  


db = SQLAlchemy(app)
