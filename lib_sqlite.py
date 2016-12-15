# -*- coding: utf-8 -*-
# Gestion des connexions à une base sqlite.
# Evolution : Remplacement de basDonn par con.


import sqlite3
import os, sys
import conf_file as Cf # fichier de parametrage avec nom de la base sqlite

class GestionBD:
    """Mise en place et interfaçage d'une base de données Sqlite."""

    def __init__(self, db_name=None, in_memory=False):
        "Établissement de la connexion et création du curseur"
        if in_memory:
            self.con = sqlite3.connect(':memory:')
            self.cur = self.con.cursor()   # création du curseur
            self.echec = 0           
        else:
            self.db_name = db_name
            # Vérifier que le fichier de DB existe
            if not os.path.isfile(db_name): 
                print("Error : Database file {} does not exist".format(db_name))   
            try:
                # IMPORTANT la connection est10 fois plus longue si le fichier 
                # est verrouillé en écriture.
                self.con = sqlite3.connect(db_name)
            except Exception as err:
                sys.stderr.write(('Connexion to database failed :\n'\
                      'SQL Error is :\n%s' % err))           
                self.echec = 1
            else:
                # print("Connexion OK") 
                self.cur = self.con.cursor()   # création du curseur
                self.echec = 0
    def creer_tables(self, dic_tables):
        "Création des tables décrites dans le dictionnaire <dic_tables>."
        for table in dic_tables:            # parcours des clés du dictionn.
            req = "CREATE TABLE %s (" % table
            pk =''
            for descr in dic_tables[table]:
                nomChamp = descr[0]        # libellé du champ à créer
                tch = descr[1]             # type de champ à créer
                if tch =='i':
                    typeChamp ='INTEGER'
                elif tch =='r':
                    typeChamp ='REAL'
                elif tch =='k':
                    # champ 'clé primaire' (entier incrémenté automatiquement)
                    #typeChamp ='SERIAL'
                    typeChamp ='INTEGER NOT NULL'
                    pk = nomChamp
                else:
                    typeChamp ='VARCHAR(%s)' % tch
                req = req + "%s %s, " % (nomChamp, typeChamp)
            if pk == '':
                req = req[:-2] + ")"
            else:
                req = req + "CONSTRAINT %s_pk PRIMARY KEY(%s))" % (pk, pk)
            self.executer_sql(req)
            print ("Fin de la création des tables")

    def supprimer_tables(self, dic_tables):
        "Suppression de toutes les tables décrites dans <dic_tables>"
        for table in list(dic_tables.keys()):
            req ="DROP TABLE %s" % table
            self.executerReq(req)
        self.commit()                       # transfert -> disque
        print ("Fin de la destruction des tables")
    def executer_sql(self, req, param =None):
        "Exécution de la requête <req>, avec détection d'erreur éventuelle."
        try:
            # obligé de faire cette bidouille infame ! Je dois améliorer le
			# passage des arguments
            if param == None :
                self.cur.execute(req)
            else:
                self.cur.execute(req, param)
        except sqlite3.Error as e:
            sys.stderr.write("An SQL error occurred: {}\n".format(e.args[0]))
            sys.stderr.write("Request was: {}\n".format(req))
            sys.stderr.write("Param  was: {}\n".format(param))
            return 0
        else:
            return 1

    def resultat_req(self):
        "renvoie le résultat de la requête précédente (une liste de tuples)"
        return self.cur.fetchall()

    def quick_sql(self, req):
       if self.executer_sql(req):
          # Afficher les noms de colonnes
          records=self.resultat_req()         # ce sera un tuple de tuples
          # TypeError: 'NoneType' object is not iterable
          try:
             for i in self.cur.description:
                 print(i[0], '|', end=' ')
             print()
          # afficher les résulats
             for rec in records:             # => chaque enregistrement
                for item in rec:            # => chaque champ dans l'enreg.
                  print(item, '|', end=' ')
                print()
                 # print("|".join(rec))
                
          except:
             print("Rien à afficher")
    def commit(self):
        # if self.con: # ??
        self.con.commit()         # transfert curseur -> disque

    def close(self):
        pass
        if self.con:
            self.con.close()
            # sys.stderr.write("Database {} has been closed\n".format(self.db_name))
class Enregistreur:
    """classe pour gérer l'entrée d'enregistrements divers"""
    def __init__(self, bd, table):
        self.bd =bd
        self.table =table
        self.descriptif =Glob.dicoTables[table]   # descriptif des champs

    def entrer(self):
        "procédure d'entrée d'un enregistrement entier"
        str_champs ="("           # ébauche de chaîne pour les noms de champs
        valeurs =[]           # liste pour les valeurs correspondantes
        # Demander successivement une valeur pour chaque champ :
        for cha, type, nom in self.descriptif:
            if type =="k":    # on ne demandera pas le n° d'enregistrement
                continue      # à l'utilisateur (numérotation auto.)
            str_champs = str_champs + cha + ","
            val = input("Entrez le champ %s :" % nom)
            if type =="i":
                val =int(val)
            valeurs.append(val)
        print(len(valeurs))

        balises ="(" + "?," * len(valeurs)       # balises de conversion

        str_donnees ="("       
        for valeur in valeurs:
             str_donnees=str_donnees + str(valeur)+','
        str_donnees=str_donnees[:-1] + ")"
        #str_donnees ="(" + valeurs +")"     # balises de conversion
        str_champs = str_champs[:-1] + ")"    # supprimer la dernière virgule,
        balises = balises[:-1] + ")"  # et ajouter une parenthèse
        req ="INSERT INTO %s %s VALUES %s" % (self.table, str_champs, balises)
        self.bd.executerReq(req, valeurs)

        ch =input("Continuer (O/N) ? ")
        if ch.upper() == "O":
            return 0
        else:
            return 1
        
if __name__ == '__main__': 
    print("Connexion à base de donnée")
    BASE = GestionBD(db_name=Cf.FACT_DB)
    if BASE.echec:
        print("Pb connexion")
    else:
        print("OK")
    BASE.quick_sql("Select 1,2,3 ")
    BASE.quick_sql("Select 456, 345")
    BASE.quick_sql("Select * from nabm WHERE ID = 126")

    # BASE.close()

    # Autre exemple avec une base en mémoire RAM.
    INRAM=GestionBD(in_memory=True)
    INRAM.quick_sql("Select 1,2,3 ")
    
