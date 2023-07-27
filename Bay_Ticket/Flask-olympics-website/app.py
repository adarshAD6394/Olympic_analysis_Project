from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL

app = Flask(__name__)

# MySQL configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'ProjectGFG'
app.config['MYSQL_DB'] = 'Flask_app'
app.config['SECRET_KEY'] = 'your_secret_key'  # Replace with a secret key for session management

# Initialize the MySQL object
mysql = MySQL(app)

# Create a route for the homepage
@app.route('/')
def index():
    return render_template('home/adasrh_6394/Hackathon/home/lander_page.html')

# Create a route for user signup
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        connection = mysql.connection
        cursor = connection.cursor()

        # Create the users table if it doesn't exist
        cursor.execute("CREATE TABLE IF NOT EXISTS users (id INT AUTO_INCREMENT PRIMARY KEY, "
                       "username VARCHAR(255) UNIQUE NOT NULL, "
                       "email VARCHAR(255) UNIQUE NOT NULL, "
                       "password VARCHAR(255) NOT NULL)")

        # Check if the username is already taken
        cursor.execute("SELECT id FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()

        if user:
            cursor.close()
            connection.close()
            return "Username already taken. Please choose a different username."

        # Insert the new user into the database
        cursor.execute("INSERT INTO users (username, email, password) VALUES (%s, %s, %s)",
                       (username, email, password))
        connection.commit()

        cursor.close()
        connection.close()

        # Redirect to the login page after successful signup
        return redirect(url_for('login'))

    return render_template('signup.html')

# Create a route for user login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'user_id' in session:
        return redirect(url_for('index'))  # Redirect to index if already logged in

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        connection = mysql.connection
        cursor = connection.cursor()

        # Check if the credentials match in the database
        cursor.execute("SELECT id FROM users WHERE username = %s AND password = %s",
                       (username, password))
        user = cursor.fetchone()

        cursor.close()
        connection.close()

        if user:
            # Store the user ID in the session for future authentication
            session['user_id'] = user[0]
            return redirect(url_for('index'))  # Redirect to index page after login
        else:
            return "Login failed. Invalid username or password."

    return render_template('login.html')

# Create a route for booking
@app.route('/booking', methods=['GET', 'POST'])
def booking():
    if 'user_id' not in session:
        return redirect(url_for('login'))  # Redirect to login if not logged in

    if request.method == 'POST':
        # Check if the 'booking_details' key is present in the form data
        if 'booking_details' not in request.form:
            return "Error: Booking details missing. Please fill out the booking form."

        # Get the booking details from the form
        booking_details = request.form['booking_details']

        connection = mysql.connection
        cursor = connection.cursor()

        # Create the bookings table if it doesn't exist
        cursor.execute("CREATE TABLE IF NOT EXISTS bookings (id INT AUTO_INCREMENT PRIMARY KEY, "
                       "user_id INT NOT NULL, "
                       "booking_details TEXT NOT NULL, "
                       "FOREIGN KEY (user_id) REFERENCES users(id))")

        # Get the user ID from the session
        user_id = session['user_id']

        # Insert the booking data into the database
        cursor.execute("INSERT INTO bookings (user_id, booking_details) VALUES (%s, %s)",
                       (user_id, booking_details))
        connection.commit()

        cursor.close()
        connection.close()

        return "Booking successful!"

    return render_template('booking.html')

# Run the Flask application if executed directly
if __name__ == '__main__':
    app.run(debug=True)
