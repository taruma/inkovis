# inkovis

Repo inkovis berisikan modul `inkovis` dan _jupyter notebook_ (buku) yang dapat digunakan untuk mevisualisasikan data infeksi COVID-19 di Indonesia. 

## Modul inkovis

### Pemasangan

Untuk menggunakan modul inkovis, Anda membutuhkan dua modul yaitu `inkovis.py` dan `so.py`. `inkovis.py` merupakan modul utama yang berisikan fungsi untuk memvisualisasikan data. `so.py` merupakan modul tambahan yang berisikan fungsi dari orang lain yang digunakan. 

Jika menggunakan jupyter notebook/google colab/kaggle kernel, bisa menggunakan kode berikut: 

```python
!wget -O inkovis.py "https://github.com/taruma/inkovis/raw/master/notebook/inkovis.py" -q
!wget -O so.py "https://github.com/taruma/inkovis/raw/master/notebook/so.py" -q
```

Atau bisa juga diunduh filenya pada tautan berikut: [inkovis.py](https://github.com/taruma/inkovis/blob/master/notebook/inkovis.py), [so.py](https://github.com/taruma/inkovis/blob/master/notebook/so.py).

### Penggunaan

Fungsi yang tersedia pada modul inkovis meminta input dataset objek `pandas.DataFrame` dan objek `matplotlib.axes.Axes`.

```python
fig, ax = plt.subplots()

inkovis.plot_confirmed_case(dataset, ax)
```

Contoh lainnya:

```python
fig, ax = plt.subplots(nrows=2, ncols=1, sharex=True, gridspec_kw={'height_ratios':[1, 3]})

inkovis.plot_confirmed_case(
    dataset, ax[0],
    show_diff_bar=False, show_info=False, show_hist=False)

inkovis.plot_confirmed_growth(
    dataset, ax[1], 
    show_bar=True, show_confirmed=True, 
    show_numbers=True,
    show_total_numbers=True, show_title=False, show_info=False,
    show_legend=False)
```

Untuk saat ini, belum tersedia dokumentasi mengenai penggunaan modul inkovis. 

### Modul `so.py`

Modul inkovis menggunakan potongan kode/fungsi berikut yang disimpan pada file `so.py`:
- [[From Stackoverflow]: Matplotlib axis with two scales shared origin](https://stackoverflow.com/a/46901839/4886384). Menggunakan potongan kode yang disediakan oleh Tim P.



## Dataset

Data diperoleh dari situs Infeksi Emerging oleh Kementerian Kesehatan beralamat [infeksiemerging.kemkes.go.id](https://infeksiemerging.kemkes.go.id/). Dataset tersedia dalam format Excel dan CSV. Dataset diperoleh dari setiap pos yang dipublikasikan pada situs dan mengunduh laporan situasi terkini (yang berupa PDF). Pengisian dataset ini dilakukan secara manual (melihat seluruh dokumen PDF dan mencatatnya ke format Excel, sehingga kekeliruan bisa dapat terjadi). Data disimpan dengan nama dokumen `data_infeksi_covid19_indonesia`. 

Dataset memiliki 9 kolom berupa:

- `tanggal`: Tanggal data dilaporkan (diambil dari informasi "Data dilaporkan sampai [tanggal]" di setiap dokumen situasi terkini).
- `jumlah_periksa`: Jumlah orang yang telah diperiksa / jumlah spesimen yang diterima.
- `konfirmasi`: Jumlah orang yang positif COVID-19.
- `sembuh`: Jumlah orang yang sembuh dari positif COVID-19.
- `meninggal`: Jumlah orang yang meninggal dari positif COVID-19.
- `negatif`: Jumlah orang yang negatif COVID-19.
- `proses_periksa`: Jumlah spesimen yang masih dalam proses pemeriksaan.
- `kasus_perawatan`: Jumlah kasus dalam perawatan. Informasi ini tidak/belum tersedia pada dokumen situasi terkini. Informasi ini tersedia sejak tanggal 22 Maret 2020 pada update yang tersedia pada situsnya. 
- `catatan`: Informasi tambahan dari dokumen dan/atau komentar mengenai laporan data. 

Informasi tambahan:

- Jumlah orang yang diambil spesimen dan memenuhi kriteria PDP/ODP/Kontak. (dari laporan situasi terkini 15 Maret 2020). *Informasi ini terkait pengurangan jumlah spesimen.
- Per tanggal 16 Maret 2020, data jumlah orang yang diperiksa hanya data orang yang memenuhi kriteria PDP/ODP/Kontak. Sedangkan pada update sebelumnya, data masih memasukkan orang yang tidak memenuhi tiga kriteria diatas sehingga terjadi pengurangan data jumlah orang yang diperiksa dan jumlah kasus negatif Per tanggal 16 Maret 2020. (dari laporan situasi terkini 16/17 Maret 2020) 

### Catatan mengenai dataset

- Digunakannya nama kolom `konfirmasi` mengikuti infografik yang tersedia di situs infeksi emerging (yang diperbarui per tanggal 22 Maret 2020). Sebelumnya, digunakan nama `positif` dikarenakan pada laporan situasi terkini menggunakan kalimat "Positif COVID-19: ...".
- Kolom `jumlah_periksa` merupakan penjumlahan antara kolom `konfirmasi`, `negatif`, dan `proses_periksa`. `jumlah_periksa == konfirmasi + negatif + proses_periksa`.
- Kolom `kasus_perawatan` merupakan sisa kolom `konfirmasi` yang telah dikurangi oleh `sembuh` dan `meninggal`. `kasus_perawatan == konfirmasi - (sembuh + meninggal)`.
- Informasi `proses_periksa` tidak tersedia sejak 22 Maret 2020.
- Informasi `kasus_perawatan` mulai tersedia pada infografik sejak 22 Maret 2020.
- Istilah "Spesimen Diterima" (yang tertampil pada infografik di situs) nilainya sama dengan "Jumlah orang yang diperiksa". Sehingga, diasumsikan bahwa angka tersebut menyatakan jumlah pengujian yang telah dilakukan.
- Angka yang tersedia pada laporan situasi terkini ditemukan memiliki kekeliruan seperti angka `jumlah_periksa` tidak memiliki nilai yang sama dengan total kolom `konfirmasi`, `negatif`, dan `proses_periksa`. Tetapnya menggunakan informasi dari laporan situasi terkini agar konsisten dan memudahkan dalam memastikan perolehan data. Sehingga, repo ini lebih fokus memvisualisasikan data, dan bukan untuk memvalidasi data ataupun menganalisis data.