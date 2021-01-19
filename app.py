from flask import Flask,request, render_template
from flask import jsonify 
from  ontology import *

app = Flask(__name__,template_folder='templates')

@app.route('/')
def index():
   return render_template('index.html')


@app.route('/execRequest', methods=['POST'])
def execRequest():
    if request.method == 'POST': 
        #data = request.files['image_data']
        print("**************************************************************")
        print(request.form.get('nom_artiste'))
        print(request.form.get('date_naissance'))
        print(request.form.get('lieu_naissance'))
        print(request.form.get('auteur'))
        print(request.form.get('musicien'))
        print(request.form.get('compositeur'))
        print(request.form.get('interprete'))
        print("**************************************************************")

        nom_artiste = request.form.get('nom_artiste')
        date_naissance = request.form.get('date_naissance')
        lieu_naissance = request.form.get('lieu_naissance')
        auteur = request.form.get('auteur')
        musicien = request.form.get('musicien')
        compositeur = request.form.get('compositeur')
        interprete = request.form.get('interprete')

        if nom_artiste  == None and auteur == None and interprete == None and musicien ==  None and compositeur == None and date_naissance == None and lieu_naissance  == None:
            return 'No date received'
        #else:
         #   result_dictionary = displayResult(nom_artiste,  date_naissance, lieu_naissance, musicien, auteur, compositeur, interprete)
    else:
      return render_template('index.html')

    return jsonify(results=result_dictionary)
    


if __name__ == '__main__':
   app.run(debug = True)