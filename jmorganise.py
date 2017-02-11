# Un essai

import os, shutil
import lib_tree

class FsHandler():
    def __init__(self, root="PRIVATE/"):
        self.root=root

    def mkdir(self, name):
        """make a directory"""
        try:
            os.mkdir(os.path.join(self.root,name))
        except:
            print("Impossible de créer '%s'" % name)
    def bm_mkdir(self, name_rep):
        """create working repertories in rep"""
        rep = os.path.join(self.root, name_rep)
        
        for subrep in ["1)_data", "2)_methode", "3)_travail",
                       "4)_sources","5)_modeles", "6)_ameliorations"]:
            try:
               subrep_name = os.path.join(rep, subrep)
               os.mkdir(subrep_name)
            except:
                print("Impossible de créer l'arborescence dans '%s'" % rep)
    def prt_dir(self):
        """print directory"""
        for item in os.listdir(self.root):
            print(item)
            
    def prt_tree(self):
        lib_tree.tree(self.root, " ", True)
       
    def move_rep(self, src, dst):
        """Move teh content of a repertory to another. Leave a message in the empty repertory."""
        # import pdb
        src = os.path.join(self.root, src)
        dst = os.path.join(self.root, dst)
        # rep_src = os.path.dirname(src)
        # pdb.set_trace()
        for item in os.listdir(src):
            print(item)
            # print(rep_src+item)
            shutil.move(os.path.join(src,item), dst)

        with open (src+"/memo.txt", mode='w') as f:
            f.write("contenu déplacé dans : %s" % dst)
            

class Menu():
    def __init__(self):
        key = ""
        while  key != "q":
            
            print("""

c) créer un répertoire essai
m) transférer un répertoire
s) Create a structure
l) list repertories
t) print tree 
q) quitter
""")
            fs = FsHandler()
            key = input("choix : ")

            if key == "c":
                name = input("Nom du répertoire : ")
                
                fs.mkdir(name)
            elif key == "m":
                src = input("Origine : ")
                dst = input("Destination : ")
                fs.move_rep(src, dst)
            elif key == "s":
                name = input("Nom du répertoire : ")
                fs.bm_mkdir(name)   
            elif key == "l":
                fs.prt_dir()
            elif key == "t":
                fs.prt_tree()
            else:
                print("Choix non prévu")
                
class Controller():
    def __init__(self):
        self.model=FsHandler()
        self.view1=Menu()
        
    def mkdir(self, name):
        self.model.mkdir(name)

    def bm_mkdir(self, name_rep):
        self.model.bm_mkdir(name_rep)
    def prt_dir(self):
        """print directory"""
        for item in os.listdir(self.root):
            print(item)
            
    def prt_tree(self):
        lib_tree.tree(self.root, " ", True)
       
    def move_rep(self, src, dst):
        pass

     
if __name__ == '__main__':
    
    Controller()
##    fs = FsHandler()
##    fs.mkdir("tutu")
##    fs.bm_mkdir("tutu")
##    Menu()

