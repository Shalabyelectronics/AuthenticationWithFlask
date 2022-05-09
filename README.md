# Authentication With Flask
Here with this project we are going to learn Authentication with Flask So have Fun.

## Project overview

![project_overview](https://user-images.githubusercontent.com/57592040/167265729-29c3fd07-41f9-49d3-ac2f-8808c427a780.gif)

In this overview we can see how we login , register and logout and how the user need to be login to get to the secret page and download the pdf file as well, plus how the home page changed as current user is already login or logout.

**What we will discuss with this project?**

1. secure your users passwords by using `werkzeug.security` tools 
2. Manage user session by using `flask_login`  extension.
3. update the pages if the current user is authenticated.

**I will not discuss adding adding and styling web pages templates or flask starter configurations, so lets began.**

#### secure your users passwords by using `werkzeug.security` tools 

In sample way we need to save our users passwords encrypted in our database instead of saving them as plan text so if our database stolen by bad guys at least the need ages to decrypting our users passwords and to do so we are going to use `generate_password_hash` function from `werkzeug.security` library 

The concept about encrypting passwords or secret messages called Cryptography and it come from a Greece and it mean hidden writing if you like to know more about the history of Cryptography I recommend you to watch this video:

[![IMAGE ALT TEXT HERE](https://1do0x210e15c8plg913c4zhy-wpengine.netdna-ssl.com/wp-content/uploads/cryptography-scaled-e1593335036543.jpg)](https://youtu.be/jhXCTbFnK8o)

So to encrypt our users passwords we need to add this line of code before send the password to our database 

`password=generate_password_hash(request.form.get('password'), "pbkdf2:sha256", 8))`

and our passwords will look like this:

![hashed_pass](https://user-images.githubusercontent.com/57592040/167366510-0012ac7d-553e-4515-a909-f34045510e16.png)

and to check back if the user password match when login we are going to use another method called 

```python
check_password_hash(user.password, request.form.get('password'))
```

for more information about werkzeug security generate_password_hash and more useful tools you can check it from [here](https://werkzeug.palletsprojects.com/en/1.0.x/utils/#werkzeug.security.generate_password_hash)

### Manage user session by using `flask_login`  extension.

Second part we are going to focus about is How to manage our users session in our flask web application?, Here flask-login extension comes to manage it for us and first step is to install it as well by pip:

```bash
$ pip install flask-login
```

Then import it and add it to your web application instance app

```python
from flask_login import LoginManager
login_manager = LoginManager(app)
```

The methods we are going to use from flask_login will be as below:

- UserMixin
- login_user
- login_required
- current_user
- logout_user

#### **What is UserMixin class?**

UserMixin it will add four different status as attributes to your user as below:

- is_uthentecated
- is_active
- is_anonumouse
- get_id

and UserMixin class should be inherited to the User class beside of Model class as below:

```python
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
```

#### **What is login_user method?**

login_user will create a session for the current user and edit the UserMixin Methods so it will get the user id by load_user function as below:

```python
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
```

and save it to get_id method, is_uthentecated will be True, is_active will be True, is_anonumouse will be False

and we need to add login_user method with login route and register route and pass user instance as argument to it.

Register Route, "/register" endpoint

```python
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
```

Login Route , "/login" endpoint

```python
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
```

#### **What is login_required method?**

login_required will block specific pages that have `@login_required` decorator so any unauthenticated user can not access any pages that need to be login to access them.

![login_restriction](https://user-images.githubusercontent.com/57592040/167367119-65f09def-7977-42d6-9a8a-bcb5fd34849e.gif)


I add login required decorator to **secrets**  and **account** routes as below:

```python
@app.route('/secrets')
@login_required
def secrets():
    return render_template("secrets.html")


@app.route('/account')
@login_required
def account():
    return render_template("account.html")
```
Also we can redirect the user to the page that tried to access before login by getting next key as below:
```py
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
```

#### **What is current_user instance ?**

current_user instance will use UserMixin attributes that we explained before and we will use is_authenticated attribute to check if the user is already authenticated  or not and it will help us to update our web page to change some options like if the user is authenticated  , the user won't see login or register button and will see logout button instead.



and inside the base.html page we need to add this functionality to preform the explained result as below:

```jinja2
{% if current_user.is_authenticated %}
            <li class="nav-item">
            <a class="nav-link" href="{{ url_for('account') }}">Account</a>
            </li>
            <li class="nav-item">
            <a class="nav-link" href="{{ url_for('logout') }}">Log Out</a>
            </li>
        {% else %}
          <li class="nav-item">
            <a class="nav-link" href="{{ url_for('login') }}">Login</a>
          </li>
            <li class="nav-item">
            <a class="nav-link" href="{{ url_for('register') }}">Register</a>
          </li>
        {% endif %}
    </ul>


  </div>
</nav>
       {% block content %}
       {% endblock %}
```

 and in our home page "/" endpoint

```jinja2
{% extends "base.html" %}
{% block content %}

<div class="box">
   <h1>Flask Authentication</h1>
{% if current_user.is_authenticated %}
    <a href="{{ url_for('secrets') }}" class="btn btn-primary btn-block btn-large">Secrets</a>
    <a href="{{ url_for('account') }}" class="btn btn-primary btn-block btn-large">Account</a>
{% else %}
  <a href="{{ url_for('login') }}" class="btn btn-primary btn-block btn-large">Login</a>
  <a href="{{ url_for('register') }}" class="btn btn-secondary btn-block btn-large">Register</a>
{% endif %}
</div>

{% endblock %}
```

#### Finally What is the logout_user?

It do what it called and that logout user and clear the session so we need to create a logout route and add it to the logout button as below:

```python
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for("home"))
```

#### Resources:

- This practice is part of [100 days of python code with Angela Yu](https://www.udemy.com/course/100-days-of-code) 
- [Python Flask Tutorial: Full-Featured Web App Part 6 - User Authentication](https://youtu.be/CSHx6eCkmv0) by Corey Schafer

