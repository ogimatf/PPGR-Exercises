from vpython import *
import math as math


label2 = label(pos=vec(2, 200, 0), text='Jednostepena raketa: ')
label4 = label(pos=vec(2, 100, 0), text='Dvostepena raketa prva faza: ')
label6 = label(pos=vec(2, 0, 0), text='Dvostepena raketa druga faza: ')
label7 = label(pos=vec(2, -100, 0), text='Dvostepena raketa treca faza: ')
label8 = label(pos=vec(2, -200, 0), text='Dvostepena raketa: ')

exhaust_velocity = vector(0, -76.36, 0)
mdot = 32  # Rate of mass loss per time.
dt = 0.001
t = 0
g = -9.8
gravity = vector(0, g * dt, 0)
rate(300)
scene.visible = True
scene.width = scene.width + 10

def jednoStepena(v0, pozicija, cista_masa, masa_goriva, toPlot, freeFall, toPrint , title):
    graph(fast=True, legend= True, xtitle = "vreme(s)", title = title)
    r_pos = gcurve(color=color.red, label="visina (m)")
    r_speed = gcurve(color=color.blue, label="brzina (m/s)")
    rocket = cylinder(pos=pozicija, color=color.red, size=vector(0.5, 0.1, 0.1),
                      velocity=v0, mass=cista_masa, fuel_mass=masa_goriva,
                      make_trail=True, axis=vector(0, 1, 0))
    scene.camera.follow(rocket)
    yNakonSagorevanja = 0
    yMax = 0
    vMax = 0
    global t
    while True:
        if rocket.fuel_mass > 0:
            dm = mdot * dt  # Amount of mass lost in time dt.
            rocket.velocity = rocket.velocity + dm / (rocket.mass + rocket.fuel_mass) * (-exhaust_velocity)
            rocket.pos = rocket.pos + rocket.velocity * dt
            rocket.fuel_mass = rocket.fuel_mass - dm

            if yNakonSagorevanja < rocket.pos.y:
                yNakonSagorevanja = rocket.pos.y
        else:
            if freeFall:
                rocket.velocity = rocket.velocity + gravity
                rocket.pos = rocket.pos + rocket.velocity * dt
            else:
                break
        if rocket.pos.y > yMax:
            yMax = rocket.pos.y
        if rocket.velocity.y > vMax:
            vMax = rocket.velocity.y



        t = t + dt
        if toPlot:
            r_pos.plot(pos=(t, rocket.pos.y))
            r_speed.plot(pos=(t, rocket.velocity.y))

        if rocket.pos.y <= 0:
            break
    if toPrint:
        print("Jednostepena:\nMax brzina: " + str(vMax) + " Visina nakon sagorevanja:" + str(
            yNakonSagorevanja) + " Max visina: " + str(yMax))
        label2.text = "Jednostepena:\nMax brzina: " + str(round(vMax,3)) + " Visina nakon sagorevanja:" + str(round(
            yNakonSagorevanja,3)) + " Max visina: " + str(round(yMax,3))
    return vMax, yNakonSagorevanja, yMax, rocket


def dvoStepena():
    # prva etapa
    global t
    v0, yNakonSagorevanja, _, _ = jednoStepena(vector(0, 0, 0), vector(0, 0, 0), 110, 50, True, False, False, "Grafik zavisnosti brzine i visine prve faze dvostepene rakete od vremena")
    print("Dvostepena Raketa Prva Faza:\nMax brzina prve faze: " + str(v0) + " Predjeni put za vreme isticanja goriva prvog motora: " + str(yNakonSagorevanja))
    label4.text = "Dvostepena Raketa Prva Faza:\nMax brzina prve faze: " + str(round(v0,3)) + " Predjeni put za vreme isticanja goriva prvog motora: " + str(round(yNakonSagorevanja,3))

    # druga etapa
    v_drugaFaza, yDrugeFaze, yMaxDrugeFaze, rocket = jednoStepena(vector(0, v0, 0), vector(0, yNakonSagorevanja, 0), 60, 50, True,
                                                          False, False, "Grafik zavisnosti brzine i visine druge faze dvostepene rakete od vremena")

    print("Dvostepena Raketa Druga Faza:\nMax brzina druge faze: " + str(v0 + v_drugaFaza) + " Predjeni put za vreme isticanja goriva drugog motora: " + str(yDrugeFaze))
    label6.text = "Dvostepena Raketa Druga Faza:\nMax brzina druge faze: " + str(round(v0 + v_drugaFaza,3)) + " Predjeni put za vreme isticanja goriva drugog motora: " + str(round(yDrugeFaze,3))

    #treca etapa
    rocket.mass = 60
    rocket.fuel_mass = 0
    rocket.velocity = vector(0, v0 + v_drugaFaza, 0)
    rocket.pos.y = yNakonSagorevanja + yDrugeFaze
    graph(fast=True, legend= True, xtitle = "vreme (s)", title = "Grafik zavisnosti brzine i visine trece faze dvostepene rakete od vremena")
    r_pos = gcurve(color=color.red, label="visina (m)")
    r_speed = gcurve(color=color.blue, label="brzina (m/s)")
    yMaxTrecaFaza = 0
    while rocket.pos.y > 0:
        rocket.velocity = rocket.velocity + gravity
        rocket.pos = rocket.pos + rocket.velocity * dt
        if yMaxTrecaFaza < rocket.pos.y:
            yMaxTrecaFaza = rocket.pos.y

        r_pos.plot(pos=(t, rocket.pos.y))
        r_speed.plot(pos=(t, rocket.velocity.y))
        t = t + dt
    print("Dvostepena Raketa Treca Faza:\n"+"Predjeni put u trecoj fazi: " + str(yMaxTrecaFaza - yDrugeFaze - yNakonSagorevanja ) + "\nMax Visina Dvostepene rakete: " + str(yMaxTrecaFaza))
    label7.text = "Dvostepena Raketa Treca Faza:\n"+"Predjeni put u trecoj fazi: " + str(round(yMaxTrecaFaza - yDrugeFaze - yNakonSagorevanja ,3))
    label8.text = "Max Visina Dvostepene rakete: " + str(round(yMaxTrecaFaza,3))
    return


jednoStepena(vector(0, 0, 0), vector(0, 0, 0), 60, 100, True, True, True, "Grafik zavisnosti brzine i visine jednostepene rakete od vremena" )
dvoStepena()
