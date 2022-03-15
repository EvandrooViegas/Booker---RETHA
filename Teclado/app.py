

from re import search
from flask import Flask, render_template, url_for, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy
import jyserver.Flask as jsf
app = Flask(__name__)
app.debug = True

#Definicoes do server
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SECRET_KEY'] = 'e31fc5f483a0c6464d7061d0eaff10fa'
db = SQLAlchemy(app)

listBooks= []
newlist = []

#DataBase Lists
listBooksDB = []



#Classe Para Database
class BookDataBase(db.Model):
    id  = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(50), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=False, nullable=False)
    for_people = db.Column(db.Integer, nullable=False)

    def __init__(self, date, name, email, for_people):
        self.date = date
        self.name = name
        self.email = email
        self.for_people = for_people

    def __repr__(self):
        return '<Book %r>' % self.name
bookDB = BookDataBase.query.all()


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/book', methods=['GET', 'POST'])
def book():
    class Books():
        def __init__(self, id, date, name, email, for_people):
            self.id = id
            self.date = date
            self.name = name
            self.email = email
            self.for_people = for_people
            
    #Pegar elementos da página 'form.html'
    if request.method=="POST":
        # def IfentifierGenerator():
            
        #     identifier = identifier + 1
        #     return identifier

        dateForm = request.form['date']
        nameForm = request.form['name']     
        emailForm = request.form['email']
        for_peopleForm = request.form['for']
        # identifier = IdentifierGenerator()

        newBook = Books(id, dateForm, nameForm, emailForm, for_peopleForm)
        

        newId = newBook.id
        newDate = newBook.date
        newName = newBook.name
        newEmail = newBook.email
        newFor_people = newBook.for_people

        #Adding values to the List
        newlist = [newId, newDate, newName, newEmail, newFor_people]
        listBooks.append(newlist)

        print(newlist)
        print(listBooks)


        #Add values to the database
        newBookDB = BookDataBase(date=dateForm, name=nameForm, email=emailForm, for_people=for_peopleForm)
        db.session.add(newBookDB)
        db.session.commit()

        flash(f'A new book have been booked for {nameForm} for {dateForm}')

        listBooksDB.append(newBookDB)
        print(listBooksDB)
        

        #Get values from the database
        return redirect(url_for('table'))

    return render_template('form.html')

@app.route('/options/<int:id>', methods=['GET', 'POST'])
def options(id):
    book_to_update = BookDataBase.query.get_or_404(id)
    return render_template('options.html', book=book_to_update)

@app.route('/delete/<int:id>')
def delete(id):
    book_to_delete = BookDataBase.query.get_or_404(id)
    try:
        db.session.delete(book_to_delete)
        db.session.commit()
        flash("Book deleted succefully")
        return redirect('/table')
    except:
        flash("A problem occured")


#--------------------------------------------------------------
@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):   
    book_to_update = BookDataBase.query.get_or_404(id)   

    if request.method=="POST":
        dateForm = request.form['date_update']
        nameForm = request.form['name_update']     
        emailForm = request.form['email_update']
        for_peopleForm = request.form['for_update']
        
        book_to_update.date = dateForm
        book_to_update.name = nameForm
        book_to_update.email = emailForm
        book_to_update.for_people = for_peopleForm

        try:
            db.session.commit()
            flash("Book updated succefully")
            return redirect(url_for("table"))

        
        except:
            flash("A problem occured, try later")
            return redirect(url_for("table"))
            
        
    return render_template('update.html', book_to_update=book_to_update)


@app.route('/filterbooks', methods=['GET','POST'])
def FilterBooks():
    search_key = request.form["search_key"]
    if request.method =="POST":
        search_key = request.form["search_key"]
    


        def SearchBook():
            search_result = BookDataBase.query.filter_by(name=search_key).all()
        
            if search_key == '':
                return BookDataBase.query.all()
            else:
                return search_result
        bookDB = SearchBook()      
        return render_template('table.html', bookDB=bookDB)

        


@app.route('/table')
def table(): 
    book()
    
    bookDB = BookDataBase.query.all()
    return render_template('table.html', bookDB=bookDB)
    
if __name__ == "__main__":
    app.run(debug=True)

