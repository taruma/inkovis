import inkovis
import pandas as pd
import matplotlib.pyplot as plt

# PENGATURAN PARAMS VISUALISASI
FIG_SIZE = (35, 8)
FIG_SIZE_GROUP = (35, 12)

# DATASET
# ALAMAT_DATASET = (
#     'https://github.com/taruma/inkovis/raw/master' +
#     '/dataset/data_infeksi_covid19_indonesia.csv')
ALAMAT_DATASET = '../dataset/data_infeksi_covid19_indonesia.csv'
dataset_inkovis = pd.read_csv(
    ALAMAT_DATASET, index_col=0, parse_dates=True, header=0)

# PARAM FUNGSI
DATASET = dataset_inkovis[-31:]
MASK = None
DAYS = 1

# ===================================

# KASUS KONFIRMASI

# AKUMULASI

# VARIASI 1
fig, ax = plt.subplots(
    nrows=2, ncols=1, figsize=FIG_SIZE_GROUP, sharex=True,
    gridspec_kw={'height_ratios': [2, 1]})

inkovis.plot_confirmed_case(
    dataset=DATASET, ax=ax[0], mask=MASK, days=DAYS,
    show_diff_bar=False, show_info=False, show_hist=True
)

inkovis.plot_confirmed_growth(
    dataset=DATASET, ax=ax[1], mask=MASK, days=DAYS,
    show_bar=True,
    show_numbers=True,
    show_confirmed=False, show_total_numbers=True,
    show_title=True, show_info=False,
    show_legend=True
)
ax[0].set_xlabel('')

plt.savefig('grafik/31hariakhir_kasuskonfirmasi_01.png', dpi=150)
plt.close(fig)

# VARIASI 2
fig, ax = plt.subplots(figsize=FIG_SIZE)

inkovis.plot_confirmed_case(
    dataset=DATASET, ax=ax, mask=MASK, days=DAYS,
    show_hist=True, show_diff_bar=False,
    show_info=False)

plt.savefig('grafik/31hariakhir_kasuskonfirmasi_02.png', dpi=150)
plt.close(fig)

# VARIASI 3
fig, ax = plt.subplots(figsize=FIG_SIZE)

inkovis.plot_confirmed_case(
    dataset=DATASET, ax=ax, mask=MASK, days=DAYS,
    show_hist=True, show_diff_bar=True,
    show_diff_numbers=True,
    show_info=False)

plt.savefig('grafik/31hariakhir_kasuskonfirmasi_03.png', dpi=150)
plt.close(fig)

# VARIASI 4
fig, ax = plt.subplots(figsize=FIG_SIZE)

inkovis.plot_confirmed_case(
    dataset=DATASET, ax=ax, mask=MASK, days=DAYS,
    show_numbers=False, show_diff_bar=False,
    show_info=False)

ax.margins(y=0.1)

plt.savefig('grafik/31hariakhir_kasuskonfirmasi_04.png', dpi=150)
plt.close(fig)

# PERKEMBANGAN KONFIRMASI

# VARIASI 1

fig, ax = plt.subplots(figsize=FIG_SIZE)
inkovis.plot_confirmed_growth(
    dataset=DATASET, ax=ax, mask=MASK, days=DAYS,
    show_info=False,
    show_confirmed=True, show_confirmed_numbers=True)

plt.savefig('grafik/31hariakhir_perkembangankonfirmasi_01.png', dpi=150)
plt.close(fig)

# VARIASI 2

fig, ax = plt.subplots(
    nrows=2, ncols=1, figsize=FIG_SIZE_GROUP, sharex=True,
    gridspec_kw={'height_ratios': [1, 3]})

inkovis.plot_confirmed_case(
    dataset=DATASET, ax=ax[0], mask=MASK, days=DAYS,
    show_diff_bar=False, show_info=False, show_hist=False
)

inkovis.plot_confirmed_growth(
    dataset=DATASET, ax=ax[1], mask=MASK, days=DAYS,
    show_bar=True, show_confirmed=True,
    show_numbers=True,
    show_total_numbers=True, show_title=False, show_info=False,
    show_legend=False
)
ax[0].set_xlabel('')

plt.savefig('grafik/31hariakhir_perkembangankonfirmasi_02.png', dpi=150)
plt.close(fig)

# JUMLAH SPESIMEN

# VARIASI 1

fig, ax = plt.subplots(
    nrows=2, ncols=1, figsize=FIG_SIZE_GROUP, sharex=True,
    gridspec_kw={'height_ratios': [2, 1]})

inkovis.plot_testing_case(
    dataset=DATASET, ax=ax[0], mask=MASK, days=DAYS,
    show_diff_bar=False, show_info=False, show_hist=True
)

inkovis.plot_testing_growth(
    dataset=DATASET, ax=ax[1], mask=MASK, days=DAYS,
    show_bar=True, show_confirmed=False,
    show_numbers=True,
    show_total_numbers=True, show_title=True, show_info=False,
    show_legend=True
)

ax[0].set_xlabel('')
plt.savefig('grafik/31hariakhir_jumlahspesimen_01.png', dpi=150)
plt.close(fig)

# VARIASI 2
fig, ax = plt.subplots(figsize=FIG_SIZE)

inkovis.plot_testing_case(
    dataset=DATASET, ax=ax, mask=MASK, days=DAYS,
    show_hist=True, show_diff_bar=False,
    show_info=False)

plt.savefig('grafik/31hariakhir_jumlahspesimen_02.png', dpi=150)
plt.close(fig)

# VARIASI 3
fig, ax = plt.subplots(figsize=FIG_SIZE)

inkovis.plot_testing_case(
    dataset=DATASET, ax=ax, mask=MASK, days=DAYS,
    show_hist=True, show_diff_bar=True,
    show_diff_numbers=True,
    show_info=False)

plt.savefig('grafik/31hariakhir_jumlahspesimen_03.png', dpi=150)
plt.close(fig)

# VARIASI 4
fig, ax = plt.subplots(figsize=FIG_SIZE)

inkovis.plot_testing_case(
    dataset=DATASET, ax=ax, mask=MASK, days=DAYS,
    show_numbers=False, show_diff_bar=False,
    show_info=False)

ax.margins(y=0.1)

plt.savefig('grafik/31hariakhir_jumlahspesimen_04.png', dpi=150)
plt.close(fig)

# PERKEMBANGAN SPESIMEN

# VARIASI 1

fig, ax = plt.subplots(figsize=FIG_SIZE)
inkovis.plot_testing_growth(
    dataset=DATASET, ax=ax, mask=MASK, days=DAYS,
    show_info=False,
    show_confirmed=True, show_confirmed_numbers=True)

plt.savefig('grafik/31hariakhir_perkembanganspesimen_01.png', dpi=150)
plt.close(fig)

# VARIASI 2

fig, ax = plt.subplots(
    nrows=2, ncols=1, figsize=FIG_SIZE_GROUP, sharex=True,
    gridspec_kw={'height_ratios': [1, 3]})

inkovis.plot_testing_case(
    dataset=DATASET, ax=ax[0], mask=MASK, days=DAYS,
    show_diff_bar=False, show_info=False, show_hist=False
)

inkovis.plot_testing_growth(
    dataset=DATASET, ax=ax[1], mask=MASK, days=DAYS,
    show_bar=True, show_confirmed=True,
    show_numbers=True,
    show_total_numbers=True, show_title=False, show_info=False,
    show_legend=False
)
ax[0].set_xlabel('')

plt.savefig('grafik/31hariakhir_perkembanganspesimen_02.png', dpi=150)
plt.close(fig)


# KOMBINASI

# VARIASI 1

fig, ax = plt.subplots(
    nrows=2, ncols=1, figsize=FIG_SIZE_GROUP, sharex=True,
    gridspec_kw={'height_ratios': [1, 1]})

_DATASET = dataset_inkovis

inkovis.plot_confirmed_case(
    dataset=DATASET, ax=ax[0], mask=MASK, days=DAYS,
    show_hist=True, show_diff_bar=True,
    show_diff_numbers=True,
    show_info=False, show_title=False
)

inkovis.plot_testing_case(
    dataset=DATASET, ax=ax[1], mask=MASK, days=DAYS,
    show_hist=True, show_diff_bar=True,
    show_diff_numbers=True,
    show_info=False, show_title=False
)

fig.suptitle("KASUS KONFIRMASI DAN JUMLAH SPESIMEN COVID-19 DI INDONESIA",
             fontweight='bold', fontsize='xx-large')
fig.subplots_adjust(top=0.95)

ax[0].set_xlabel('')
plt.savefig('grafik/31hariakhir_kombinasi_01.png', dpi=150)
plt.close(fig)

# VARIASI 2

fig, ax = plt.subplots(
    nrows=2, ncols=1, figsize=FIG_SIZE_GROUP, sharex=True,
    gridspec_kw={'height_ratios': [1, 1]})

_DATASET = dataset_inkovis

inkovis.plot_confirmed_growth(
    dataset=DATASET, ax=ax[0], mask=MASK, days=DAYS,
    show_bar=True, show_confirmed=True,
    show_numbers=True,
    show_total_numbers=True, show_title=False, show_info=False,
)
inkovis.plot_testing_growth(
    dataset=DATASET, ax=ax[1], mask=MASK, days=DAYS,
    show_bar=True, show_confirmed=True,
    show_numbers=True,
    show_total_numbers=True, show_title=False, show_info=False,
)

fig.suptitle(
    "PERKEMBANGAN KASUS KONFIRMASI DAN JUMLAH SPESIMEN COVID-19 DI" +
    "INDONESIA",
    fontweight='bold', fontsize='xx-large')
fig.subplots_adjust(top=0.95)

ax[0].set_xlabel('')
plt.savefig('grafik/31hariakhir_kombinasi_02.png', dpi=150)
plt.close(fig)
