from flask import render_template,url_for, flash, redirect
from webapp import app
from webapp.forms import LoginForm, RegistrationForm
from webapp.models import User,Post

posts = [
    {
        'author' : 'Corey',
        'title' : 'Blog Post',
        'content': 'First Post Content',
        'date_posted': 'April 20, 2018'
    },
    {
        'author' : 'Marco',
        'title' : 'Updated Blog Post',
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
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'Success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)

@app.route("/login", methods =['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@blog.com' and form.password.data == 'password':
            flash('You have logged in', 'Success')
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)