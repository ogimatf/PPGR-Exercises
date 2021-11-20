import numpy as np
import math
import statistics

import pygame as pg
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

#pravljenje jednacine
def jed(a, b):
    
    a1 = a[0]
    a2 = a[1]
    a3 = a[2]
    
    b1 = b[0]
    b2 = b[1]
    b3 = b[2]
    
    return np.array([a1*b1, a2*b1, a3*b1, a1*b2, a2*b2, a3*b2, a1*b3, a2*b3, a3*b3])

#pravljenje matrice od jednacina za sve korespodencije
def matrica_8x9(xx, yy):
    
    n = len(xx)
    
    jed8 = [jed(xx[0], yy[0])]
    
    for i in range(1, n):
        
        jed8.append(jed(xx[i], yy[i]))
        
    jed8 = np.array(jed8)
    
    jed8 = np.stack(jed8)
        
    return jed8

#matrica vektorskog mnozenja, kao kod rodrigeza
def vec(p):
    
    p1 = p[0]
    p2 = p[1]
    p3 = p[2]
    
    P = np.zeros((3,3), dtype='float')
    
    P[0][1] = -p3
    P[0][2] = p2
    P[1][0] = p3
    P[1][2] = -p1
    P[2][0] = -p2
    P[2][1] = p1
    
    return P

def jednacine(x, y, T1, T2):
    
    j = []
    j.append(x[1]*T1[2] - x[2]*T1[1])
    j.append(-x[0]*T1[2] + x[2]*T1[0])
    j.append(y[1]*T2[2] - y[2]*T2[1])
    j.append(-y[0]*T2[2] + y[2]*T2[0])
    
    return np.array(j)

def UAfine(x):
    
    #za np array
    xp = x / x[3]
    xp = xp[:-1]
    
    return xp

#vraca 3d koordinate rekonstruisane tacke
def TriD(x, y, T1, T2):
    
    u, t, v = np.linalg.svd(jednacine(x, y, T1, T2))
    
    return UAfine(np.dot(jednacine(x, y, T1, T2), v[3]))

x1 = [1960.0, 650.0, 1.0]
x2 = [2305.0, 750.0, 1.0]
x3 = [1680.0, 1000.0, 1.0]
x4 = [1350.0, 895.0, 1.0]
x9 = [805.0, 1770.0, 1.0]
x10 = [1890.0, 2075.0, 1.0]
x11 = [1850.0, 2370.0, 1.0]
x12 = [825.0, 2000.0, 1.0]

y1 = [2175.0, 430.0, 1.0]
y2 = [2445.0, 620.0, 1.0]
y3 = [1505.0, 815.0, 1.0]
y4 = [1310.0, 590.0, 1.0]
y9 = [760.0, 1400.0, 1.0]
y10 = [1470.0, 2010.0, 1.0]
y11 = [1450.0, 2265.0, 1.0]
y12 = [790.0, 1600.0, 1.0]


xx = np.array([x1, x2, x3, x4, x9, x10, x11, x12])
yy = np.array([y1, y2, y3, y4, y9, y10, y11, y12])

np.set_printoptions(suppress = True)

jed8 = matrica_8x9(xx, yy)
#print(jed8)

u_j8, d_j8, v_j8 = np.linalg.svd(jed8)
#print(np.round(u_j8, 6), "\n\n", np.round(d_j8, 6), "\n\n", np.round(v_j8, 6), "\n\n")

np.set_printoptions(suppress = False)
Fvector = v_j8[8]
#print(Fvector)

FF = Fvector.reshape(3, 3)
#print(FF, "\n\n", np.linalg.det(FF))

np.set_printoptions(suppress = True)
U, D, V = np.linalg.svd(FF)
#print(np.round(U, 6), "\n\n", np.round(D, 6), "\n\n", np.round(V, 6), "\n\n")

e1 = V[2]
e1 = (1 / e1[2]) * e1
#print(np.round(e1, 2))

e2 = np.transpose(U)[2]
e2 = (1 / e2[2]) * e2
#print(np.round(e2, 2))

#Rekonstrukcija skrivenih tacaka
# x6 = [1094.0, 536.0, 1.0]
# y6 = [980.0, 535.0, 1.0]

# x7 = [862.0, 729.0, 1.0]
# y7 = [652.0, 638.0, 1.0]

# x8 = [710.0, 648.0, 1.0]
# y8 = [567.0, 532.0, 1.0]

# x14 = [1487.0, 598.0, 1.0]
# y14 = [1303.0, 700.0, 1.0]

# x15 = [1462.0, 1072, 1.0]
# y15 = [1257.0, 1165.0, 1.0]

# y13 = [1077.0, 269.0, 1.0]

x6 = [2300.0, 1430.0, 1.0]
x7 = [1740.0, 1755.0, 1.0]
x8 = [1420.0, 1590.0, 1.0]
x14 = (2560.0, 1210.0, 1.0)
x15 = [2550.0, 1455.0, 1.0]

y6 = [2395.0, 1360.0, 1.0]
y7 = [1575.0, 1600.0, 1.0]
y8 = [1400.0, 1345.0, 1.0]
y14 = [2870.0, 1180.0, 1.0]
y15 = [2810.0, 1430.0, 1.0]

x5 = np.cross(np.cross(np.cross(np.cross(x4, x8), np.cross(x6, x2)), x1), 
             np.cross(np.cross(np.cross(x1, x4), np.cross(x3, x2)), x8))
x5 = np.round(x5 / x5[2])
#print(x5)

x13 = np.cross(np.cross(np.cross(np.cross(x9, x10), np.cross(x11, x12)), x14), 
             np.cross(np.cross(np.cross(x11, x15), np.cross(x10, x14)), x9))
x13 = np.round(x13 / x13[2])

x16 = np.cross(np.cross(np.cross(np.cross(x10, x14), np.cross(x11, x15)), x12), 
             np.cross(np.cross(np.cross(x9, x10), np.cross(x11, x12)), x15))
x16 = np.round(x16 / x16[2])

y5 = np.cross(np.cross(np.cross(np.cross(y4, y8), np.cross(y6, y2)), y1), 
             np.cross(np.cross(np.cross(y1, y4), np.cross(y3, y2)), y8))
y5 = np.round(y5 / y5[2])

y16 = np.cross(np.cross(np.cross(np.cross(y10, y14), np.cross(y11, y15)), y12), 
             np.cross(np.cross(np.cross(y9, y10), np.cross(y11, y12)), y15))
y16 = np.round(y16 / y16[2])

y13 = np.cross(np.cross(np.cross(np.cross(y9, y10), np.cross(y11, y12)), y14), 
             np.cross(np.cross(np.cross(y11, y15), np.cross(y10, y14)), y9))
y13 = np.round(y13 / y13[2])


#Trianglucija
T1 = np.eye(3, 4, dtype = 'float')
#print(T1)

E2 = vec(e2)
#print(np.round(E2, 2))

T2 = np.dot(E2, FF)
T2 = np.append(T2, e2.reshape(3,1), axis = 1)
#print(T2)

#u, t, v = np.linalg.svd(jednacine(x1, y1, T1, T2))
# print(v[3], jednacine(x1, y1, T1, T2))
# print(np.dot(jednacine(x1, y1, T1, T2), v[3]))

slika1 = [x1, x2, x3, x4, x5, x6, x7, x8, x9, x10, x11, x12, x13, x14, x15, x16]
slika2 = [y1, y2, y3, y4, y5, y6, y7, y8, y9, y10, y11, y12, y13, y14, y15, y16]

#rekonstruisemo 3d koordinate
n = len(slika1)

rekonstruisane = []

for i in range(n):    
    rekonstruisane.append(TriD(slika1[i], slika2[i], T1, T2))

rekonstruisane = np.array(rekonstruisane)
#print(rekonstruisane, "\n")

#za skaliranje z ose, jer nismo radili normalizaciju
dijag_matrica = np.diag([1, 1, 400])    
    
rekonstruisane400 = []

slika1_400 = np.array(slika1)
for i in slika1_400:
    i[2] *= 400

slika2_400 = slika2
for i in slika2_400:
    i[2] *= 400

for i in range(n):
    rekonstruisane400.append(TriD(slika1_400[i], slika2_400[i], T1, T2))

rekonstruisane400 = np.array(rekonstruisane400)
print(rekonstruisane400, "\n")

################################################################################################

#iscrtavanje kocke

def tacka(x):

    return (x[0], x[1], x[2])

def nacrtaj_pravougaonik(x1, x2, x3, x4):

    a = tacka(x1)
    b = tacka(x2)
    c = tacka(x3)
    d = tacka(x4)

    glBegin(GL_LINES)
    
    glVertex3fv(a)
    glVertex3fv(b)

    glVertex3fv(b)
    glVertex3fv(c)

    glVertex3fv(c)
    glVertex3fv(d)

    glVertex3fv(d)
    glVertex3fv(a)

    glEnd()

    

centerX = statistics.mean(x[0] for x in rekonstruisane400)
centerY = statistics.mean(x[1] for x in rekonstruisane400)
centerZ = statistics.mean(x[2] for x in rekonstruisane400)

pg.init()
display = (1200, 800)
pg.display.set_mode(display, DOUBLEBUF|OPENGL)

gluPerspective(45, (display[0]/display[1]), 0.1, 10000.0)

gluLookAt(0, 0, 800, 0, 0, 0 , 1, 0, 0)

while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            quit()

    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

    glTranslate(-centerX , -centerY , -centerZ)
    
    #Gornji kvadar
    glColor3f(1,1,1)
    nacrtaj_pravougaonik(rekonstruisane400[0], rekonstruisane400[1], rekonstruisane400[2], rekonstruisane400[3])
    nacrtaj_pravougaonik(rekonstruisane400[1], rekonstruisane400[5], rekonstruisane400[6], rekonstruisane400[2])
    nacrtaj_pravougaonik(rekonstruisane400[4], rekonstruisane400[5], rekonstruisane400[6], rekonstruisane400[7])
    nacrtaj_pravougaonik(rekonstruisane400[0], rekonstruisane400[4], rekonstruisane400[7], rekonstruisane400[3])

    #Donji kvadar
    glColor3f(1,0,0)
    nacrtaj_pravougaonik(rekonstruisane400[12], rekonstruisane400[13], rekonstruisane400[9], rekonstruisane400[8])
    nacrtaj_pravougaonik(rekonstruisane400[15], rekonstruisane400[14], rekonstruisane400[10], rekonstruisane400[11])
    nacrtaj_pravougaonik(rekonstruisane400[9], rekonstruisane400[13], rekonstruisane400[14], rekonstruisane400[10])
    nacrtaj_pravougaonik(rekonstruisane400[8], rekonstruisane400[12], rekonstruisane400[15], rekonstruisane400[11])
   
    glTranslate(centerX , centerY , centerZ)

    pg.display.flip()
    pg.time.wait(50)