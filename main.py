from flask import Flask, render_template, request, url_for, redirect, flash, send_from_directory
from werkzeug.security import generate_password_hash, check_password_hash
import secrets
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user

app = Flask(__name__)

app.config['SECRET_KEY'] = secrets.token_hex(16)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
login_manager = LoginManager(app)


##CREATE TABLE IN DB
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))


# Line below only required once, when creating DB.
# db.create_all()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/')
def home():
    return render_template("index.html")


@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        check_user_by_email = User.query.filter_by(email=request.form.get('email')).first()
        if check_user_by_email:
            flash("This email is already taken, or you can ")
        else:
            new_user = User(name=request.form.get('name'),
                            email=request.form.get('email'),
                            password=generate_password_hash(request.form.get('password'), "pbkdf2:sha256", 8))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user)
            load_user(new_user.id)
            return redirect(url_for('secrets'))
    return render_template("register.html")


@app.route("/download", methods=["GET", "POST"])
def download():
    return send_from_directory('static/files', 'cheat_sheet.pdf')


@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('secrets'))
        flash("Login unsuccessful. please check email and password", "danger")
    return render_template("login.html")


@app.route('/secrets', methods=["GET", "POST"])
def secrets():
    return render_template("secrets.html")


@app.route('/logout')
def logout():
    pass


if __name__ == "__main__":
    app.run(debug=True)
