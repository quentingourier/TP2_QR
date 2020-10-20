from tkinter import *
from tp2 import *

def genA():
    print('\n----------------------------------------------------------------------------------------------------')
    print('----------------------------------------------------------------------------------------------------\n')
    taille = int(saisie.get())
    A = Trouver_A(taille)
    return A

def decomposition():
    taille = int(saisie.get())
    A = genA()
    [Q, R] = DecompositionGS(A)
    return Q, R

def resolution():
    taille = int(saisie.get())
    A = genA()
    b=np.ravel(np.random.randint(10, size =(taille, 1))).T
    print("\nb =\n", b)
    ResolGS(A, b)

def experimentation():
    experimentation_methodes()
    
def kill():
    window.destroy()

def info():
    win = Toplevel(window)
    win.title('INFO')
    win.resizable(False, False)
    labelfont3 = ('bodoni MT', 12)
    def kill2():
        win.destroy()
    file = open('aide.txt', 'r')
    text = file.readlines()
    display = ''
    F = StringVar()
    for i in text:
        display = display + i + '\n'
    F.set(display)
    infotext = Label(win, textvariable = F)
    infotext.grid(row = 1, column = 1)
    back = Button(win, text = 'Retour', command = kill2)
    back.grid(row = 2, column = 1)
    back.config(font = labelfont3, fg='white', bg='red')
    
window = Tk()
window.geometry('610x275+600+350')
window.title('TP2')
window.resizable(False, False)
labelfont = ('copperplate gothic bold', 14)
labelfont2 = ('bodoni MT', 13)

titre = Label(window, text = 'Ma 313 - Algèbre linéaire numérique (2020-2021)\nTP2 - Décomposition QR et algorithme de Gram-Schmidt\n')
titre.grid(row= 0, column = 1, columnspan = 5, sticky = E+W)
titre.config(font = labelfont)

blanc = Label(window, text = '')
blanc.grid(row= 3, columnspan = 1)
blanc2 = Label(window, text = '')
blanc2.grid(row= 5, columnspan = 1)
blanc3 = Label(window, text = '')
blanc3.grid(row= 7, columnspan = 1)

dimension = Label(window, text = '                                Taille de la matrice       =')
dimension.grid(row = 1, rowspan = 2, column = 1, columnspan = 2)
dimension.config(font = labelfont2)

saisie = Entry(window)
saisie.grid(row =  2, column = 3)
saisie.focus_force()
saisie.config(font = labelfont2, width = 6)

trouverA = Button(window, text = 'Générer A', command = genA)
trouverA.grid(row = 4, column = 1)
trouverA.config(font = labelfont2)

decompo = Button(window, text = 'Décomposition QR', command = decomposition)
decompo.grid(row = 4, column = 2, columnspan = 2)
decompo.config(font = labelfont2)

resol = Button(window, text = 'Résolution Ax = b', command = resolution)
resol.grid(row = 4, column = 4)
resol.config(font = labelfont2)

expe = Button(window, text = 'Expérimentation des méthodes', command = experimentation)
expe.grid(row = 6, column = 2, columnspan = 2)
expe.config(font = labelfont2, width = 30)

quitter = Button(window, text = 'Quitter', command = kill)
quitter.grid(row = 8, column = 1)
quitter.config(font = labelfont2)

aide = Button(window, text = 'Aide', command = info)
aide.grid(row = 8, column = 4)
aide.config(font = labelfont2)



window.mainloop()
