from flask import Flask, render_template, request, url_for, redirect, flash, send_from_directory
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user

app = Flask(__name__)

app.config['SECRET_KEY'] = '0f01f3b4733d44837234f64dd0757a7f'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


##CREATE TABLE IN DB
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))


# Line below only required once, when creating DB.
# db.create_all()


@app.route('/')
def home():
    return render_template("index.html")


@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        new_user = User(name=request.form.get('name'),
                        email=request.form.get('email'),
                        password=request.form.get('password'))
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('secrets', username=request.form.get('name')))
    return render_template("register.html")


@app.route("/download", methods=["GET", "POST"])
def download():
    return send_from_directory('static/files', 'cheat_sheet.pdf')


@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')
        check_user = db.session.query(User).filter(User.email == email).first()
        if check_user:
            if check_user.password == password:
                return redirect(url_for('secrets', username=check_user.name))
    return render_template("login.html")


@app.route('/secrets')
def secrets():
    name = request.args['username']
    return render_template("secrets.html", username=name)


@app.route('/logout')
def logout():
    pass


if __name__ == "__main__":
    app.run(debug=True)