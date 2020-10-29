import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from style_my_cv.db import get_db


bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/register', methods=('GET', 'POST'))
def register():
    """Register new user"""

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        password2 = request.form.get("password2")
        db = get_db()
        error = None

        # Check username valid
        if not username:
            error = "Enter a username!"
        elif db.execute('SELECT id FROM users WHERE username = ?', (username,)).fetchone() is not None:
            error = "Username already used!"

        # Check passwords match
        if len(password) < 5:
            error = "Password must be 5 characters or more!"
        if password != password2:
            error = "Passwords do not match."

        if error is None:
            # Insert into database
            db.execute("INSERT INTO users (username, hash) VALUES (? , ?)",
                        (username, generate_password_hash(password, method="pbkdf2:sha256", salt_length=8)))
            db.commit()
            print("###---REGISTRATION SUCCESSFUL---###---REDIRECT TO HOMEPAGE---###")
            
            # Remember which user has registered and log them in
            user = db.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
            session["user_id"] = user['id']

            # return redirect(url_for('main.index'))

        flash(error)

    return render_template("auth/register.html")


@bp.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        db = get_db()
        error = None
        user = db.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()

        # Validate Credentials
        if user is None:
            error = "Incorrect username."
        elif not check_password_hash(user['hash'], password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            # return redirect(url_for('main.index'))

        flash(error)

    return render_template("auth/login.html")


@bp.route('/logout')
def logout():
    """Log user out"""

    session.clear()
    return redirect(url_for('main.index'))


@bp.before_app_request
def load_logged_in_user():
    """Runs before view function to check if there is a user_id in g.user"""

    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()


def login_required(view):
    """Decorator to ensure user login before accessing a view"""

    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view