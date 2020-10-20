#TP1 DECOMPOSITION QR GRAM-SCHMIDT
from math import *
from random import *
import numpy as np
import matplotlib.pyplot as pp
import time
from fonctions_utiles import *

#-----------------DEFINITIONS----------------------------

def find_A_inv(n): #trouve une matrice A inversible de dimension (n, n)
    A = np.random.random_sample((n, n))
    if np.linalg.det(A) != 0:
        print("\nA est inversible et vaut\nA =\n", A)
    else:
        find_A_inv(n)
    return A

def DecompositionGS(A):#décompose la matrice A en deux matrices Q et R par la méthode de Gram-Schmidt
    Q = np.zeros(A.shape)
    for i in range(A.shape[1]):
        #processus d'orthogonalité
        aj = A[:, i]#on identifie les colonnes de A comme des vecteurs sur lesquelles on va travailler un par un
        qi = Q[:, :i] #colonnes calculées de Q
        rij = aj @ qi #produit scalaire formant la partie supérieure de R
        wj = aj - np.sum(rij * qi, axis=1) #vecteur dont les normes donnent la diago

        #processus de normalisation
        rjj = abs(np.sqrt(wj @ wj)) #calcul des composantes de la diagonale du vecteur orthogonal
        qj = wj / rjj
        Q[:, i] = qj 
    R = Q.T @ A
    print("\nQ =\n", Q)
    print("\nR =\n", R)
    
    return Q, R

    #QR alternatif
    '''n = A.shape 
    Q = np.zeros(n)
    R = np.zeros((A.shape[1], A.shape[1]))
    for i in range(0, A.shape[1]):
        wj = np.dot(A[:, i], A[:, i]) #revient à calculer A[:, i]-sum(R[i, j]*Q[:, i])
        R[i, i] = np.sqrt(wj)
        Q[:, i] = A[:, i]/R[i, i]
        for j in range(i+1, A.shape[1]):
            R[i, j] = np.dot(Q[:, i], A[:, j])
            A[:, j] = A[:, j] - np.dot(R[i, j],Q[:, i])
    print("\nQ =\n", Q)
    print("\nR =\n", R)
    return Q, R'''


def ResolGS(A, b): #résout une équation Ax = b par la décomposition QR 
    n, m = A.shape
    Q, R = DecompositionGS(A)
    Y = np.dot(Q.T, b)
    Aaug = np.concatenate((R,np.reshape(Y, (n,1))), axis = 1)
    
    n, m = np.shape(Aaug)
    x = np.zeros(n)
    for i in range(n-1, -1, -1): 
        somme = 0
        for k in range(i,n):
            somme = somme + x[k]*Aaug[i,k]
        x[i] = (Aaug[i, n] - somme) / Aaug[i, i]
    print('\nx =\n', np.reshape(x, (n,1)))
    return np.reshape(x, (n,1))

def verif(A, x, b): #permet de vérifier si x est bien solution de Ax = b
    print("\n b=\n", b)
    print("\n A*x=\n", np.ravel(np.dot(A, x)))

def courbe(dim, time_qr, time_gauss, time_cholesky): #affiche les courbes 
    x, y, y2, y3 = [], [], [], []
    for i in range(len(dim)):
        x.append(np.array([dim[i]]))
        y.append(np.array([time_qr[i]]))
        y2.append(np.array([time_gauss[i]]))
        y3.append(np.array([time_cholesky[i]]))
    pp.plot(x, y, label = "par QR")
    pp.plot(x, y2, label = "par Gauss")
    pp.plot(x, y3, label = "par Cholesky")
    pp.xlabel('taille de la matrice A')
    pp.ylabel('temps de calcul (s)')
    pp.title('Temps de résolution en fonction de la dimension de A')
    pp.legend()
    pp.show()

def experimentation_methodes():
    dim = [3, 10, 100, 200, 300, 400, 500, 600, 700, 800, 900, 1000]
    time_qr, time_gauss, time_cholesky = [], [], []
    for i in range(len(dim)):
        taille = dim[i]
        #processus pour QR
        A = Trouver_A(dim[i])
        n = A.shape
        B= np.random.randint(10, size =(dim[i], 1))
        t0 = time.time()
        [Q, R] = DecompositionGS(A)
        ResolGS(A, B)
        t1 = time.time()
        time_qr.append(t1-t0)
        #processus pour Gauss
        print('A =', A)
        print('B =', B)
        print(np.concatenate((A, B), axis = 1))
        dt = gauss(A, B)
        time_gauss.append(dt)
        #processus pour Cholesky
        dt = ResolCholesky(A, B)
        time_cholesky.append(dt)    
    courbe(dim, time_qr, time_gauss, time_cholesky)
    
'''
#question1
print("\nEXERCICE 1\n")
A = np.array([[6.0, 6.0, 16.0], [-3.0, -9.0, -2.0], [6.0, -6.0, -8.0]])
print("A =\n", A)
DecompositionGS(A)
#question2
print("\nQUESTION 2")
n = 3
A = find_A_inv(n)
b=np.ravel(np.random.randint(10, size =(n, 1))).T
print("\nb =\n", b)
print("\nrésultat x =\n", ResolGS(A,b))
verif(A, ResolGS(A,b), b)#parfois donne des valeurs dont l'écart est infinitésimal, à expliquer
'''
