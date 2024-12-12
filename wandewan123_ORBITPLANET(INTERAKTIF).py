from vpython import *
#Web VPython 3.2

scene.width = 1500
scene.height = 500
scene.background = color.black

scene.title = """                                                                                            <b>ORBIT PLANET TATA SURYA</b>
                                                                           <font color="blue">by. Dewan Java Turis Repmi Tamsih (225090307111005)</font>
Program ini dibuat pada tahun 2024 untuk memenuhi tugas matakuliah Pemodelan dan Visualisasi  - Fisika - Universitas Brawijaya
"""

# Grafik untuk kecepatan orbit
speed_graph = graph(title="Kecepatan Orbit vs Waktu", width=900, height=400, background=color.white,
                    xtitle="Waktu (s)", ytitle="Kecepatan (m/s)")
speed_curve = gcurve(graph=speed_graph, color=color.blue, label="Kecepatan Orbit")

scene.caption = '''Pada kasus ini, benda hanya diatur pada nilai esentrisitas dan massa planet yang diatur tetap.
'''

# Membuat parameter konstanta pegas dan massa benda
scene.append_to_caption('esentris: ')

current_eccentricity = 0.8  # Initial eccentricity
target_eccentricity = 0.8  # Eccentricity to interpolate towards

def setamp1(samp1):
    global target_eccentricity
    target_eccentricity = samp1.value
    wtamp1.text = '{:1.2f}'.format(samp1.value)

slamp1 = slider(min=0, max=0.9, value=current_eccentricity, step=0.1, length=300, bind=setamp1)
wtamp1 = wtext(text='{:1.2f}'.format(slamp1.value))

# Waktu simulasi
dt = 3600 * 12  # Interval waktu dalam detik (1 hari)
t = 0  # Waktu awal
running = True  # Status simulasi (pause/run)

# Konstanta fisika dan parameter orbit
G = 6.674e-11  # Gravitasi universal, m^3/kg/s^2
M = 1.989e30   # Massa Matahari, kg
m = 5.972e24   # Massa Bumi, kg
a = 1.496e11   # Semimajor axis (1 AU), m
c = a * current_eccentricity  # Offset fokus elips

# Objek Matahari (di fokus elips)
sun = sphere(pos=vector(-c, 0, 0), radius=1e10, color=color.yellow, emissive=True)

# Objek Bumi
earth = sphere(pos=vector(a - c, 0, 0), radius=5e9, color=color.blue, make_trail=True, trail_color=color.cyan)
earth.label = label(pos=earth.pos, text="Bumi", xoffset=20, height=10, color=color.white)

# Panah gaya gravitasi (visualisasi)
force_arrow = arrow(pos=earth.pos, axis=vector(0, 0, 0), color=color.red, shaftwidth=2e9)

# Fungsi untuk menghitung jarak dan kecepatan berdasarkan sudut θ
def calculate_position(theta, a, e, c):
    r = a * (1 - e**2) / (1 + e * cos(theta))
    x = r * cos(theta) - c  # Posisi x relatif terhadap fokus
    y = r * sin(theta)
    return vector(x, y, 0), r

def calculate_velocity(r, a):
    return sqrt(G * M * (2 / r - 1 / a))

# Fungsi untuk tombol kontrol
def pause_sim():
    global running
    running = False

def run_sim():
    global running
    running = True

def reset_sim():
    global t, theta, running, current_eccentricity, target_eccentricity, c
    running = False
    t = 0
    theta = 0
    current_eccentricity = slamp1.value
    target_eccentricity = slamp1.value
    c = a * current_eccentricity
    earth.pos, _ = calculate_position(theta, a, current_eccentricity, c)  # Reset posisi Bumi
    earth.clear_trail()  # Hapus jejak
    speed_curve.delete()  # Hapus data grafik
    force_arrow.pos = earth.pos

# Tambahkan tombol kontrol
button(text="Pause", bind=pause_sim)
button(text="Run", bind=run_sim)
button(text="Reset", bind=reset_sim)

# Simulasi
theta = 0  # Sudut awal (radian)
interpolation_speed = 0.01  # Speed of eccentricity transition

while True:
    rate(100)  # Kecepatan simulasi
    if running:
        # Gradual update of eccentricity
        if abs(current_eccentricity - target_eccentricity) > 1e-3:
            current_eccentricity += (target_eccentricity - current_eccentricity) * interpolation_speed
            c = a * current_eccentricity  # Update focus offset
            sun.pos = vector(-c, 0, 0)  # Update Sun's position at the focus
        
        # Update sudut dan waktu
        r_vector, r = calculate_position(theta, a, current_eccentricity, c)
        v = calculate_velocity(r, a)  # Kecepatan orbit
        theta += v / r * dt  # Update sudut berdasarkan kecepatan sudut
        t += dt  # Waktu berjalan
        
        # Update posisi dan visualisasi
        earth.pos = r_vector  # Update posisi Bumi
        earth.label.pos = earth.pos  # Update posisi label
        force_arrow.pos = earth.pos  # Update posisi panah gaya
        force_arrow.axis = -(earth.pos - sun.pos).norm() * 5e10  # Update arah dan panjang panah gravitasi
        
        # Tambahkan data ke grafik
        speed_curve.plot(t, v)
