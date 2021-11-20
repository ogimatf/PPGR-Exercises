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

x2 = [950.0, 159.0, 1.0]
y2 = [811.0, 560.0, 1.0]

x4 = [855.0, 78.0, 1.0]
y4 = [1014.0, 490.0, 1.0]

x7 = [949.0, 319.0, 1.0]
y7 = [863.0, 823.0, 1.0]

x9 = [322.0, 344.0, 1.0]
y9 = [297.0, 73.0, 1.0]

x15 = [525.0, 486.0, 1.0]
y15 = [272.0, 360.0, 1.0]

x18 = [432.0, 763.0, 1.0]
y18 = [135.0, 320.0, 1.0]

x20 = [547.0, 252.0, 1.0]
y20 = [743.0, 348.0, 1.0]

x23 = [805.0, 489.0, 1.0]
y23 = [532.0, 647.0, 1.0]

xx = np.array([x2, x4, x7, x9, x15, x18, x20, x23])
yy = np.array([y2, y4, y7, y9, y15, y18, y20, y23])

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
x1 = [814.0, 111.0, 1.0]
y1 = [912.0, 447.0, 1.0]

x3 = [988.0, 123.0, 1.0]
y3 = [919.0, 612.0, 1.0]

x5 = [791.0, 304.0, 1.0]

x6 = [912.0, 358.0, 1.0]
y6 = [773.0, 772.0, 1.0]

y8 = [956.0, 700.0, 1.0]

x10 = [452.0, 368.0, 1.0]
y10 = [251.0, 119.0, 1.0]

x11 = [510.0, 270.0, 1.0]
y11 = [371.0, 137.0, 1.0]

x12 = [386.0, 249.0, 1.0]
y12 = [414.0, 88.0, 1.0]

x13 = [365.0, 559.0, 1.0]

x14 = [477.0, 583.0, 1.0]
y14 = [287.0, 325.0, 1.0]

y16 = [433.0, 289.0, 1.0]

x17 = [139.0, 554.0, 1.0]
y17 = [863.0, 823.0, 1.0]

x19 = [816.0, 380.0, 1.0]
y19 = [529.0, 529.0, 1.0]

x21 = [175.0, 655.0, 1.0]

x22 = [449.0, 862.0, 1.0]
y22 = [162.0, 428.0, 1.0]

y24 = [735.0, 456.0, 1.0]


x8 = np.cross(np.cross(np.cross(np.cross(x1, x4), np.cross(x2, x3)), x5), 
             np.cross(np.cross(np.cross(x5, x1), np.cross(x7, x3)), x4))
x8 = np.round(x8 / x8[2])

x16 = np.cross(np.cross(np.cross(np.cross(x9, x13), np.cross(x15, x11)), x12), 
             np.cross(np.cross(np.cross(x12, x9), np.cross(x10, x11)), x13))
x16 = np.round(x16 / x16[2])

x24 = np.cross(np.cross(np.cross(np.cross(x20, x17), np.cross(x19, x18)), x21), 
             np.cross(np.cross(np.cross(x17, x21), np.cross(x19, x23)), x20))
x24 = np.round(x24 / x24[2])

y5 = np.cross(np.cross(np.cross(np.cross(y2, y6), np.cross(y4, y8)), y1), 
             np.cross(np.cross(np.cross(y1, y2), np.cross(y8, y7)), y6))
y5 = np.round(y5 / y5[2])

y13 = np.cross(np.cross(np.cross(np.cross(y10, y14), np.cross(y12, y16)), y9), 
             np.cross(np.cross(np.cross(y9, y10), np.cross(y15, y16)), y14))
y13 = np.round(y13 / y13[2])

y17 = np.cross(np.cross(np.cross(np.cross(y19, y20), np.cross(y23, y24)), y18), 
             np.cross(np.cross(np.cross(y18, y19), np.cross(y22, y23)), y20))
y17 = np.round(y17 / y17[2])

y21 = np.cross(np.cross(np.cross(np.cross(y22, y23), np.cross(y18, y19)), y24), 
             np.cross(np.cross(np.cross(y23, y24), np.cross(y20, y19)), y22))
y21 = np.round(y21 / y21[2])

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

slika1 = [x1, x2, x3, x4, x5, x6, x7, x8, x9, x10, x11, x12, x13, x14, x15, x16, x17, x18, x19, x20, x21, x22, x23, x24]
slika2 = [y1, y2, y3, y4, y5, y6, y7, y8, y9, y10, y11, y12, y13, y14, y15, y16, y17, y18, y19, y20, y21, y22, y23, y24]

#rekonstruisemo 3d koordinate
n = len(slika1)

rekonstruisane = []

for i in range(n):    
    rekonstruisane.append(TriD(slika1[i], slika2[i], T1, T2))

rekonstruisane = np.array(rekonstruisane)
#print(rekonstruisane, "\n")

#za skaliranje z ose, jer nismo radili normalizaciju, nisam koristio matricu, mnozio sam samo trecu koordinatu dole
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

#steluje se gledanje
gluLookAt(0, 0, 500, 0, 0, 0 , 1, 5, 0)

while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            quit()

    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

    glTranslate(-centerX , -centerY , -centerZ)
    
    #Bevita
    glColor3f(1,1,0)
    nacrtaj_pravougaonik(rekonstruisane400[0], rekonstruisane400[1], rekonstruisane400[2], rekonstruisane400[3])
    nacrtaj_pravougaonik(rekonstruisane400[1], rekonstruisane400[5], rekonstruisane400[6], rekonstruisane400[2])
    nacrtaj_pravougaonik(rekonstruisane400[4], rekonstruisane400[5], rekonstruisane400[6], rekonstruisane400[7])
    nacrtaj_pravougaonik(rekonstruisane400[3], rekonstruisane400[0], rekonstruisane400[4], rekonstruisane400[7])

    #Caj
    glColor3f(0,1,0)
    nacrtaj_pravougaonik(rekonstruisane400[12], rekonstruisane400[13], rekonstruisane400[9], rekonstruisane400[8])
    nacrtaj_pravougaonik(rekonstruisane400[15], rekonstruisane400[14], rekonstruisane400[10], rekonstruisane400[11])
    nacrtaj_pravougaonik(rekonstruisane400[9], rekonstruisane400[13], rekonstruisane400[14], rekonstruisane400[10])
    nacrtaj_pravougaonik(rekonstruisane400[8], rekonstruisane400[12], rekonstruisane400[15], rekonstruisane400[11])

    #Ruter
    glColor3f(0,0,1)
    nacrtaj_pravougaonik(rekonstruisane400[16], rekonstruisane400[17], rekonstruisane400[18], rekonstruisane400[19])
    nacrtaj_pravougaonik(rekonstruisane400[20], rekonstruisane400[21], rekonstruisane400[22], rekonstruisane400[23])
    nacrtaj_pravougaonik(rekonstruisane400[16], rekonstruisane400[17], rekonstruisane400[21], rekonstruisane400[20])
    nacrtaj_pravougaonik(rekonstruisane400[19], rekonstruisane400[18], rekonstruisane400[22], rekonstruisane400[23])
   
    glTranslate(centerX , centerY , centerZ)

    pg.display.flip()
    pg.time.wait(50)