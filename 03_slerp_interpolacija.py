import math
import numpy as np

import matplotlib.pyplot as plt
import matplotlib.animation as animation

from mpl_toolkits.mplot3d import axes3d

#normalizacija na jedinicini vektor
def normalize(v):
    
    norm = np.linalg.norm(v)
    
    if(norm == 0):
        return v
    else:
        return v / norm

#funkcija kojom izometriju A predstavljamo rotacijom oko prave p za ugao fi
def AxisAngle(A):
    
    Ap = A - np.eye(3, dtype='float')

    if(Ap[0][0] == Ap[1][0] and Ap[0][1] == Ap[1][1] and Ap[0][2] == Ap[1][2]):
        p = np.cross(Ap[0], Ap[2])
    else:
        p = np.cross(Ap[0], Ap[1])
        
    #racunanje normalnog vektora 
    u = [0, 0, 0]
    u[0] = p[1]
    u[1] = -p[0]

    u = np.array(u)
    u = normalize(u)
    
    up = np.matmul(A, u)

    fi = math.acos(np.dot(u, up))

    mes_proizvod = np.array([[u[0], u[1], u[2]], [up[0], up[1], up[2]], [p[0], p[1], p[2]]])
    
    if (np.linalg.det(mes_proizvod) < 0):
        p = -1 * p

    p = normalize(p)

    return p, fi

#funkcija koja racuna matricu izometrije Rodrigezovom formulom
def Rodrigez(p, fi):
    
    Rp = np.zeros((3, 3), dtype='float')
    
    for i in range(3):
        for j in range(3):
            Rp[i][j] = p[j] * p[i]
            
    Rp = Rp + math.cos(fi) * (np.eye(3, dtype='float') - Rp)
    
    #pravljenje px matrice
    px = np.zeros((3,3), dtype='float')
    
    px[0][1] = -p[2]
    px[0][2] = p[1]
    px[1][0] = p[2]
    px[1][2] = -p[0]
    px[2][0] = -p[1]
    px[2][1] = p[0]
    
    Rp = Rp + math.sin(fi) * px
            
    return Rp

#funkcija racunanja kvaterniona koji predstavlja rotaciju
def AxisAngle2Q(p, fi):
    
    w = math.cos(fi / 2)
    
    #normalizacija
    norm = np.linalg.norm(p)
    
    if norm != 0:
        p = p / norm
        
    q = np.zeros(4, dtype='float')
    
    for i in range(3):
        q[i] = math.sin(fi / 2) * p[i]
    
    q[3] = w
    
    return q

#funkcija kojom od kvaterniona dobijamo vektor i ugao rotacije
def Q2AxisAngle(q):
    
    p = np.zeros(3, dtype='float')
    
    norm = np.linalg.norm(q)
    
    if norm != 0:
        q = q / norm
        
    fi = 2 * np.arccos(q[3])
    
    if(abs(q[3]) == 1):
        
        p[0] = 1
        
    else:
        for i in range(3):
            p[i] = q[i]
            
        norm = np.linalg.norm(p)
    
        if norm != 0:
            p = p / norm
            
    return p, fi

#slerp funkcija, vraca jedinicni kvaternion q, slerp interpolacija izmedju q1 i q2 u trenutku t iz [0, tm]
def slerp(q1, q2, tm, t):

    cosO = np.dot(q1, q2)

    if(cosO < 0):
        #idi po kracem luku
        q1 = -q1
    if(cosO > 0.95):
        #kvat previse blizu
        return q1

    fi_0 = math.acos(cosO)

    qs = math.sin(fi_0 * (1 - t / tm)) / math.sin(fi_0) * q1 + math.sin(fi_0 * t / tm) / math.sin(fi_0) * q2

    return qs

########################################################




#niz boja
colors = ['red', 'green', 'blue']
    
#inicijalizacija plota    
fig = plt.figure()
ax = fig.gca(projection = '3d')

#funkcija transformacije po kadru animacije
def animation_frame(i):
    lines = []

    x = np.array([0, 1]) + i / 50
    y = np.array([0, 0]) + i / 50
    z = np.array([0, 0]) + i / 50

    lines.append([x, y, z])
    print([x, y, z])

    x = np.array([0, 0]) + i / 50
    y = np.array([0, 1]) + i / 50
    z = np.array([0, 0]) + i / 50

    lines.append([x, y, z])

    x = np.array([0, 0]) + i / 50
    y = np.array([0, 0]) + i / 50
    z = np.array([0, 1]) + i / 50

    lines.append([x, y, z])

    plt.cla()

    ax.set_xlim3d([0.0, 3.0])
    ax.set_ylim3d([0.0, 3.0])
    ax.set_zlim3d([0.0, 3.0])

    ax.set_title('SLerp interpolacija')

    for i in range(3):
        ax.plot(lines[i][0], lines[i][1], lines[i][2], c = colors[i])

#poziv animacije
line_animation = animation.FuncAnimation(fig, animation_frame, 25, interval = 200, blit=False)

plt.show()