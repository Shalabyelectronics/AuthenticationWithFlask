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
login_manager.login_view = "login"


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
    if current_user.is_authenticated:
        return redirect(url_for("secrets"))
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
            return redirect(url_for('secrets'))
    return render_template("register.html")


@app.route("/download", methods=["GET", "POST"])
@login_required
def download():
    return send_from_directory('static/files', 'cheat_sheet.pdf')


global next_page


@app.route('/login', methods=["GET", "POST"])
def login():
    global next_page
    if current_user.is_authenticated:
        return redirect(url_for("secrets"))
    if request.method == "GET":
        next_page = request.args.get("next")
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                login_user(user)
                return redirect(next_page) if next_page else redirect(url_for('secrets'))
            else:
                flash("Login unsuccessful. please check password", "danger")
        else:
            flash("Login unsuccessful. please check email", "danger")
    return render_template("login.html")


@app.route('/secrets')
@login_required
def secrets():
    return render_template("secrets.html")


@app.route('/account')
@login_required
def account():
    return render_template("account.html")


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)
