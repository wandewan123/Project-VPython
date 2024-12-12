from vpython import *
#Web VPython 3.2

scene.width = 1500
scene.height = 500
scene.background = color.white

scene.title = """                                                                                            <b>GERAK OSILASI SEDERHANA</b>
                                                                           <font color="blue">by. Dewan Java Turis Repmi Tamsih (225090307111005)</font>
Program ini dibuat pada tahun 2024 untuk memenuhi tugas matakuliah Pemodelan dan Visualisasi  - Fisika - Universitas Brawijaya
 """

# Membuat sumbu pergerakan
pointer1 = arrow(pos = vector(0, 4, 3), axis = vector(0, 3, 0), color = color.blue)
pointer2 = arrow(pos = vector(0, 4, 3), axis = vector(3, 0, 0), color = color.blue)
Label_pointer = text(text = "y", pos = vector(0, 9, 0), color = color.blue)
Label_pointer = text(text = "x", pos = vector(4, 4, 0), color = color.blue)

# Membuat Objek dinding, pegas dan kotak
dinding = box(pos = vector(-20, 0, 0), size = vector(0.5, 6, 0), color = color.gray(0.6))
pegas = helix(pos = dinding.pos + vector(0.5, 0, 0), axis = vector(30, 0, 0), radius = 0.5, thickness = 0.1, coils = 24, color = color.red)
benda = box(pos = pegas.pos + pegas.axis - vector(0.5, 0, 0), size = vector(2, 2, 0), color = color.green)

scene.caption = '''Pada kasus ini, benda dianggap tidak memiliki sudut fase dan berada pada posisi sudah tersimpangkan saat t = 0.
Plot grafik yang dilakukan adalah kecepatan, posisi dan percepatan benda pada tiap waktu.
'''

# Membuat parameter konstanta pegas dan massa benda
scene.append_to_caption('Koefisien Pegas: ')
def setamp1(samp1):
    wtamp1.text = '{:1.2f}'.format(samp1.value)
slamp1 = slider(min = 5, max = 10, value = 10, step = 0.1, length = 300, bind = setamp1)
wtamp1 = wtext(text='{:1.2f}'.format(slamp1.value))
scene.append_to_caption(' N/m    ')

scene.append_to_caption('Massa Benda: ')
def setamp2(samp2):
    wtamp2.text = '{:1.2f}'.format(samp2.value)
slamp2 = slider(min = 5, max = 10, value = 5, step = 0.1, length = 300, bind = setamp2)
wtamp2 = wtext(text='{:1.2f}'.format(slamp2.value))
scene.append_to_caption(' kg\n\n')

# Inisial value
omega = sqrt(slamp1.value / slamp2.value)  # Frekuensi sudut (omega)
x     = 10   #Awal nilai x
v     = 0  # Kecepatan inisial
t     = 0  # Waktu inisial
dt    = 0.1  # Interval waktu

# Pembuatan Tombol Run dan Reset
pause_button = button(text=' '*10 + 'Run' + ' '*10, bind=pause) 
scene.append_to_caption('    ')
reset_button = button(text=' '*10 + 'Reset' + ' '*10, bind=reset)
scene.append_to_caption('<font color="black">   Tekan tombol Reset ketika roda mencapai ujung kanan\n </font>')

# Membuat definisi run dan reset simulasi
run = False
def pause(b):
    global run
    run = not run
    if run:
        b.text = ' '*10 + 'Pause' + ' '*16
    else:
        b.text = ' '*10 + 'Run' + ' '*10

def reset(c):
    global run, t, theta, benda, pegas
    run = False
    pause_button.text = ' '*10 + 'Run' + ' '*10
    f1.delete()
    f2.delete()
    data1.clear()
    data2.clear()
    g1.xmin = 0
    g1.xmax = 11
    g2.xmin = 0
    g2.xmax = 11
    
    # Update posisi benda dan pegas berdasarkan parameter
    pegas.axis = vector(30, 0, 0)  # Reset pegas ke panjang semula
    benda.pos = pegas.pos + pegas.axis - vector(0.5, 0, 0)  # Posisi benda mengikuti pegas
    
    # Inisial value
    omega = sqrt(slamp1.value / slamp2.value)  # Frekuensi sudut (omega)
    x     = 10   #Awal nilai x
    v     = 0  # Kecepatan inisial
    t     = 0  # Waktu inisial
    dt    = 0.01  # Interval waktu
    


# Membuat Definisi Grafik
data1 = []
data2 = []

g1 = graph(scroll=True, title="Posisi Benda dalam tiap waktu",
           xtitle="t (s)", ytitle="x [m]", width=1200, height=150,
           xmin=0, xmax=11)
f1 = gcurve(color=color.red)

g2 = graph(scroll=True, title="Kecepatan benda tiap saat",
           xtitle="time (s)", ytitle="velocity (m/s)", width=1200, height=150,
           xmin=0, xmax=11)
f2 = gcurve(color=color.red)

# Animasi Gerak Osilasi Harmonik dengan Batas waktu 10 sekon

while True:
    rate(120)
    if not run: continue

    omega = sqrt(slamp1.value / slamp2.value)
    a = -omega * omega * x
    v = v + a*dt
    x = x + v*dt
    
    # Membuat Animasi Benda Bergerak
    benda.pos.x = x
    pegas.axis = vector(x - dinding.pos.x, 0, 0)  # Update pegas sesuai dengan posisi benda

    # Menampilkan data grafik posisi
    data1 = data1 + [[t, x]]  # Menambahkan data posisi
    f1.data = data1
    # Menampilkan data grafik kecepatan
    data2 = data2 + [[t, v]]  # Menambahkan data kecepatan
    f2.data = data2
    # Menambahkan waktu
    t += dt

