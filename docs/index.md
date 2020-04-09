---
layout: home
---

<div align="center" class="m-2">
    <h1 class="f00-light">$inkovis$ project</h1>
    <img alt="GitHub last commit" class="mb-3" src="https://img.shields.io/github/last-commit/taruma/inkovis?label=LAST%20UPDATE&logo=github&style=for-the-badge"><br>
    Proyek $inkovis$ berisikan modul <em>python</em> bernama inkovis dan <em>jupyter notebook</em> (buku) yang dapat digunakan untuk
    memvisualisasikan data infeksi COVID-19 di Indonesia.
</div>

-----

{% include alert.html text="Kunjungi halaman <b><a href=\"https://github.com/taruma/inkovis \">github</a></b> untuk mengetahui status/informasi proyek ini."%}

{% include info.html text="Dataset inkovis diperbarui otomatis setiap jam 17.00 WIB. Dan situs ini diperbarui otomatis setiap jam 17.30 WIB. Lihat statusnya <a href=\"https://github.com/taruma/inkovis/actions\">disini</a>."%}

{% include lastdata.html %}

-----

<div align="center" class="m-2" markdown="1">
__Kunjungi halaman dibawah ini untuk melihat visualisasi data infeksi COVID-19 di Indonesia__
</div>


<div class="Box my-3 border-green" style="border:3px solid">
    <div class="Box-row d-flex flex-wrap flex-justify-center">
        <a href="{{site.baseurl}}{% link _posts/2020-04-09-31hariakhir.md %}" role="button"
            class="btn m-1 btn-outline">Grafik 31 Hari Terakhir</a>
        <a aria-disabled="true" href="#" role="button"
            class="btn m-1 btn-outline">Grafik Seluruh Data</a>
        <!-- <a aria-disabled="true" class="btn m-1 btn-outline" href="#url" role="button">Laporan</a>
        <a aria-disabled="true" class="btn m-1 btn-outline" href="#url" role="button">Video</a> -->
    </div>
</div>