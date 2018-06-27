from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy  # flask_sqlalchemy is the module, SQLAlchemy is the class
from datetime import datetime  # need this for our second table



app = Flask(__name__)

app.config.update(  # GENERAL PURPOSE PYTHON DICT- for whole project- this is a method
    #DEBUG=True,
    SECRET_KEY='topsecret', # this is used by flask and other 3rd party tools for
    SQLALCHEMY_DATABASE_URI='postgresql://postgres:p0stgr3s!@localhost/catalog_db', # this has the name of the DB type, PW, server and DB name
    SQLALCHEMY_TRACK_MODIFICATIONS=True  # surpress some warning messages

)

db = SQLAlchemy(app)  # note we are passing it our application 'app'. This lets flask know we are using a db

@app.route('/index') # can have more than one route per function
@app.route('/')   # route using a decorator... "/" means the route or homepage of the website
def hello_world():
    return 'Hello World!' # whatever is in the body of the funtion will be executed


@app.route('/new/')
def query_strings(greeting = 'hello'):
    query_val = request.args.get('greeting', greeting)
    return '<h1> the greeting is : {0} </h1>'.format(query_val)  # this will return none because there is no value set for greeting

@app.route('/user/')
@app.route('/user/<name>')# brackets like this will always be a variable
def no_query_strings(name = 'claud'): # if we use variables in the routes, we must pass them in the function as so

    return '<h1> Hello There : {0} </h1>'.format(name)



@app.route('/temp')
def using_templates():
    return render_template('hello.html') # render_templates takes two arguments- first is the html template the second is any number of arguments


@app.route('/watch')
def movies_2018():
    movie_list = ['Ocean\'s 8', 'Gotti', 'Superfly', 'Tag', 'Incredibles2']



    return render_template('movies.html', movies=movie_list, name = 'Jenny R Page')


@app.route('/tables')
def movies_plus():
    movie_dict = {'Ocean\'s 8': 01.55, 'Gotti': 2.00, 'Superfly': 2.15, 'Tag': 1.47, 'Incredibles2': 1.59}



    return render_template('table_data.html', movies=movie_dict, name = 'Jenny R Page')


@app.route('/filters')
def filter_data():
    movie_dict = {'Ocean\'s 8': 01.55, 'Gotti': 2.00, 'Superfly': 2.15, 'Tag': 1.47, 'Incredibles2': 1.59}



    return render_template('filter_data.html', movies=movie_dict, name = None, film='a chirstmas carol')


@app.route('/macros')
def jinja_macros():
    movie_dict = {'Ocean\'s 8': 01.55, 'Gotti': 2.00, 'Superfly': 2.15, 'Tag': 1.47, 'Incredibles2': 1.59}



    return render_template('using_macros.html', movies=movie_dict)



class Publication(db.Model):  #this inherents from db.Model
    __tablename__ = 'publication'  # this is the name of the table itself

    # note using SQLalchemy takes care alof the DB talk and config for us

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)

    def __init__(self, name): # removing ID because we want the priamry key to be auto-generated
        #self.id = id removing this so that the primary key is auto generated
        self.name = name

    def __repr__(self ):  # this returns a string version of the instance
        return  'Publisher is {} '.format(self.name)  # removing self that ID so the primary key could be auto-generated



class Book(db.Model):
    __tablename__ = 'book'  # this is the name of the table itself

    # note using SQLalchemy takes care alot the DB talk and config for us

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(500), nullable=False, index=True) # this will spead up results time
    author = db.Column(db.String(350))
    avg_rating = db.Column(db.Float)
    format = db.Column(db.String(50))
    image = db.Column(db.String(100), unique=True)
    num_pages = db.Column(db.Integer)
    pub_date = db.Column(db.DateTime, default=datetime.utcnow())# this datetime is from Python

    #relationship

    pub_id = db.Column(db.Integer, db.ForeignKey('publication.id')) # this is the last column- need to define foreign key
    #  and pass the priamry key from the publication table, the id column (which is its primary key)
    # this is a 1:many relationship- because each publisher can have more than one book.
    # so the one is the publisher the many is the # of books he can publish

    def __init__(self, title, author, avg_rating, book_format, image, num_pages, pub_id): # note relationship col is included

        # purpose contrcuts/registers the new instances every time one is created.
        self.title = title
        self.author = author
        self.avg_rating = avg_rating
        self.format = book_format
        self.image = image
        self.num_pages= num_pages
        self.pub_id = pub_id
        # note we did not include the pub date, because date fields in SQLAlchemy are popuated automatically because we set a sefault for this field
        # same with the primary key


    def __repr__(self):  # this returns a string version of the instance- prints in an acceptable manner
        return '{} by {} '.format(self.title, self.author)





if __name__ == '__main__':  # this is how we intend to run this module... directly. That is no other modual will call it
    db.create_all()  # this will create the DB tables but only if they dont exist
    app.run(debug=True, port=5006)  # i am stating port 5002 since I want no conflicts with other Flask apps in dev


# on my system when I run this I must use python3 run.py