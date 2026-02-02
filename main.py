import datetime
import fileinput

from flask import Flask, render_template, request, url_for, redirect

import data.UserDB as db

app = Flask(__name__,static_folder='static')

logged_in = False
"""
HOME PAGE
"""
@app.route("/", methods = ['GET','POST'])
def home():

    return render_template("home.html")


"""
LOGIN
"""
@app.route("/login", methods = ['GET','POST'])
def login():
    global logged_in
    if not logged_in:
        if request.method == 'POST':
            username = request.form.get('username')
            password = request.form.get('password')

            with open("data/user_data.csv") as userfile:
                userfile.readline() #skip header line
                trueline = userfile.readline()

            fields = trueline.split(',')
            for i in range(2):
                fields[i] = fields[i].strip()
            if username == fields[0] and password == fields[1]:
                logged_in = True
                return redirect(url_for('dashboard'))
            return redirect(url_for('login'))
        return render_template('login.html', user="")
    else:
        return redirect(url_for('dashboard'))

"""
INVENTORY DASHBOARD
"""
@app.route("/dashboard", methods = ['GET','POST'])
def dashboard():
    if logged_in:
        error = 0
        #make rows be all the rows of the db
        database = db.Database()
        if request.method == "POST":
            item_name = request.form.get('Button') #get item name from button value

            if request.form.get("new_quantity"):
                quantity = request.form.get("new_quantity") #data verification
                #TESTING
                print(item_name)
                if quantity.isdigit():
                    #Update db with new quantity for inventory
                    database.changeQuantity(item_name, quantity)
                    redirect(url_for('dashboard'))
                else:
                    #send message saying the db has not been updated
                    error = "Invalid Input. Database has not been update."
            else:
                database.removeItem(item_name)
                redirect(url_for('dashboard'))

        rows = database.cur.execute("SELECT * FROM Inventory").fetchall()
        return render_template("inventory.html",
                                page_title = "Inventory",
                                rows = rows,
                                error = error)
    else:
        return redirect(url_for('login'))

"""
ADD ITEM
"""
@app.route("/add", methods = ['GET','POST'])
def add():
    if logged_in:
        database = db.Database()

        if request.method == "POST":
            name = request.form.get("name")
            amount = request.form.get("amount")
            donor = request.form.get("donor")
            category = request.form.get("category")
            dietary_restrictions = [request.form.get('kosher'), request.form.get('halal'),
                                    request.form.get('vegetarian'), request.form.get('vegan')]
            kosher = dietary_restrictions[0]
            halal = dietary_restrictions[1]
            vegetarian = dietary_restrictions[2]
            vegan = dietary_restrictions[3]
           # allergens = [request.form.get('dairy'), request.form.get('eggs'), request.form.get('fish'),
                      #   request.form.get('shellfish'), request.form.get('tree_nuts'), request.form.get('peanuts'),
                      #  request.form.get('wheat'), request.form.get('soybeans'), request.form.get('sesame')]


            # tag_list = request.form.get('tags')
            # tags = tag_list.split(',')
            # for i in range(0, len(tags)):
            #    tags[i] = tags[i].strip()

            requested = request.form.get('requested')
            expiration = request.form.get('expiration_date')

            database.addItem(name,None,amount,category,donor,vegetarian,kosher,vegan,halal,expiration,requested)
            print(database.cur.execute("SELECT * FROM Inventory").fetchall())
        return render_template("add.html")
    else:
        return redirect(url_for('login'))

if __name__ == "__main__":
    global LOGGED_IN
    LOGGED_IN = False
    app.run(debug=True)