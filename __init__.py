from flask import Flask, render_template_string, render_template, jsonify
from flask import render_template
from flask import json
from urllib.request import urlopen
import sqlite3
from tkinter import*
from tkinter import messagebox



                                                                                                                                       
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


@app.route('/fiche_client_recherche/<string:nom>')
def Search(nom):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    param="%" + nom +"%"
    cursor.execute('SELECT * FROM clients WHERE nom  LIKE ?' , (param,))
    data = cursor.fetchall()
    conn.close()
    
    # Rendre le template HTML et transmettre les données
    return render_template('read_data.html', data=data)


@app.route('/formulaire/')
def validate():
    # récupération des données du formulaire
    nom = entryNom.get()
    prenom   =  entryPrenom.get() 
    adresse     =  entryAdresse.get() 
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    req1 = "CREATE TABLE IF NOT EXISTS clients(id INTEGER PRIMARY KEY AUTOINCREMENT, nom TEXT NOT NULL\
,prenom TEXT NOT NULL , adresse TEXT NOT NULL)"
    cur.execute(req1)    
    req2 = "INSERT INTO clients (nom , prenom, adresse) values (?, ?, ?)"
    cur.execute(req2 , (nom, prenom, adresse))
    conn.commit()
    conn.close()

    messagebox.showinfo("Succès", "Élément inséré avec succès dans la base de données.")
    except Exception as e:
        messagebox.showerror("Erreur", f"Erreur lors de l'insertion dans la base de données : {str(e)}")


    
root = Tk()
root.geometry("600x400")
 
#==============================
# create a form to insert data
#==============================
# Label & Entry for nom
lblNom = Label(root , text = "Nom : ")
lblNom.place(x = 10 , y = 10)
entryNom = Entry(root )
entryNom.place(x = 100 , y = 10 , width = 200)
 
# Label & Entry Prenom
lblPrenom = Label(root , text = "Prenom")
lblPrenom.place( x = 10 , y = 40 ) 
entryPrenom = Entry(root)
entryPrenom.place( x = 100 , y = 40 , width = 200)
 
# Label & Entry Adresse
lblAdresse = Label(root , text = "Adresse")
lblAdresse.place( x = 10 , y = 70 ) 
entryAdresse = Entry(root)
entryAdresse.place( x = 100 , y = 70 , width = 200)
 
# Button Action
btnValidate = Button(root , text = "INSERTION" , command = validate)
btnValidate.place(x = 100 , y = 100, width = 200 , height = 25)
root.mainloop()







if __name__ == "__main__":
  app.run(debug=True)
