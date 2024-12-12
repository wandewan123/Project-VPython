from vpython import *
#Web VPython 3.2

scene.width = 1500
scene.height = 500
scene.background = color.white

scene.title = """                                                                                            <b>GERAK OSILASI SEDERHANA</b>
                                                                           <font color="blue">by. Dewan Java Turis Repmi Tamsih (225090307111005)</font>
Program ini dibuat pada tahun 2024 untuk memenuhi tugas matakuliah Pemodelan dan Visualisasi  - Fisika - Universitas Brawijaya
 """

# Panjang tali (L) dan sudut awal (theta) dalam derajat
L       = 30 # m
theta   = radians(10)  # Konversi sudut ke radian
gravity = 9.8 # m/s^2
mass    = 10

# Objek dinding, tali dan Bola
dinding = box(pos=vector(0, 20, 0), size=vector(20, 2, 0), color=color.black)
tali    = cylinder(pos=dinding.pos - vector(0, 0.5, 0), axis=vector(L * sin(theta), -L * cos(theta), 0), radius=0.1, color=color.red)
bola    = sphere(pos=tali.pos + tali.axis, radius=1, color=color.blue)

scene.caption = '''Pada kasus ini, benda dianggap tidak memiliki sudut fase dan berada pada posisi sudah tersimpangkan saat t = 0.
Plot grafik yang dilakukan adalah energi kinetik, potensial dan mekanik terhadap waktu.
'''

# Inisial value
thetaf = sqrt(gravity / L) #Frekuensi sudut (omega)
theta  = theta   #Awal nilai x
omega  = 0  # Kecepatan inisial
t      = 0  # Waktu inisial
dt     = 0.1  # Interval waktu

# Pembuatan Tombol Run dan Reset
pause_button = button(text=' '*10 + 'Run' + ' '*10, bind=pause) 
scene.append_to_caption('    ')
reset_button = button(text=' '*10 + 'Reset' + ' '*10, bind=reset)

# Membuat definisi run dan reset simulasi
run = False
def pause(b):
    global run
    run = not run
    if run:
        b.text = ' '*10 + 'Pause' + ' '*16
    else:
        b.text = ' '*10 + 'Run' + ' '*10

def reset(b):
    global t, theta, omega, run, data1, data2, data3
    run = False
    pause_button.text = ' '*10 + 'Run' + ' '*10
    t = 0
    theta = radians(10)
    omega = 0
    tali.axis = vector(L * sin(theta), -L * cos(theta), 0)
    bola.pos = tali.pos + tali.axis
    f1.delete()
    f2.delete()
    f3.delete()
    data1.clear()
    data2.clear()
    data3.clear()
    g1.xmin = 0
    g1.xmax = 10
    
    # Reset posisi benda
    tali.axis = vector(L * sin(theta), -L * cos(theta), 0)  # Reset pegas ke panjang semula
    benda.pos = tali.pos + tali.axis  # Posisi benda mengikuti pegas
    
    # Inisial value
    thetaf = sqrt(gravity / L) #Frekuensi sudut (omega)
    theta  = theta   #Awal nilai x
    omega  = 0  # Kecepatan inisial
    t      = 0  # Waktu inisial
    dt     = 0.01  # Interval waktu

# Membuat Definisi Grafik
data1 = []
data2 = []
data3 = []

g1 = graph(scroll = True, title = "Energi Benda",
           xtitle = "t (sekon)", ytitle = "E [Joule]", width = 1200, height = 150,
           xmin   = 0, xmax = 11)
f1 = gcurve(color = color.red, label = "Kinetik")
f2 = gcurve(color = color.blue, label = "Potensial")
f3 = gcurve(color = color.black, label = "Mekanik")

# Animasi Gerak Osilasi Harmonik dengan Batas waktu 10 sekon

# Animasi
while True:
    rate(100)
    if not run:
        continue

    # Perhitungan gerak osilasi
    a = -thetaf ** 2 * theta  # Percepatan sudut
    omega += a * dt  # Kecepatan sudut
    theta += omega * dt  # Posisi sudut

    # Perbarui posisi bola dan tali
    tali.axis = vector(L * sin(theta), -L * cos(theta), 0)
    bola.pos = tali.pos + tali.axis

    # Hitung energi
    kecepatan = L * omega  # kecepatan linear
    kinetik = 0.5 * mass * kecepatan ** 2
    potensial = mass * gravity * L * (1 - cos(theta))
    mekanik = kinetik + potensial

    # Tambahkan data ke grafik
    f1.plot(t, kinetik)
    f2.plot(t, potensial)
    f3.plot(t, mekanik)

    t += dt