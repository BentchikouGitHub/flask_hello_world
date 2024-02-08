from flask import Flask, render_template_string, render_template, jsonify
from flask import render_template
from flask import json
from urllib.request import urlopen
import sqlite3
from tkinter import*



                                                                                                                                       
app = Flask(__name__)                                                                                                                  
                                                                                                                                       
@app.route('/')
def hello_world():
    return render_template('hello.html')
                                                                                                                                       
@app.route("/fr/")
def monfr():
    return "<h2>Bonjour tout le monde !</h2>"




@app.route('/paris/')
def meteo():
    response = urlopen('https://api.openweathermap.org/data/2.5/forecast/daily?q=Paris,fr&cnt=16&appid=bd5e378503939ddaee76f12ad7a97608')
    raw_content = response.read()
    json_content = json.loads(raw_content.decode('utf-8'))
    results = []
    for list_element in json_content.get('list', []):
        dt_value = list_element.get('dt')
        temp_day_value = list_element.get('temp', {}).get('day') - 273.15 # Conversion de Kelvin en °c 
        results.append({'Jour': dt_value, 'temp': temp_day_value})
    return jsonify(results=results)
@app.route("/rapport/")
def mongraphique():
    return render_template("graphique.html")



@app.route('/consultation/')
def ReadBDD():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM clients;')
    data = cursor.fetchall()
    conn.close()
    
    # Rendre le template HTML et transmettre les données
    return render_template('read_data.html', data=data)




@app.route('/fiche_client/<int:post_id>')
def Readfiche(post_id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM clients WHERE id = ?', (post_id,))
    data = cursor.fetchall()
    conn.close()
    
    # Rendre le template HTML et transmettre les données
    return render_template('read_data.html', data=data)



@app.route('/fiche_client2/<string:post_DU>')
def Readfiche(post_id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    param="%" + post_DU +"%"
    cursor.execute('SELECT * FROM clients WHERE nom  LIKE ?' , (param))
    data = cursor.fetchall()
    conn.close()
    
    # Rendre le template HTML et transmettre les données
    return render_template('read_data.html', data=data)


def validate():
    # récupération des données du formulaire
    name = entryName.get()
    email   =  entryEmail.get() 
    age     =  entryAge.get() 
    conn = sqlite3.connect('mydatabase.db')
    cur = conn.cursor()
    req1 = "CREATE TABLE IF NOT EXISTS students(id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL\
,email TEXT NOT NULL , age INTEGER NOT NULL)"
    cur.execute(req1)    
    req2 = "INSERT INTO students (name , email, age) values (?, ?, ?)"
    cur.execute(req2 , (name, email, age))
    conn.commit()
    conn.close()
    
root = Tk()
root.geometry("600x400")


#==============================
# create a form to insert data
#==============================
# Label & Entry for name
lblName = Label(root , text = "Name : ")
lblName.place(x = 10 , y = 10)
entryName = Entry(root )
entryName.place(x = 100 , y = 10 , width = 200)
 
# Label & Entry Email
lblEmail = Label(root , text = "Email")
lblEmail.place( x = 10 , y = 40 ) 
entryEmail = Entry(root)
entryEmail.place( x = 100 , y = 40 , width = 200)
 
# Label & Entry Age
lblAge = Label(root , text = "Age")
lblAge.place( x = 10 , y = 70 ) 
entryAge = Entry(root)
entryAge.place( x = 100 , y = 70 , width = 200)
 
# Button Action
btnValidate = Button(root , text = "Validate" , command = validate)
btnValidate.place(x = 100 , y = 100, width = 200 , height = 25)
root.mainloop()
#==============
# Display data
#==============
conn = sqlite3.connect('mydatabase.db')
cur = conn.cursor()
result = cur.execute("select * from students")
for row in result:
    print("ID : ", row[0])
    print("Name : ", row[1])
    print("Email : ", row[2])
    print("Age : ", row[3])
    print("--------------------------")





if __name__ == "__main__":
  app.run(debug=True)
