# Un essai  de gestionnaire d'arborescence.
import os, shutil
import lib_tree

class Observable:
    def __init__(self, initialValue=None):
        self.data = initialValue
        self.callbacks = {}

    def addCallback(self, func):
        print("passage par addCallback")
        self.callbacks[func] = 1

##    def delCallback(self, func):
##        del self.callback[func]

    def _docallbacks(self):
        for func in self.callbacks:
             print("passage par _docallbacks")
             print(self.callbacks)
             func(self.data)

    def set(self, data):
        print("passage par set")          
        self.data = data
        self._docallbacks()

    def get(self):
        print("passage par get") 
        return self.data

    def unset(self):
        print("passage par unset") 
        self.data = None

class FsHandler():
    def __init__(self, root="PRIVATE/"):
        self.root=root
        self.notification = Observable("")
        
    def bidon(self):
        print("passé par bidon")
        self.notification.set("OK bidon")

    def mkdir(self, name):
        """make a directory"""
        try:
            os.mkdir(os.path.join(self.root,name))
            self.notification.set("repertoire créé")
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
        self.requested_command = Observable("")

    def prt_menu(self):
        print("""

c) créer un répertoire essai
m) transférer un répertoire
s) Create a structure
l) list repertories
t) print tree 
q) quitter
""")
        return input("choix : ")
        
    def decode(self, key):
        return key
##            if key == "c":
##                name = input("Nom du répertoire : ")
##                self.requested_command.set(fs.mkdir, name)
##            if key == "b": # B comme BIDON
##                self.requested_command.set("b")
##            elif key == "m":
##                src = input("Origine : ")
##                dst = input("Destination : ")
##                fs.move_rep(src, dst)
##            elif key == "s":
##                name = input("Nom du répertoire : ")
##                fs.bm_mkdir(name)   
##            elif key == "l":
##                fs.prt_dir()
##            elif key == "t":
##                fs.prt_tree()
##            else:
##                print("Choix non prévu")
                
    def update(self):
        print("Quelqhe chose est nouveau")
    
                
class Controller():
    def __init__(self):
        self.model=FsHandler()
        self.view=Menu()
        self.model.notification.addCallback(self.updateview)
        self.mainloop()
        
    def mainloop(self):
        cont_while = True
        while cont_while:
            self.view.decode(self.view.prt_menu())
            key = self.view.requested_command.get()
            print("key", key)
            if key == "b":
                self.bidon()
            elif key == "t":
                self.prt_tree()
            else:
                print("Choix non prévu")            
                
    def updateview(self, a=None): # Je suis obligé de mettre ce second argument
        self.view.update()
        
    def bidon(self):
        print("Passage par controller.bidon()")
        self.model.bidon()            
        
    def mkdir(self, name):
        self.model.mkdir(name)

    def bm_mkdir(self, name_rep):
        self.model.bm_mkdir(name_rep)
        
    def prt_dir(self):
        self.model.prt_dir()
            
    def prt_tree(self):
        self.model.prt_tree()
       
    def move_rep(self, src, dst):
        self.model.move_rep(src, dst)
        
    def decode_view(self):       
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

if __name__ == '__main__':
##    fs = FsHandler()
##    fs.mkdir("tutu")
##    fs.bm_mkdir("tutu")
##    Menu()
    Controller()
