#tacke se biraju u redu
#gore-levo, gore-desno, dole-levo, dole-desno
#napisan je program tako da gore-leva tacka ostaje fiksirana a ostale se slikaju pravougaonik cije se dimenzije proporcijalne udaljenostima odg stranica na originalnoj slici

import cv2
import numpy as np
import statistics
import math

#funkcija prebacuje afine koordinate u homogene, za korscenje u dlt-u
def homogenize(niz_afinih_tacaka):
    homogeni_niz = []

    for tacka in niz_afinih_tacaka:
        [x, y] = tacka
        homogeni_niz.append([x, y, 1])
    
    return homogeni_niz

def matrica_2x9(m, mp):
    M = np.zeros((2,9))
    
    M[1][0] = mp[2] * m[0]
    M[1][1] = mp[2] * m[1]
    M[1][2] = mp[2] * m[2]
    
    M[0][3] = -mp[2] * m[0]
    M[0][4] = -mp[2] * m[1]
    M[0][5] = -mp[2] * m[2]
    
    M[0][6] = mp[1] * m[0]
    M[0][7] = mp[1] * m[1]
    M[0][8] = mp[1] * m[2]
    
    M[1][6] = -mp[0] * m[0]
    M[1][7] = -mp[0] * m[1]
    M[1][8] = -mp[0] * m[2]
    
    return M

#dlt algoritam, isti onaj koji je koriscen za prva tri dela domaceg
def dlt(original, slika):
    n = min(len(original), len(slika))
    niz_mi = []
    
    for i in range(n):
        Mi = matrica_2x9(original[i], slika[i])
        niz_mi.append(Mi)
          
    M = np.stack(niz_mi)
    M = M.reshape(2*n, 9)
    
    _, _, ut = np.linalg.svd(M)
    P = ut[-1]
    P = P.reshape(3, 3)
    
    return P

#inicijalizacija biranih tacaka
izabrane_tacke = np.zeros((4,2), np.int)
#pomeranje, kako se ne bi videle na slici pri iscrtavanju pre nego da budu izabrane
izabrane_tacke = izabrane_tacke - 20

brojac_tacaka = 0

#funkcija osluskuje event pritiska levog tastera misa
def biranje_tacaka(event, x, y, flags, params):
    
    global izabrane_tacke
    global brojac_tacaka
    
    if event == cv2.EVENT_LBUTTONDOWN:
        
        if(brojac_tacaka <= 4):
            #azuririranje izabranih tacaka
            izabrane_tacke[brojac_tacaka] = x, y
            brojac_tacaka = brojac_tacaka + 1
            print(izabrane_tacke)

#ucitavanje slike
img = cv2.imread('02_dist1.bmp')
#kopija zbog prikaza izabranih tacaka
img_copy = cv2.imread('02_dist1.bmp')

visina, sirina, _ = img.shape

# u petlji se vrsi iscrtavanje originalne slike, oslusavanje akcije misem, i oznacavanje izabranih piksela
prekid = False

while True:

    cv2.imshow("Izaberite tacke koje zelite da slikate u pravougaonik", img_copy)

    if brojac_tacaka < 4:
        cv2.setMouseCallback("Izaberite tacke koje zelite da slikate u pravougaonik", biranje_tacaka)
    else:
        prekid = True

    for i in range(4):
        cv2.circle(img_copy, (izabrane_tacke[i][0], izabrane_tacke[i][1]), 4, (0, 0, 255), 2)

    cv2.waitKey(1)

    cv2.imshow("Izaberite tacke koje zelite da slikate u pravougaonik", img_copy)
    if prekid:
        break


tacke1 = np.float32([izabrane_tacke[0], izabrane_tacke[1], izabrane_tacke[2], izabrane_tacke[3]])

#ovako sam programirao odabir slika, bilo je pogodno za onu sliku koju sam koristio
sirina_projekcije = min(abs(izabrane_tacke[0][0] - izabrane_tacke[1][0]), abs(izabrane_tacke[2][0] - izabrane_tacke[3][0]))
visina_projekcije = min(abs(izabrane_tacke[0][1] - izabrane_tacke[2][1]), abs(izabrane_tacke[0][1] - izabrane_tacke[3][1]))

tp1 = [izabrane_tacke[0][0], izabrane_tacke[0][1]]
tp2 = [izabrane_tacke[0][0] + sirina_projekcije, izabrane_tacke[0][1]]
tp3 = [izabrane_tacke[0][0], izabrane_tacke[0][1] + visina_projekcije]
tp4 = [izabrane_tacke[0][0] + sirina_projekcije, izabrane_tacke[0][1] + visina_projekcije]

tacke2 = np.float32([tp1, tp2, tp3, tp4])

#koristi dlt algoritam za pravljenje matrice projekcije
matrica_proj = dlt(homogenize(tacke1), homogenize(tacke2))
#funkcija koja vrsi preslikavanje na slici
trans_slika = cv2.warpPerspective(img, matrica_proj, (sirina, visina))

#prikaz rezultata
cv2.imshow("Transformisana slika", trans_slika)

cv2.waitKey(0)