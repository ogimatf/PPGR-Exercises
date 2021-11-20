
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

broj_istih_tacaka = 0

izabrane_tacke_l = []
brojac_tacaka_l = 0

def biranje_levih_tacaka(event, x, y, flags, params):

    global izabrane_tacke_l
    global brojac_tacaka_l

    if event == cv2.EVENT_LBUTTONDOWN:

        izabrane_tacke_l.append([x, y])
        brojac_tacaka_l = brojac_tacaka_l + 1
        print(izabrane_tacke_l)

izabrane_tacke_d = []
brojac_tacaka_d = 0

def biranje_desnih_tacaka(event, x, y, flags, params):

    global izabrane_tacke_d
    global brojac_tacaka_d

    if event == cv2.EVENT_LBUTTONDDOWN:

        izabrane_tacke_d.append([x, y])
        brojac_tacaka_d = brojac_tacaka_d + 1
        print(izabrane_tacke_d)



img_l = cv2.imread('02_slika_levo.jpg')
img_d = cv2.imread('02_slika_desno.jpg')

img_l_cp= cv2.imread('02_slika_levo.jpg')
img_d_cp = cv2.imread('02_slika_desno.jpg')

prekid = False

cv2.imshow("Izaberite tacke na levoj slici", img_l_cp)
cv2.imshow("Izaberite tacke na desnoj slici", img_d_cp)

print("Koliko zajednickih tacaka zelite da izaberete?\n")
broj_istih_tacaka = int(input())

prekid = False

while True:

    cv2.imshow("Izaberite tacke na levoj slici", img_l_cp)
    cv2.imshow("Izaberite tacke na desnoj slici", img_d_cp)

    if brojac_tacaka_l < broj_istih_tacaka and brojac_tacaka_d < broj_istih_tacaka:
        cv2.setMouseCallback("Izaberite tacke na levoj slici", biranje_levih_tacaka)
    else:
        prekid = True

    for i in range(brojac_tacaka_l):
        cv2.circle(img_l_cp, (izabrane_tacke_l[i][0], izabrane_tacke_l[i][1]), 4, (0, 0, 255), 2)


    cv2.waitKey(1)

    cv2.imshow("Izaberite tacke na levoj slici", img_l_cp)
    cv2.imshow("Izaberite tacke na levoj slici", img_l_cp)

    if prekid:
        break

while True:

    cv2.imshow("Izaberite tacke na levoj slici", img_l_cp)
    cv2.imshow("Izaberite tacke na desnoj slici", img_d_cp)

    if brojac_tacaka_l < broj_istih_tacaka and brojac_tacaka_d < broj_istih_tacaka:
        cv2.setMouseCallback("Izaberite tacke na desnoj slici", biranje_desnih_tacaka)
    else:
        prekid = True

    for i in range(brojac_tacaka_d):    
        cv2.circle(img_l_cp, (izabrane_tacke_d[i][0], izabrane_tacke_d[i][1]), 4, (0, 0, 255), 2)

    cv2.waitKey(1)

    cv2.imshow("Izaberite tacke na levoj slici", img_l_cp)
    cv2.imshow("Izaberite tacke na desnoj slici", img_d_cp)

    if prekid:
        break