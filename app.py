from flask import Flask, render_template,redirect, session
import os
import csv
from flask import request
from flask.json import jsonify
from flask import send_from_directory
from customer import Customer
from my_parser import Parser

app = Flask(__name__)
app.secret_key = 'global_temp'  # Set a secret key for session security


@app.route('/')
def index():
    session.clear() 
    session['string_array'] = []  # Initialize an empty array if it doesn't exist
    return render_template('index.html')

@app.route('/get-user-csv/')
def get_user_csv():
    return send_from_directory('C:\\Users\\shoeb\\Downloads\\My major project\\FrontEnd\\static', 'user_data.csv', as_attachment=True)

@app.route('/get-feedback-csv/')
def get_feedback_csv():
    return send_from_directory('C:\\Users\\shoeb\\Downloads\\My major project\\FrontEnd\\static', 'user_feedback.csv', as_attachment=True)

@app.route('/set_session_variables', methods=['POST'])
def set_session_variables():
    if request.method == 'POST':
        data = request.json
        if 'username' in data and 'login_time' in data:
            session['username'] = data['username']
            session['login_time'] = data['login_time']
            print(session['username'])
            print(session['login_time'])
            return jsonify({"status": "success"})
        else:
            return jsonify({"status": "error", "message": "Username or login time not provided in request"})
    else:
        return jsonify({"status": "error", "message": "Invalid request method"})

@app.route('/static/feedback', methods=['POST'])
def feedback():
    if request.method == 'POST':
        feedback_text = request.form.get('feedback')
        rating = request.form.get('rating')  # Get the rating value from the form
        # Specify the file you want to store the feedback in
        feedback_file = 'C:\\Users\\shoeb\\Downloads\\My major project\\FrontEnd\\static\\user_feedback.csv'
        print(session['username'])
        name = session['username']
        print(session['login_time'])
        login_time = session['login_time']
        if not os.path.exists(feedback_file):
            with open(feedback_file, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["Name","Login-Time","Rating","Feedback"])
        
        # Append the feedback
        with open(feedback_file, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([name, login_time, rating, feedback_text])

        return redirect('/thankyou')
    else:
        return jsonify({"status": "error", "message": "Invalid request method"})

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/usermanual')
def usermanual():
    return render_template('usermanual.html')

@app.route('/thankyou')
def thankyou():
    return render_template('thankyou.html')

@app.route('/static/user_registration', methods=['POST'])
def user_registration():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        age = request.form.get('age')
        phoneNumber = request.form.get('phoneNumber')
        password = request.form.get('password')

        data = [name, email, age, phoneNumber, password]
        csv_file = 'C:\\Users\\shoeb\\Downloads\\My major project\\FrontEnd\\static\\user_data.csv'

        # Check if the file exists, if not, create it and add header
        if not os.path.exists(csv_file):
            header = ["Name", "Email", "Age", "Phone Number", "Password"]
            with open(csv_file, 'w', newline='') as fp:
                csv.writer(fp).writerow(header)

        # Append user data to the CSV file
        with open(csv_file, 'a', newline='') as fp:
            csv.writer(fp).writerow(data)

        return redirect('/login')
    else:
        return jsonify({"status": "error", "message": "Invalid request method"})

@app.route('/chatbot', methods=['GET', 'POST'])
def chatbot():
    o = Customer()
    p = Parser()
    m = ""
    message = ""
    order_msg = ""
    order = ""
    msg = ""
    msgs = ""
    resp = ""
    temp = ""
    bill = None
    delivery_msg = ""
    place = ""
    location = ""
    t = ""
    tm = ""
    bill_html = ""
    bc = ""
    mg = ""
    cm = ""
    # feedback = ""
    fb_msg = ""
    c = ""
    greet = ""
    # h = ""
    # hm = ""
    
    str_array = ""

    welcome_message = o.welcome_greeting()

    if request.method == 'POST':
        user_input = request.form.get('userInput')
        if any(keyword in user_input.lower() for keyword in ['top', 'best', 'suggest', 'recommend', 'suggestions', 'recommendation', 'special']) and user_input != "menu" and user_input != "no" and 'want' not in user_input.lower() and 'cancel' not in user_input.lower():
            tm = user_input
            t = o.top_food()
            bc = o.best_combos()
            message = o.get_menu()
            print("case 0")
        if user_input == "menu":
            t = o.top_food()
            bc = o.best_combos()
            mg = o.get_menu()
            m = user_input
            message = p.user_input(user_input)
            order_msg = o.place_order_message()
            print("case 1")
        # if user_input == "help":
        #     h = user_input
        #     hm = p.user_input(user_input)
            # print("case 6")
        if 'cancel' in user_input.lower() and 'want' not in user_input.lower() and ("menu" not in user_input.lower() and "no" not in user_input.lower()) and not any(keyword in user_input.lower() for keyword in ['top', 'best', 'suggest', 'recommend', 'suggestions', 'recommendation', 'special']):
            cm = user_input
            c = o.cancel_order()
        if user_input != "menu" and user_input.lower() != "no" and not any(keyword in user_input.lower() for keyword in ['top', 'best', 'suggest', 'recommend', 'suggestions', 'recommendation', 'special']) and 'want' in user_input.lower() and 'cancel' not in user_input.lower():
            t = o.top_food()
            bc = o.best_combos()
            mg = o.get_menu()
            m = "menu"
            message = p.user_input('menu')
            order_msg = o.place_order_message()
            order = o.generate_order(user_input)
            temp = user_input
            session['global_temp'] = temp  # Store the value in the session
            session['string_array'].append(temp)
            str_array = session['string_array']
            print(session['global_temp'])
            print(session['string_array'])
            for x in str_array:
                print(x)
            msg = "Do you want something else ?"
            print("case 2")
        if user_input.lower() == "no" and user_input != "menu" and 'cancel' not in user_input.lower():
            t = o.top_food()
            bc = o.best_combos()
            mg = o.get_menu()
            m = "menu"
            message = p.user_input('menu')
            order_msg = o.place_order_message()
            str_array = session['string_array']
            order = session['orders']  # Retrieve the value from the session
            msg = "Do you want something else ?"
            resp = user_input
            msgs = o.order_confirmed()
            bill = o.generate_bill(session['orders'])
            # Process the bill response
            if bill:
                # If bill is a message, display it using <p> tag
                if isinstance(bill, str):
                    bill_html = f"{bill}"
                # If bill is a list of items, display them as a list
                else:
                    bill_html = "<h3>BILL:</h3><ul>"
                    for item in bill:
                        bill_html += f"<li>{item}</li>"
                    bill_html += "</ul>"
                    delivery_msg = o.address_message()
            else:
                bill_html = "" 
            
            # location = o.get_delivery_time(user_input)
            print("case 3")
        if 'want' not in user_input.lower() and ("menu" not in user_input.lower() and "no" not in user_input.lower()) and not any(keyword in user_input.lower() for keyword in ['top', 'best', 'suggest', 'recommend', 'suggestions', 'recommendation', 'special']) and 'cancel' not in user_input.lower():
            # print(f"user_input: {user_input}")
            t = o.top_food()
            bc = o.best_combos()
            mg = o.get_menu()
            m = "menu"
            message = p.user_input('menu')
            order_msg = o.place_order_message()
            str_array = session['string_array']
            order = session['orders']  # Retrieve the value from the session
            msg = "Do you want something else ?"
            resp = "no"
            msgs = o.order_confirmed()
            bill = o.generate_bill(session['orders'])
            # Process the bill response
            if bill:
                # If bill is a message, display it using <p> tag
                if isinstance(bill, str):
                    bill_html = f"<p class='bot'>{bill}</p>"
                # If bill is a list of items, display them as a list
                else:
                    bill_html = "<h3>BILL:</h3><ul>"
                    for item in bill:
                        bill_html += f"<li>{item}</li>"
                    bill_html += "</ul>"
                    delivery_msg = o.address_message()
            else:
                bill_html = "" 
            # delivery_msg = o.address_message()
            place = user_input
            location = o.get_delivery_time(user_input)
            fb_msg = o.feed_back()
            # feedback = ""
            print("case 4")
    else:
        greet = o.hello()
        message = o.get_help()
        # messages = []
        # for mesg in h:
        #     messages.append(mesg)
        print("case 5")

    return render_template('chatbot.html', welcome_message=welcome_message,tm=tm, t=t, bc=bc, m=m, mg=mg, message=message, order_msg=order_msg, str_array=str_array, order=order, msg=msg,
                           resp=resp, msgs=msgs, temp=temp, bill=bill_html, delivery_msg=delivery_msg, place=place, location=location, fb_msg=fb_msg, c=c, cm=cm, greet=greet)


# Initialize an empty list for orders in the session before the first request
@app.before_request
def before_request():
    if 'orders' not in session:
        session['orders'] = []

if __name__ == '__main__':
    app.run(debug=False,host='0.0.0.0')
