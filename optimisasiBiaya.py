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

# enumerasi titik pojok
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
idx_opt = int(np.argmin(nilai_Z))
x_opt, y_opt = titik_layak[idx_opt]
z_opt = nilai_Z[idx_opt]

# output
print("OPTIMASI BIAYA SEWA CLOUD SERVER")
print("=" * 50)
print("Model:")
print("Minimasi Z = 8000x + 12000y")
print("20x + 10y >= 100   (pemrosesan data)")
print("10x + 30y >= 90    (akses basis data)")
print("x, y >= 0")
print("-" * 50)
print("Titik pojok daerah layak dan nilai Z:")
for p, z in zip(titik_layak, nilai_Z):
    print(f"(x={p[0]:.1f}, y={p[1]:.1f})  ->  Z = Rp {z:,.0f}")
print("-" * 50)
print("HASIL AKHIR:")
print(f"Server Standar          : {x_opt:.1f} jam")
print(f"Server Performa Tinggi  : {y_opt:.1f} jam")
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

# garis melalui titik optimum
y_iso = (z_opt - biaya[0] * x) / biaya[1]
ax.plot(x, y_iso, "--", color="tab:red",
        label=f"Garis biaya optimum (Z = Rp {z_opt:,.0f})")

# titik pojok
for p, z in zip(titik_layak, nilai_Z):
    ax.plot(p[0], p[1], "ko")
    ax.annotate(f"({p[0]:.1f}; {p[1]:.1f})\nZ={z:,.0f}", (p[0], p[1]),
                textcoords="offset points", xytext=(10, 8), fontsize=9)

# titik optimum
ax.plot(x_opt, y_opt, "r*", markersize=18, label="Titik optimum")

ax.set_xlim(0, 12)
ax.set_ylim(0, y_atas)
ax.set_xlabel("x : jam Server Standar")
ax.set_ylabel("y : jam Server Performa Tinggi")
ax.set_title("Grafik Titik Optimal Biaya Sewa Cloud Server")
ax.grid(True, linestyle=":", alpha=0.6)
ax.legend(loc="upper right")
plt.tight_layout()
plt.savefig("grafik_optimal.png", dpi=150)
plt.show()