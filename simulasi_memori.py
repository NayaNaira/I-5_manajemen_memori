# simulasi_memori.py - Analisis Memori Server Database UMKM (srv-toko-250660121067)
import math

KB, MB, GB = 1024, 1024**2, 1024**3
ALAMAT_UJI = [8192, 50000, 2097152]
UKURAN_PAGE = {"4 KB": 4 * KB, "2 MB": 2 * MB}

# Asumsi pemetaan frame fisik pada page table
PETA_FRAME = {
    "4 KB": {2: 5, 12: 18, 512: 100},
    "2 MB": {0: 3, 1: 7},
}

print("=== 1. TRANSLASI ALAMAT LOGIS -> FISIK ===")
for nama, ps in UKURAN_PAGE.items():
    print(f"\n[Ukuran Page: {nama} = {ps} byte]")
    for a in ALAMAT_UJI:
        p, d = divmod(a, ps)
        f = PETA_FRAME[nama][p]
        fisik = (f * ps) + d
        print(f"  Logis {a:>7} -> page={p:<3} | offset={d:<7} | frame={f:<3} | fisik=({f}*{ps})+{d} = {fisik}")

print("\n=== 2. PERHITUNGAN TLB REACH ===")
for entri in (64, 1024):
    for nama, ps in UKURAN_PAGE.items():
        reach = entri * ps
        print(f"  {entri:>4} entri x {nama}: {reach:>10} byte = {reach/KB:>6.0f} KB = {reach/MB:>6.2f} MB")

print("\n=== 3. EFFECTIVE ACCESS TIME (t_TLB=20 ns, t_mem=100 ns) ===")
t_tlb, t_mem = 20, 100
for h in (0.80, 0.90, 0.95, 0.99):
    eat = h * (t_tlb + t_mem) + (1 - h) * (t_tlb + 2 * t_mem)
    print(f"  Hit ratio {h*100:>2.0f}% -> EAT = {eat:>5.1f} ns (slowdown {eat/t_mem:.2f}x terhadap akses RAM murni)")

print("  Skenario Multi-Level Page Walk x86-64 (4-level utk 4 KB vs 3-level utk 2 MB):")
eat_4k_ml = 0.80 * (t_tlb + t_mem) + 0.20 * (t_tlb + 5 * t_mem)
eat_2m_ml = 0.99 * (t_tlb + t_mem) + 0.01 * (t_tlb + 4 * t_mem)
print(f"    4 KB (hit 80%, 4-level walk): EAT = {eat_4k_ml:.1f} ns")
print(f"    2 MB (hit 99%, 3-level walk): EAT = {eat_2m_ml:.1f} ns")

print("\n=== 4. UKURAN PAGE TABLE (ARSITEKTUR 64-BIT / PTE 8 BYTE) ===")
for nama, ps in UKURAN_PAGE.items():
    entri_1gb = (1 * GB) // ps
    entri_8gb = (8 * GB) // ps
    print(f"  {nama} (Buffer 1 GB): {entri_1gb:>7} entri -> {(entri_1gb*8)/KB:>7.1f} KB ({(entri_1gb*8)/MB:.3f} MB)")
    print(f"  {nama} (Buffer 8 GB): {entri_8gb:>7} entri -> {(entri_8gb*8)/KB:>7.1f} KB ({(entri_8gb*8)/MB:.3f} MB)")

print("\n=== 5. FRAGMENTASI INTERNAL ===")
for alokasi in (2097153, 4_500_000):
    for nama, ps in UKURAN_PAGE.items():
        jml_page = math.ceil(alokasi / ps)
        sisa = (jml_page * ps) - alokasi
        print(f"  Alokasi {alokasi:>7} B ({nama}): butuh {jml_page:>4} page | sisa = {sisa:>7} B ({sisa/ps*100:.2f}% dari 1 page)")
