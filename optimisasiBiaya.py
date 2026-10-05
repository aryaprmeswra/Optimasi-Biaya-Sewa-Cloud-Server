import itertools
import numpy as np
import matplotlib.pyplot as plt

# data masalah
biaya = np.array([8000, 12000])          # Rp/jam: Standar, Performa Tinggi

A = np.array([[20, 10],    # pemrosesan data
              [10, 30],    # akses basis data
              [1, 0],      # x >= 0
              [0, 1]])     # y >= 0
b = np.array([100, 90, 0, 0])

# langkah 1: relaksasi linear (enumerasi titik pojok)
titik_layak = []
for i, j in itertools.combinations(range(len(b)), 2):
    M = A[[i, j]]
    if abs(np.linalg.det(M)) < 1e-12:    # garis sejajar
        continue
    p = np.linalg.solve(M, b[[i, j]])
    if np.all(A @ p >= b - 1e-9):        # cek kelayakan
        titik_layak.append(p)

# hapus duplikat
unik = []
for p in titik_layak:
    if not any(np.allclose(p, q) for q in unik):
        unik.append(p)
titik_layak = sorted(unik, key=lambda p: p[0])

nilai_Z = [float(biaya @ p) for p in titik_layak]
idx_lp = int(np.argmin(nilai_Z))
x_lp, y_lp = titik_layak[idx_lp]
z_lp = nilai_Z[idx_lp]

# langkah 2: pencarian solusi bilangan bulat
# batas 0..12 sudah cukup: (9,0) layak dengan Z = 72.000, sehingga x > 9
# atau y > 6 pasti lebih mahal dari itu
bulat_layak = []
for xi in range(0, 13):
    for yi in range(0, 13):
        if np.all(A @ np.array([xi, yi]) >= b):
            bulat_layak.append((xi, yi, int(biaya @ np.array([xi, yi]))))

bulat_layak.sort(key=lambda t: (t[2], t[0]))
x_opt, y_opt, z_opt = bulat_layak[0]

# output
print("OPTIMASI BIAYA SEWA CLOUD SERVER (JAM BULAT)")
print("=" * 50)
print("Model:")
print("Minimasi Z = 8000x + 12000y")
print("20x + 10y >= 100   (pemrosesan data)")
print("10x + 30y >= 90    (akses basis data)")
print("x, y >= 0 dan bilangan bulat")
print("-" * 50)
print("Langkah 1 - Relaksasi linear (jam boleh pecahan):")
for p, z in zip(titik_layak, nilai_Z):
    print(f"(x={p[0]:.1f}, y={p[1]:.1f})  ->  Z = Rp {z:,.0f}")
print(f"Optimum relaksasi: x={x_lp:.1f}, y={y_lp:.1f}, Z = Rp {z_lp:,.0f} (tidak bulat)")
print("-" * 50)
print("Langkah 2 - 5 kombinasi jam bulat layak termurah:")
for xi, yi, zi in bulat_layak[:5]:
    print(f"(x={xi}, y={yi})  ->  Z = Rp {zi:,.0f}")
print("-" * 50)
print("HASIL AKHIR:")
print(f"Server Standar          : {x_opt} jam")
print(f"Server Performa Tinggi  : {y_opt} jam")
print(f"Biaya sewa minimum      : Rp {z_opt:,.0f}")

# grafik
x = np.linspace(0, 12, 400)
y_k1 = 10 - 2 * x            # 2x + y = 10
y_k2 = (9 - x) / 3           # x + 3y = 9
batas_bawah = np.maximum.reduce([y_k1, y_k2, np.zeros_like(x)])
y_atas = 12

fig, ax = plt.subplots(figsize=(9, 7))
ax.plot(x, y_k1, label="K1: 20x + 10y = 100", color="tab:blue")
ax.plot(x, y_k2, label="K2: 10x + 30y = 90", color="tab:green")
ax.fill_between(x, batas_bawah, y_atas, alpha=0.25, color="gold",
                label="Daerah layak")

# titik bulat layak
bx = [t[0] for t in bulat_layak]
by = [t[1] for t in bulat_layak]
ax.scatter(bx, by, s=14, color="gray", zorder=3, label="Titik bulat layak")

# garis biaya melalui titik optimum bulat
y_iso = (z_opt - biaya[0] * x) / biaya[1]
ax.plot(x, y_iso, "--", color="tab:red",
        label=f"Garis biaya optimum (Z = Rp {z_opt:,.0f})")

# titik optimum relaksasi
ax.plot(x_lp, y_lp, "D", color="tab:purple", markersize=9, zorder=4,
        label=f"Optimum relaksasi ({x_lp:.1f}; {y_lp:.1f}), Z = Rp {z_lp:,.0f}")

# titik optimum bulat
ax.plot(x_opt, y_opt, "r*", markersize=18, zorder=5,
        label=f"Optimum bulat ({x_opt}; {y_opt}), Z = Rp {z_opt:,.0f}")
ax.annotate(f"({x_opt}; {y_opt})\nZ={z_opt:,.0f}", (x_opt, y_opt),
            textcoords="offset points", xytext=(12, 10), fontsize=9)

ax.set_xlim(0, 12)
ax.set_ylim(0, y_atas)
ax.set_xlabel("x : jam Server Standar")
ax.set_ylabel("y : jam Server Performa Tinggi")
ax.set_title("Grafik Titik Optimal Biaya Sewa Cloud Server (Jam Bulat)")
ax.grid(True, linestyle=":", alpha=0.6)
ax.legend(loc="upper right", fontsize=8)
plt.tight_layout()
plt.savefig("grafik_optimal.png", dpi=150)
plt.show()