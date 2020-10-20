from math import *
import numpy as np
import scipy
import scipy.linalg
import pprint
import time
from random import *
import matplotlib.pyplot as pp


#--------------------------------------DEFINITIONS--------------------------------------------------

#cette définition permet de créer une matrice A définie positive de manière certaine
def Trouver_A(dim):
    M =  np.random.random_sample((dim, dim))
    if np.linalg.det(M) !=0 :
        print("\nA est inversible et vaut\nA =\n", M)
        return np.dot(M.T, M)
    else:
        Trouver_A(dim)
        
        
    
#cette définition permet de vérifier si une matrice A générée de manière aléatoire est définie positive    
def Conditions(A):
    if np.linalg.det(A) == 0:
        print("\ndet(A) = ", round(np.linalg.det(A), 3), "alors A n'est pas inversible et Cholesky n'est pas applicable")
        A_NDC.append(A)
        return round(np.linalg.det(A), 3)
    else:
        print("\ndet(A) = ", round(np.linalg.det(A), 3), "alors A est inversible, cherchons la deuxième condition\n")
        
        valprop = np.reshape(np.linalg.eigvals(A), (dim, 1))
        print('Matrice des valeurs propres =\n', valprop)

        for i in range(dim):
            if valprop[i] < 0:
                print("\nToutes les valeurs propres ne sont pas strictement positives donc Cholesky n'est pas applicable")
                A_NDC.append(A)
                return valprop[i]
                
                
        print("\nToutes les valeurs propres sont strictement positives donc Cholesky est applicable\n")
        A_SDP.append(A)
    
#cette définition effectue la décomposition par Cholesky             
def Cholesky(A):
    n,c = np.shape(A)
    L = np.zeros((n,c))
    for k in range(0, n):
        somme = 0
        for j in range(0, k):
            somme = somme + L[k,j]**2
        L[k,k] = (A[k,k] - somme)**0.5
        for i in range(k+1, n):
            somme = 0
            for j in range(0, k):
                somme = somme + L[i,j]*L[k,j]
            L[i,k] = (A[i,k] - somme)/L[k,k]  
    LT = L.T
    return L, LT
    

#cette définition permet de résoudre une équation de la forme AX = B par Cholesky
def ResolCholesky(A, B):
    t0 = time.time()
    [L, LT]= Cholesky(A)
    '''P, L, LT = scipy.linalg.lu(A)'''
    Aaug = np.concatenate((L, B), axis = 1)
    n, m = np.shape(Aaug)
    Y = res_low(Aaug)
    Y = np.reshape(res_low(Aaug), (n, 1))
    Aaug = np.concatenate((LT, Y), axis = 1)
    X = res(Aaug)
    t1 = time.time()
    dt = t1-t0
    return dt

#cette définition trace la courbe du temps de calcul en fonction de la dimension
'''def courbe(temps_chol, temps_gauss, temps_chol_alt, time_qr, dim):
    #courbe avec cholesky
    x, x2, x3, x4, y, y2, y3, y4 = [], [], [], [], [], [], [], []
    for i in range(len(dim)):
        x.append(np.array([dim[i]]))
        y.append(np.array([temps_chol[i]]))
    pp.plot(x, y, label = 'par Cholesky')
    #courbe avec gauss
    for i in range(len(dim)):
        x2.append(np.array([dim[i]]))
        y2.append(np.array([temps_gauss[i]]))
    pp.plot(x2, y2, label = 'par Gauss')
    #courbe avec cholesky alternatif
    for i in range(len(dim)):
        x3.append(np.array([dim[i]]))
        y3.append(np.array([temps_chol_alt[i]]))
    pp.plot(x3, y3, label = 'par Cholesky alternatif')
    #courbe avec qr
    for i in range(len(dim)):
        x4.append(np.array([dim[i]]))
        y4.append(np.array([time_qr[i]]))
    pp.plot(x4, y4, label = "par QR de Gram-Schmidt")
    pp.xlabel('dimension')
    pp.ylabel('temps (s)')
    pp.legend()
    pp.show()

#cette définition trace la courbe de l'erreur en fonction de la dimension
def courbe2(erreur_chol, erreur_gauss, dimension):
    #courbe avec cholesky
    x = []
    y = []
    for i in range(len(dimension)):
        x.append(np.array([dimension[i]]))
        y.append(np.array([erreur_chol[i]]))
    pp.plot(x, y, label = 'par Cholesky')

    #courbe avec gauss
    x2 = []
    y2 = []
    for i in range(len(dimension)):
        x2.append(np.array([dimension[i]]))
        y2.append(np.array([erreur_gauss[i]]))
    pp.plot(x2, y2, label = 'par Gauss')

    pp.xlabel('dimension')
    pp.ylabel('erreur')
    pp.legend()
    pp.show()
'''  
#-----------------FROM TP1---------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------
    
def rg(Aaug):
    n,m = np.shape(Aaug) #retourne les lignes et colonnes (la dimension)
    for k in range(0, n-1):
        for i in range(k+1, n):
            gik = Aaug[i, k]/Aaug[k,k]
            Aaug[i, :] = Aaug[i, :] - gik*Aaug[k, :]
    return Aaug

def res(Aaug):
    n, m = np.shape(Aaug)
    X = np.zeros(n)
    for i in range(n-1, -1, -1): 
        somme = 0
        for k in range(i,n):
            somme = somme + X[k]*Aaug[i,k]
        X[i] = (Aaug[i, n] - somme) / Aaug[i, i]
    return X

def res_low(Aaug):
    n, m = np.shape(Aaug)
    Y = np.zeros(n)
    for i in range(0, n): 
        somme = 0
        for k in range(0,n):
            somme = somme + Y[k]*Aaug[i,k]
        Y[i] = (Aaug[i, n] - somme) / Aaug[i, i]
    return Y
         
def gauss(A, B):
    Aaug = np.concatenate((A, B), axis = 1)
    t0 = time.time()
    Baug = rg(Aaug)
    X = res(Baug)
    t1 = time.time()
    dt = t1-t0
    return dt

def Cholesky_alt(A, B):
    n,m = np.shape(A)
    L=np.eye(n) 
    D=np.eye(n)
    for k in range (n):
        somme = 0
        for j in range (k):
            somme = somme+L[k,j ]**2* D[j,j]
        D[k,k]=A[k,k]- somme
        for i in range (k+1,n):
            somme = 0
            for j in range (k):
                somme = somme +L[i,j]*L[k,j]*D[j,j]
            L[i,k]=(A[i,k]- somme )/D[k,k]
            
    print('\nL =\n', L, '\n\nD =\n', D, '\n\nLT =\n', L.T)
    Aaug = np.concatenate((L, B), axis = 1)
    Z = np.reshape(res(Aaug), (n, 1))
    Aaug = np.concatenate((D, Z), axis = 1)
    Y = np.reshape(res(Aaug), (n, 1))
    Aaug = np.concatenate((L.T, Y), axis = 1)
    X = np.reshape(res_low(Aaug), (n, 1))
    print('\nX =\n', X)
    return X
    
