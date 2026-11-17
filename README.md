# I-5: Translasi Alamat dan Manajemen Memori

Repositori artefak praktik dan analisis **Tugas Individu I-5** mata kuliah **Sistem Operasi (USA-WP2260110)** — **Kepingan Puzzle #8 (Modul Proyek UAS)**. Studi kasus berfokus pada evaluasi kinerja manajemen memori virtual (*paging* dan *Translation Lookaside Buffer*) untuk layanan basis data (*database*) digital UMKM pada instans virtual Linux `srv-toko-250660121067`.

| Identitas | Keterangan |
| :--- | :--- |
| **Nama** | Naya Naira Zahra |
| **NIM** | `250660121067` |
| **Kelas / Tema** | Kelas D — Cloud dan Layanan Digital UMKM |
| **Host VM** | `mhs@srv-toko-250660121067` |
| **Dosen Pengampu** | Muhammad Agreindra Helmiawan, S.Kom., M.T |
| **Institusi** | Program Studi S1 Informatika, Fakultas Teknologi Informasi — Universitas Sebelas April (2026) |

---

## Deskripsi & Tujuan

Pengujian ini membandingkan efektivitas penggunaan ***Standard Page* (`4 KB` / `4.096 byte`)** dan ***Huge Page* (`2 MB` / `2.097.152 byte`)** pada beban kerja server basis data UMKM melalui tiga tujuan utama:

1. **Translasi Alamat Logis ke Fisik:** Menghitung nomor *page* ($p$), *offset* ($d$), dan alamat fisik untuk sampel alamat logis `8.192`, `50.000`, dan `2.097.152` pada ukuran *page* `4 KB` dan `2 MB`.
2. **Evaluasi TLB & EAT:** Menjelaskan peran *Translation Lookaside Buffer* (TLB) serta menghitung *TLB reach* (`64` dan `1.024` entri) dan *Effective Access Time* (EAT) pada variasi *hit ratio* (`80%` vs `99%`).
3. **Analisis Ukuran *Page Table* & Fragmentasi:** Menganalisis dampak perbedaan ukuran halaman terhadap konsumsi memori struktur *page table* (arsitektur 64-bit, $\text{PTE} = 8\text{ byte}$) dan fragmentasi internal (*internal fragmentation*).

---

## Lingkungan Praktik & Parameter Uji

* **Sistem Operasi VM:** Ubuntu 26.04.1 (`7.0.0-38-generic`), RAM 2 GB, 1 vCPU (VirtualBox 7.2.20)
* **Konfigurasi Memori Kernel Terobservasi:**
  * `PAGESIZE = 4096` *byte* (`4 KB`)
  * `Hugepagesize = 2048 kB` (`2 MB`)
  * `PageTables = 3368 kB`
* **Parameter Simulasi:**
  * Alamat logis uji: `8.192`, `50.000`, `2.097.152`
  * Asumsi pemetaan *frame*:
    * `4 KB`: $\text{Page } 2 \rightarrow \text{Frame } 5$, $\text{Page } 12 \rightarrow \text{Frame } 18$, $\text{Page } 512 \rightarrow \text{Frame } 100$
    * `2 MB`: $\text{Page } 0 \rightarrow \text{Frame } 3$, $\text{Page } 1 \rightarrow \text{Frame } 7$
  * Latensi perangkat keras: $t_{\text{TLB}} = 20\text{ ns}$, $t_{\text{mem}} = 100\text{ ns}$

---

## Struktur Artefak Repositori

```text
I-5_manajemen_memori/
├── README.md                                  # Dokumentasi repositori
├── simulasi_memori.py                         # Skrip Python validasi perhitungan manajemen memori
├── screenshots/                               # Bukti tangkapan layar terminal VM (Gambar 4.1 & 4.2)
└── D_I-5_250660121067_Naya Naira Zahra.pdf    # Laporan lengkap Tugas Individu I-5
