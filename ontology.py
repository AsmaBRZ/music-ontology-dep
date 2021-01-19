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

equivalence =  {"birthP":"Place de naissance","birthD":"Date de naissance", "group":"URL","person":"URL", "name":"Nom", "dateC":"Date de création","origin":"Pays"}
def artiste_query(name,birthD,birthP, musicien, auteur, compositeur, interprete):
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
    
def displayResult(v_nom, v_date, v_place, musicien, auteur, compositeur, interprete):
    global texte1
    global texte0
    date_artiste = v_date
    nom_artiste = v_nom


    sparql = SPARQLWrapper("http://dbpedia.org/sparql")
    

    query=artiste_query(nom_artiste,date_artiste, lieu_artiste, musicien, auteur, compositeur, interprete)

    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()['results']['bindings']

    d = {}
    for result in results :
        for key,value in result.items():
            attribut = equivalence[key]
            valeur = value['value']
            if(key == 'birthP'):
                valeur = value['value'].split("/")[-1]
            d[str(attribut)] = str(valeur)

    return d