# file : conf_file.py
# Fichier de configuration

# Nom de la base de données
FACT_DB = "fact_db.sqlite"

# Où enregistrer les résultats
EXPORT_REP = "PRIVATE/"

    
# Structure de la base de données.

dico_tables ={
"anomaly":[
('id', "k", "clé primaire"),
('title', 25, "Titre"),
('creation_date', 10, "date de création"),
('closure_date', 10, "date de cloture"),
('description',6,""),
('solution', 255, ""),
('rem',500,"Remarque")],

"action":[
('id', "k", "clé primaire"),
('title', 25, "Titre"),
('creation_date', 10, "date de création"),
('closure_date', 10, "date de cloture"),
('description',6,"Descriptio de l'action"),
('rem',500,"Remarque")]
}
