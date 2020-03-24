# inkovis

Repo inkovis digunakan hanya untuk mevisualisasikan data infeksi COVID-19 di Indonesia. 

## Dataset

Data diperoleh dari situs Infeksi Emerging oleh Kementerian Kesehatan beralamat [infeksiemerging.kemkes.go.id](https://infeksiemerging.kemkes.go.id/). Dataset tersedia dalam format Excel dan CSV. Dataset diperoleh dari setiap pos yang dipublikasikan pada situs dan mengunduh laporan situasi terkini (yang berupa PDF). Pengisian dataset ini dilakukan secara manual (melihat seluruh dokumen PDF dan mencatatnya ke format Excel). Data disimpan dengan nama dokumen `data_infeksi_covid19_indonesia`. 

Dataset memiliki 9 kolom berupa:

- `tanggal`: Tanggal data dilaporkan (diambil dari informasi "Data dilaporkan sampai [tanggal]" di setiap dokumen situasi terkini).
- `jumlah_periksa`: Jumlah orang yang telah diperiksa / jumlah spesimen yang diterima.
- `positif`: Jumlah orang yang positif COVID-19.
- `sembuh`: Jumlah orang yang sembuh dari positif COVID-19.
- `meninggal`: Jumlah orang yang meninggal dari positif COVID-19.
- `negatif`: Jumlah orang yang negatif COVID-19.
- `proses_periksa`: Jumlah spesimen yang masih dalam proses pemeriksaan. Informasi ini hanya tersedia pada dokumen sebelum tanggal 21 Maret 2020.
- `kasus_perawatan`: Jumlah kasus dalam perawatan. Informasi ini tidak/belum tersedia pada dokumen situasi terkini. Informasi ini tersedia sejak tanggal 22 Maret 2020 pada update yang tersedia pada situsnya. 
- `catatan`: Informasi tambahan dari dokumen dan/atau komentar mengenai laporan data. 

