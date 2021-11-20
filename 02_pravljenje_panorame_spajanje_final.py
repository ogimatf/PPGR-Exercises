#algoritam zahteva levu i desnu sliku da se ucitaju tim redosledom
#korisnik unosi "istih tacki" koje zeli da izabere
#korisnik bira misem "iste tacke" naizmenicno na levoj slici pa na desnoj slici

import cv2
import numpy as np
import statistics
import math

#funkcija koja uklanja crnu okolinu oko slika
def crop(image, threshold=0):

    if len(image.shape) == 3:
        flatImage = np.max(image, 2)
    else:
        flatImage = image
    assert len(flatImage.shape) == 2

    rows = np.where(np.max(flatImage, 0) > threshold)[0]
    if rows.size:
        cols = np.where(np.max(flatImage, 1) > threshold)[0]
        image = image[cols[0]: cols[-1] + 1, rows[0]: rows[-1] + 1]
    else:
        image = image[:1, :1]

    return image

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

#radi pracenja unosa tacaka
broj_istih_tacaka = 0

brojac = 0

izabrane_tacke_l = []
brojac_tacaka_l = 0

izabrane_tacke_d = []
brojac_tacaka_d = 0

#funkcija kojom se biraju tacke misem
def biranje_tacaka(event, x, y, flags, params):
    
    global izabrane_tacke_l
    global izabrane_tacke_d

    global brojac_tacaka_l
    global brojac_tacaka_d

    global brojac

    global brojac_istih_tacaka
    
    #osluskivanje dogadjaja klika na levi taster misa
    if event == cv2.EVENT_LBUTTONDOWN:
        
        #izabrane tacke se ubacuju u odgovarajuce nizove naizmenicno
        if(brojac <= broj_istih_tacaka * 2):
            
            if (brojac % 2 == 0):

                izabrane_tacke_l[brojac_tacaka_l] = x, y
                brojac_tacaka_l = brojac_tacaka_l + 1
                #print(izabrane_tacke_l)

            else:
                
                izabrane_tacke_d[brojac_tacaka_d] = x, y
                brojac_tacaka_d = brojac_tacaka_d + 1
                #print(izabrane_tacke_d)

            brojac = brojac + 1
            #print(brojac)


#POCETAK GLAVNOG DELA PROGRAMA
print("Koliko zajednickih tacaka zelite da izaberete?\n")
broj_istih_tacaka = int(input())

#inicijalizacija nizova 
izabrane_tacke_l = np.zeros((broj_istih_tacaka,2), np.int)
izabrane_tacke_l = izabrane_tacke_l - 20

izabrane_tacke_d = np.zeros((broj_istih_tacaka,2), np.int)
izabrane_tacke_d = izabrane_tacke_d - 20

prekid = False

#ucitavanje slika, bitan redosled
img_l = cv2.imread('nikola_levo.jpg')
img_d = cv2.imread('nikola_desno.jpg')
img_l_cp = cv2.imread('nikola_levo.jpg')
img_d_cp = cv2.imread('nikola_desno.jpg')

h1, w1 = img_l_cp.shape[:2]
h2, w2 = img_d_cp.shape[:2]

#spajanje slika u jednu radi lakseg prikaza i odabira tacaka
spojene_slike = np.zeros((max(h1, h2), w1 + w2, 3), np.uint8)

spojene_slike[:h1, :w1, :3] = img_l_cp
spojene_slike[:h2, w1 : w1 + w2, :3] = img_d_cp

prekid = False

#petlja u kojoj se osluskuje dogadjaj klika na mis, beleze odabrane tacke, i zaokruzuju na slici
while True:

    cv2.imshow('Spojena slika', spojene_slike)

    if brojac < broj_istih_tacaka * 2:
        cv2.setMouseCallback('Spojena slika', biranje_tacaka)
    else:
        prekid = True

    for i in range(broj_istih_tacaka):
        cv2.circle(spojene_slike, (izabrane_tacke_l[i][0], izabrane_tacke_l[i][1]), 4, (0, 0, 255), 2)

    for i in range(broj_istih_tacaka):
        cv2.circle(spojene_slike, (izabrane_tacke_d[i][0], izabrane_tacke_d[i][1]), 4, (0, 0, 255), 2)

    cv2.waitKey(1)

    cv2.imshow('Spojena slika', spojene_slike)
    if prekid:
        break


tacke_l = np.float32(izabrane_tacke_l)

#ovde se pomera x koordinatu izabranih tacaka sa desne slike za sirinu leve slike, zbog toga stu su one birane kada su slike bile spojene
tacke_d = []

for tacka in izabrane_tacke_d:
    tacka_tmp = [tacka[0] - w1, tacka[1]]
    tacke_d.append(tacka_tmp)

tacke_d = np.float32(tacke_d)


#slikamo tacke desne slike u tacke leve slike
matrica_proj = dlt(homogenize(tacke_d), homogenize(tacke_l))

#racuna se duplo sira slika nego sto je potrebno, kako bi stala cela transformisana desna slika
trans_slika_d = cv2.warpPerspective(img_d, matrica_proj, (w2 * 2, h2))

#preslikavam levu sliku na levu stranu transformisane desne slike
trans_slika_d[:h1, :w1, :3] = img_l

#obrada crnih ivica sa desne strane
panorama = crop(trans_slika_d, 0)

#konacan prikaz
cv2.imshow('Panorama', panorama)

cv2.waitKey(0)