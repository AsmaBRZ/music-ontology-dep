from SPARQLWrapper import SPARQLWrapper, JSON


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

equivalence =  {"birthP":"Lieu de naissance","interprete":"Interprète", "compositeur":"Compositeur", "auteur":"Auteur", "musicien":'Musicien', "birthD":"Date de naissance", "group":"URL","person":"URL", "name":"Nom", "dateC":"Date de création","origin":"Pays"}
def artiste_query(name,birthD,birthP):
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
        where = where  + '?person  dbo:nationality ?birthP .'
        where = where  + 'FILTER (?birthP = <http://dbpedia.org/resource/'+str(birthP)+'>) '
    else: 
        select = select + " ?birthP "
        where = where  + '?person dbo:birthPlace ?birthP . '
   

    where = where + " } LIMIT 10"

    return select + " " + where


def ask_function_musicien(name):
    where = """ASK { """

    where = where  +  """ 
        { ?person a dbo:MusicalArtist } UNION { ?person a umbel-rc:Artist } """


    where = where  + '?person foaf:name "' + name + '"@en . '
    where = where  + '{?person a yago:Musician110339966} UNION {?person a yago:Musician110340312} '  
    where = where + " }"

    return  where

def ask_function_auteur(name):
    where = """ASK { """

    where = where  +  """ 
        { ?person a dbo:MusicalArtist } UNION { ?person a umbel-rc:Artist } """

    where = where  + '?person foaf:name "' + name + '"@en . '
    where = where  + '{?person a yago:Songwriter110624540} UNION {?person a yago:Writer110801291} UNION {?person a yago:Writer110794014} '
    where = where + " }"

    return  where
    
def ask_function_compositeur(name):
    where = """ASK { """

    where = where  +  """ 
        { ?person a dbo:MusicalArtist } UNION { ?person a umbel-rc:Artist } """

    where = where  + '?person foaf:name "' + name + '"@en . '
    where = where  + '?person a yago:Composer109947232 . '
    where = where + " }"

    return  where
    
def ask_function_interprete(name):
    where = """ASK { """

    where = where  +  """ 
        { ?person a dbo:MusicalArtist } UNION { ?person a umbel-rc:Artist } """

    where = where  + '?person foaf:name "' + name + '"@en . '
    where = where  + '{?person a yago:Singer110599806} UNION {?person a yago:Performer110415638} '
    where = where + " }"

    return  where
    
    
def displayResult(v_nom, v_date, v_place, v_musicien, v_auteur, v_compositeur, v_interprete):
    if v_nom == '':
        nom_artiste = None
    else:
        nom_artiste = v_nom


    if v_date == '':
        date_artiste = None
    else:
        date_artiste = v_date

    if v_place == '':
        lieu_artiste = None
    else:
        lieu_artiste = v_place

    if v_musicien == 'musicien':
        musicien = True
    else:
        musicien = False

    if v_auteur == 'auteur':
        auteur = True
    else:
        auteur = False

    if v_compositeur == 'compositeur':
        compositeur = True
    else:
        compositeur = False

    if v_interprete == 'interprete':
        interprete = True
    else:
        interprete = False
    

    sparql = SPARQLWrapper("http://dbpedia.org/sparql")
    query=artiste_query(nom_artiste,date_artiste,lieu_artiste)
    print("\n",query)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()['results']['bindings']  

    
    print("---------------------")
    
    final_results = []
    for result in results :
        d = {}
        for key,value in result.items():
            attribut = equivalence[key]
            valeur = value['value']
            d[str(attribut)] = str(valeur)
            
            if key == 'name':
                nom_artiste = valeur
                ask_musicien = ask_function_musicien(nom_artiste)
                print("ask_musicien ",ask_musicien)
                sparql.setQuery(ask_musicien)
                sparql.setReturnFormat(JSON)
                is_musicien =  sparql.query().convert()
                print("is_musicien ",is_musicien)

                ask_auteur = ask_function_auteur(nom_artiste)
                print("ask_auteur ",ask_auteur)
                sparql.setQuery(ask_auteur)
                sparql.setReturnFormat(JSON)
                is_auteur = sparql.query().convert()
                print("is_auteur ",is_auteur)


                ask_compositeur =  ask_function_compositeur(nom_artiste)
                print("ask_compositeur", ask_compositeur)
                sparql.setQuery(ask_compositeur)
                sparql.setReturnFormat(JSON)
                is_compositeur =  sparql.query().convert()
                print("is_compositeur ",is_compositeur) 
                
                ask_interprete = ask_function_interprete(nom_artiste)
                print("ask_interprete ",ask_interprete)
                sparql.setQuery(ask_interprete)
                sparql.setReturnFormat(JSON)
                is_interprete = sparql.query().convert()
                print("is_interprete ",is_interprete)

                f=''
                if is_musicien == 'musicien':
                    f=f+'musicien'

                
                if is_auteur == 'auteur':
                    if f=='':
                        f=f+"auteur"
                    else:
                        f=f+", auteur"
            
                if is_compositeur == 'compositeur':
                    if f=='':
                        f=f+"compositeur"
                    else:
                        f=f+", compositeur"


                if is_interprete == 'interprete':
                    if f=='':
                        f=f+"interprète"
                    else:
                        f=f+", interprète"

                d["Fonction"] = f
            

        final_results.append(d)

    print("final_results ",final_results)
    return final_results