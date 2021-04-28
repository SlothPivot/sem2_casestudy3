from flask import (
    Flask,
    g,
    jsonify,
    redirect, 
    render_template, 
    url_for, request, 
    make_response,
    session,
    url_for
)
import databaseConnector as db
import passHash as ph

class User:
    def __init__(self, username, email):
        self.username = username
        self.email = email
    
    def __repr__(self):
        return f'<User: {self.username}>'

# users = []
# users.append(User(username='Mr.Robot', email='mrrobot@email.nl', password='anonymous'))
# users.append(User(username='Pickle Rick', email='picklerick@email.nl', password='swifty'))
# users.append(User(username='Elon Musk', email='elonmusk@email.nl', password='spacex'))

# print(users)

app = Flask(__name__)
app.secret_key = '$uper$ecretP@ssword'



@app.before_request
def before_request():
    g.user = None

    if 'username' in session:
        try:
            user = db.checkUser(session['username'])[0]
            print("username " + user)
        except:
            pass
        g.user = user


@app.route('/')
@app.route('/home')
def home():
    print("you are in home end-point")
    if not g.user:
        return redirect(url_for('login'))
    
    return render_template('home.html', title='Home', username = g.user)


@app.route('/inventory')
def inventory():
    items = db.returnListInv()
    return render_template('inventory.html', title='Inventory', items=items)


@app.route('/about')
def about():
    print("you are in about end-point")
    return render_template('about.html', title='About')


# @app.route('/login')
# def login():
#     print("you are in login end-point")
#     auth = request.authorization

#     if auth and auth.password == 'password':
#         return ''

#     return make_response('Could not verify!', 401, {'WWW-Authenticate' : 'Basic realm"Login Required"'})


@app.route('/login', methods=['GET', 'POST'])
def login():
    print("you are in login end-point")

    if request.method == 'POST':
        session.pop('username', None)
        print("this is a POST request")

        username = request.form['username']
        password = request.form['password']

        # user = [x for x in users if x.username == username][0]
        # if user and user.password == password:

        try:
            credentials = db.readCreds(username)
            if ph.verify_password(credentials[1], password):
                session['username'] = credentials[0]
                return redirect(url_for('home'))
            else:
                pass
        except:
            pass

        return redirect(url_for('login'))

    return render_template('login.html', title='Login')


@app.route('/register', methods =['GET', 'POST'])
def register():
    print("you are in register end-point")
    if request.method == 'GET':
        print("this is a GET request")

        return render_template('register.html')
    else:
        session.pop('username', None)
        print("this is a POST request")

        username = request.form['username']
        email = request.form['email']
        password = ph.hash_password(request.form['password'])

        db.registerNewCreds(username, password, email)

        return redirect(url_for('home'))
        
    return render_template('register.html', title='Register')

@app.route('/logout', methods =['GET'])
def logout():
    print("you are in logout end-point")
    if request.method == 'GET':
        print("this is a GET request")
        session.clear()
        return redirect(url_for('home'))

    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)
