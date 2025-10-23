from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from chatbot_model import get_response
import os

# Flask app setup
app = Flask(__name__)
app.secret_key = "secret123"

# Database setup
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

# User Model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(150), nullable=False)

# Create database if not exists
with app.app_context():
    db.create_all()

# ----------- ROUTES -----------

# Home (Chatbot) - Requires Login
@app.route("/")
def home():
    if "user_id" not in session:
        return redirect(url_for("login"))
    return render_template("index.html")

# Signup
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        # Check if username exists
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash("Username already exists. Try another.", "error")
            return redirect(url_for("register"))

        # Hash password
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        # Save new user
        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash("Account created successfully! Please login.", "success")
        return redirect(url_for("login"))
    return render_template("register.html")

# Login
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        user = User.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password, password):
            session["user_id"] = user.id
            session["username"] = user.username
            flash("Login successful!", "success")
            return redirect(url_for("home"))
        else:
            flash("Invalid username or password", "error")
            return redirect(url_for("login"))
    return render_template("login.html")

# Logout
@app.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for("login"))

# Chatbot API
@app.route("/get", methods=["POST"])
def chatbot_response():
    if "user_id" not in session:
        return jsonify({"response": "Please log in to chat with me!"})

    user_message = request.json["message"]
    bot_reply = get_response(user_message)
    return jsonify({"response": bot_reply})

# Run app
if __name__ == "__main__":
    app.run(debug=True)
