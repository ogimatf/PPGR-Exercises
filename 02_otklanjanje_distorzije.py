import cv2
import numpy as np

izabrane_tacke = np.zeros((4,2), np.int)
brojac_tacaka = 0


def biranje_tacaka(event, x, y, flags, params):
    
    global izabrane_tacke
    global brojac_tacaka
    
    if event == cv2.EVENT_LBUTTONDOWN:
        
        izabrane_tacke[brojac_tacaka] = x, y
        brojac_tacaka = brojac_tacaka + 1
        print(izabrane_tacke)

img = cv2.imread('02_dist1.jpg')
img_copy = cv2.imread('02_dist1.jpg')

visina, sirina, _ = img.shape

while True:
    
    if brojac_tacaka == 4:
        tacke1 = np.float32([izabrane_tacke[0], izabrane_tacke[1], izabrane_tacke[2], izabrane_tacke[3]])

        sirina_projekcije = max(abs(izabrane_tacke[0][0] - izabrane_tacke[1][0]), abs(izabrane_tacke[2][0] - izabrane_tacke[3][0]))
        visina_projekcije = max(abs(izabrane_tacke[0][1] - izabrane_tacke[2][1]), abs(izabrane_tacke[0][1] - izabrane_tacke[3][1]))

        tp1 = [izabrane_tacke[0][0], izabrane_tacke[0][1]]
        tp2 = [izabrane_tacke[0][0] + sirina_projekcije, izabrane_tacke[0][1]]
        tp3 = [izabrane_tacke[0][0], izabrane_tacke[0][1] + visina_projekcije]
        tp4 = [izabrane_tacke[0][0] + sirina_projekcije, izabrane_tacke[0][1] + visina_projekcije]

        tacke2 = np.float32([tp1, tp2, tp3, tp4])

        matrica_proj = cv2.getPerspectiveTransform(tacke1, tacke2)
        trans_slika = cv2.warpPerspective(img, matrica_proj, (sirina, visina))
        
        cv2.imshow("Transformisana slika", trans_slika)


    for i in range(4):
        cv2.circle(img_copy, (izabrane_tacke[i][0], izabrane_tacke[i][1]), 4, (0, 0, 255), 2)

    cv2.imshow("Izaberite tacke koje zelite da slikate u pravougaonik", img_copy)
    cv2.setMouseCallback("Izaberite tacke koje zelite da slikate u pravougaonik", biranje_tacaka)

    cv2.waitKey(1)