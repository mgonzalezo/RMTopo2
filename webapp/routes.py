from flask import render_template,url_for, flash, redirect, request
from webapp import app, db, bcrypt
from webapp.forms import LoginForm, RegistrationForm, UpdateAccountForm
from webapp.models import User,Post
from flask_login import login_user, current_user, logout_user, login_required

posts = [
    {
        'author' : 'PS Core',
        'title' : 'First Topology',
        'content': 'First Post Content',
        'date_posted': 'April 20, 2018'
    },
    {
        'author' : 'IMS',
        'title' : 'Second Topology',
        'content': 'Second Post Content',
        'date_posted': 'April 21, 2018'
    }


]

@app.route("/")
@app.route("/home")
def home():
    # name = request.args.get("name", "World")
    # return f'Hello, {escape(name)}!'
    return render_template('home.html', posts= posts)


@app.route("/about")
def about():
    return render_template('about.html', title = 'About')

@app.route("/register", methods =['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username= form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f' Your account {form.username.data} has been created! You are now able to log in', 'Success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route("/login", methods =['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
    #     if form.email.data == 'marco@rakuten.com' and form.password.data == '123':
    #         flash('You have logged in', 'Success')
    #         return redirect(url_for('home'))
    #     else:
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember = form.remember.data)
            next_page = request.args.get('next')
            #redirect user to the home page if the user has not requested an specific url at the beginning.
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and/or password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route("/account", methods =['GET','POST'])
@login_required
def account():
    form = UpdateAccountForm() #Create an instance from UpdateAccountForm
    if form.validate_on_submit(): #Method to validate form
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account',
                            image_file = image_file, form=form)
