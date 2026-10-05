
print("\n" + "="*70)
print("OPTIMASI SEWA CLOUD SERVER")
print("="*70)

# PARAMETER
instr_x, akses_x, biaya_x = 20, 10, 8000   # Server Standar
instr_y, akses_y, biaya_y = 10, 30, 12000  # Server Performa Tinggi
instr_min, akses_min = 100, 90

# TEMUKAN TITIK KRITIS
print("\n" + "="*70)
print("PENYELESAIAN: CORNER POINT METHOD")
print("="*70)

# Titik perpotongan dua garis kendala
# 20x + 10y = 100  -->  y = 10 - 2x
# 10x + 30y = 90   -->  y = (9-x)/3
# 10 - 2x = (9-x)/3  -->  30 - 6x = 9 - x  -->  x = 4.2
x1, y1 = 4.2, 1.6

# Titik-titik lainnya
titik_list = [
    ("Perpotongan garis 1 & 2", 4.2, 1.6),
    ("Garis 1 ∩ Sumbu Y", 0.0, 10.0),
    ("Garis 1 ∩ Sumbu X", 5.0, 0.0),
    ("Garis 2 ∩ Sumbu Y", 0.0, 3.0),
    ("Garis 2 ∩ Sumbu X", 9.0, 0.0),
]

print("\nEvaluasi Setiap Titik:")
print("-" * 70)
print(f"{'Titik':<25} {'x':>6} {'y':>6} {'K1':>8} {'K2':>8} {'Z (Rp)':>12} {'Feasible':<8}")
print("-" * 70)

feasible = []
for nama, x, y in titik_list:
    k1 = instr_x*x + instr_y*y
    k2 = akses_x*x + akses_y*y
    z = biaya_x*x + biaya_y*y
    valid = (k1 >= instr_min - 0.001) and (k2 >= akses_min - 0.001)
    
    status = "YA" if valid else "TIDAK"
    print(f"{nama:<25} {x:>6.1f} {y:>6.1f} {k1:>8.0f} {k2:>8.0f} {z:>12.0f} {status:<8}")
    
    if valid:
        feasible.append((nama, x, y, z))

# ==================== SOLUSI OPTIMAL ====================
print("-" * 70)

if feasible:
    optimal = min(feasible, key=lambda p: p[3])
    nama_opt, x_opt, y_opt, z_opt = optimal
    
    print("\n" + "="*70)
    print("JAWABAN: SOLUSI OPTIMAL")
    print("="*70)
    
    jam_s = int(x_opt)
    menit_s = int((x_opt - jam_s) * 60)
    
    jam_t = int(y_opt)
    menit_t = int((y_opt - jam_t) * 60)
    
    print(f"\nServer Standar: {x_opt} jam ({jam_s} jam {menit_s} menit)")
    print(f"Server Performa Tinggi: {y_opt} jam ({jam_t} jam {menit_t} menit)")
    print(f"Biaya Total Minimum: Rp {z_opt:,.0f}")
    
    # ==================== VERIFIKASI ====================
    print("\n" + "="*70)
    print("VERIFIKASI")
    print("="*70)
    
    k1 = instr_x*x_opt + instr_y*y_opt
    k2 = akses_x*x_opt + akses_y*y_opt
    
    print(f"\nInstruksi Pemrosesan: {k1:.0f} >= {instr_min} ✓")
    print(f"Akses Basis Data: {k2:.0f} >= {akses_min} ✓")
    print(f"Non-negativitas: x={x_opt}>=0, y={y_opt}>=0 ✓")
    
    # ==================== BREAKDOWN ====================
    print("\n" + "="*70)
    print("BREAKDOWN BIAYA")
    print("="*70)
    
    biaya_s = x_opt * biaya_x
    biaya_t = y_opt * biaya_y
    
    print(f"\nServer Standar: {x_opt} jam × Rp {biaya_x:,} = Rp {biaya_s:,.0f}")
    print(f"Server Performa Tinggi: {y_opt} jam × Rp {biaya_y:,} = Rp {biaya_t:,.0f}")
    print(f"{'Total Biaya:':<47} Rp {z_opt:,.0f}")
    
    # ==================== KAPASITAS ====================
    print("\n" + "="*70)
    print("KAPASITAS YANG DIHASILKAN")
    print("="*70)
    
    cap_instr_s = x_opt * instr_x
    cap_instr_t = y_opt * instr_y
    cap_akses_s = x_opt * akses_x
    cap_akses_t = y_opt * akses_y
    
    print(f"\nInstruksi Pemrosesan:")
    print(f"  Server Standar: {x_opt} × 20 = {cap_instr_s:.0f}")
    print(f"  Server Performa Tinggi: {y_opt} × 10 = {cap_instr_t:.0f}")
    print(f"  Total: {cap_instr_s+cap_instr_t:.0f} (Dibutuhkan: {instr_min}) ✓")
    
    print(f"\nAkses Basis Data:")
    print(f"  Server Standar: {x_opt} × 10 = {cap_akses_s:.0f}")
    print(f"  Server Performa Tinggi: {y_opt} × 30 = {cap_akses_t:.0f}")
    print(f"  Total: {cap_akses_s+cap_akses_t:.0f} (Dibutuhkan: {akses_min}) ✓")
    
    print("\n" + "="*70 + "\n")
else:
    print("\n✗ Tidak ada solusi feasible!")