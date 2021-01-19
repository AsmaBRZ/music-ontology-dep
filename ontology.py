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


def ask_function_musicien(p):
    where = """ASK FROM """
    where = where+ str(p) + """   { """

    where = where  + '{?person a yago:Musician110339966} UNION {?person a yago:Musician110340312} UNION {?person a dbo:Musician} UNION {?person a dbo:Instrumentalist} '  
    where = where + " }"

    return  where

def ask_function_auteur(p):
    where = """ASK FROM """
    where = where+ str(p) + """   { """

    where = where  + '{?person a dbo:Songwriter} UNION  {?person a dbo:Writer} UNION {?person a dbo:Singer-Songwriter} UNION {?person a yago:Songwriter110624540} UNION {?person a yago:Writer110801291} UNION {?person a yago:Writer110794014} '
    where = where + " }"

    return  where 
    
def ask_function_compositeur(p):
    where = """ASK FROM """
    where = where+ str(p) + """   { """

    where = where  + '{?person a yago:Composer109947232} UNION {?person a dbo:composer} . '
    where = where + " }"
    return  where
    
def ask_function_interprete(p):
    where = """ASK FROM """
    where = where+ str(p) + """   { """

    where = where  + '{?person a dbo:Singer} UNION {?person a dbo:Singer-Songwriter} UNION  {?person a yago:Singer110599806} UNION {?person a yago:Performer110415638} '
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
                url = '<'+d['URL']+'>'
                nom_artiste = valeur
                ask_musicien = ask_function_musicien(url)
                print("ask_musicien ",ask_musicien)
                sparql.setQuery(ask_musicien)
                sparql.setReturnFormat(JSON)
                is_musicien =  bool(sparql.query().convert()['boolean'])
                print("is_musicien ",is_musicien)

                ask_auteur = ask_function_auteur(url)
                print("ask_auteur ",ask_auteur)
                sparql.setQuery(ask_auteur)
                sparql.setReturnFormat(JSON)
                is_auteur = bool(sparql.query().convert()['boolean'])
                print("is_auteur ",is_auteur)


                ask_compositeur =  ask_function_compositeur(url)
                print("ask_compositeur", ask_compositeur)
                sparql.setQuery(ask_compositeur)
                sparql.setReturnFormat(JSON)
                is_compositeur = bool( sparql.query().convert()['boolean'])
                print("is_compositeur ",is_compositeur) 
                
                ask_interprete = ask_function_interprete(url)
                print("ask_interprete ",ask_interprete)
                sparql.setQuery(ask_interprete)
                sparql.setReturnFormat(JSON)
                is_interprete =bool( sparql.query().convert()['boolean'])
                print("is_interprete ",is_interprete)

                f='artiste, '
                if is_musicien == 'musicien':
                    f=f+'musicien'

                
                if is_auteur == 'auteur':
                    if f=='artiste, ':
                        f=f+"auteur"
                    else:
                        f=f+", auteur"
            
                if is_compositeur == 'compositeur':
                    if f=='artiste, ':
                        f=f+"compositeur"
                    else:
                        f=f+", compositeur"


                if is_interprete == 'interprete':
                    if f=='artiste, ':
                        f=f+"interprète"
                    else:
                        f=f+", interprète"

                d["Fonction"] = f
        final_results.append(d)

    print("final_results ",final_results)
    return final_results