from SPARQLWrapper import SPARQLWrapper, JSON
import tkinter



texte1 = ""
texte0 = ""
bouton0 = ""


prefix = """PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
PREFIX dc: <http://purl.org/dc/elements/1.1/>
PREFIX : <http://dbpedia.org/resource/>
PREFIX dbpedia2: <http://dbpedia.org/property/>
PREFIX dbpedia: <http://dbpedia.org/>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>"""

equivalence =  {"birthP":"Place de naissance","birthD":"Date de naissance", "group":"URL","person":"URL", "name":"Nom", "dateC":"Date de création","origin":"Pays"}
def artiste_query(prefix, name=None,birthD=None,birthP=None):
    select = """SELECT DISTINCT ?person """

    where =  """ WHERE {
        { ?person a dbo:MusicalArtist } UNION { ?person a umbel-rc:Artist } """


    if name != None :
        where = where  + '?person foaf:name "' + name + '"@en . '
    else: 
        select = select + " ?name "
        where = where  + '?person foaf:name ?name . '

    if birthD != None :
        where = where  + '?person dbo:birthDate "' + birthD + '"^^xsd:date  . '
    else: 
        select = select + " ?birthD "
        where = where  + '?person dbo:birthDate ?birthD . '

    if birthP != None :
        where = where  + '?person dbo:birthPlace "' + birthP + ' " . '
    else: 
        select = select + " ?birthP "
        where = where  + '?person dbo:birthPlace ?birthP . '

    where = where + " } LIMIT 10"

    return select + " " + where
    
def groupe_query(prefix, name=None,dateC=None,origin=None):
    select = """SELECT DISTINCT ?group """

    where =  """ WHERE {
        { ?group a schema:MusicGroup } UNION { ?group a dbo:Band } UNION { ?group a umbel-rc:Band_MusicGroup } """


    if name != None :
        where = where  + '?group foaf:name "' + name + '"@en . '
    else: 
        select = select + " ?name "
        where = where  + '?group foaf:name ?name . '

    if dateC != None :
        where = where  + '?group dbo:activeYearsStartYear "' + dateC + '"^^xsd:date  . '
    else: 
        select = select + " ?dateC "
        where = where  + '?group dbo:activeYearsStartYear ?dateC . '

    if origin != None :
        where = where  + '?group dbo:origin "' + origin + ' " . '
    else: 
        select = select + " ?origin "
        where = where  + '?group dbp:origin ?origin . '

    where = where + " } LIMIT 10"

    return select + " " + where

def displayResult():
    global texte1
    global texte0
    date_artiste = texte1.get()
    nom_artiste = texte0.get()



    sparql = SPARQLWrapper("http://dbpedia.org/sparql")
    #query=artiste_query(prefix,name = "Eminem")
    #query=artiste_query(prefix,birthD="1972-10-17")
    #query=artiste_query(prefix,"Kurt Cobain")

    #query=groupe_query(prefix,name="Nirvana")


    if(len(nom_artiste)==0):
        nom_artiste = None


    if(len(date_artiste)==0):
        date_artiste = None

    query=artiste_query(prefix,name=nom_artiste,birthD=date_artiste)

    print(query+"\n")
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()['results']['bindings']

    #print(results)
    affichage = ""
    for result in results :
        for key,value in result.items():
            attribut = equivalence[key]
            valeur = value['value']
            if(key == 'birthP'):
                valeur = value['value'].split("/")[-1]
            affichage = affichage + str(attribut)+ " : "+valeur+"\n"
            #print(attribut," : ",valeur)
        #print()


    print(affichage)
    return affichage

    """
    birthD = results['birthD']['value']
    birthP = results['birthP']['value'].split("/")[-1]

    print(birthD)
    print(birthP)
    """



def Window1():
    global texte1
    global texte0

    affichage = displayResult()
    window1 = tkinter.Tk()
    window1.title("Résultats")
    window1.minsize(640,480)
    label = tkinter.Label(window1, text= affichage)
    label.pack()


racine0 =tkinter.Tk()
racine0.title("Music Search Engine")
racine0.minsize(640,480)
invite0 =tkinter.Label(racine0, text ="Nom de l'artiste ", width =20, height =3, fg ="navy")
invite0.pack()
texte0 =tkinter.StringVar()  # definition d'une variable-chaine pour recevoir la saisie d'un texte
texte0.set("")  # facultatif: assigne une valeur à la variable
saisie0 =tkinter.Entry(textvariable =texte0, width =30)
saisie0.pack()

print(texte0.get()) # affiche le texte saisi à la fermeture de la fenêtre

invite1 =tkinter.Label(racine0, text ="Date de naissace de l'artiste ", width =50, height =3, fg ="navy")
invite1.pack()
texte1 =tkinter.StringVar()  # definition d'une variable-chaine pour recevoir la saisie d'un texte
texte1.set("AAAA-MM-JJ")  # facultatif: assigne une valeur à la variable
saisie1 =tkinter.Entry(textvariable =texte1, width =30)
saisie1.pack()

bouton0 =tkinter.Button(racine0, text ="ok", command = Window1)
bouton0.pack(side =tkinter.BOTTOM)
racine0.mainloop()


