import re
from tika import parser
from datetime import datetime, timezone, timedelta
import pandas as pd
import requests

# DOWNLOAD DATASET

print('DONWLOAD DATASET')

url_dataset = (
    "https://raw.githubusercontent.com/taruma/inkovis" +
    "/master/dataset/data_infeksi_covid19_indonesia.csv")
dataset = pd.read_csv(url_dataset, index_col=0, parse_dates=True)

# FIND DIFFERENCE

print('CHECK DIFFERENCE')

now_jakarta = datetime.now(timezone(timedelta(hours=7)))
now_systems = datetime.now()

diff = pd.date_range('20200218', now_systems,
                     freq='D').difference(dataset.index)[1:]

# DOWNLOAD


def download_report(date, dir=''):
    base_url = (
        'https://infeksiemerging.kemkes.go.id/download' +
        '/Situasi_Terkini_{}.pdf')
    date_url = date.strftime('%d%m%y')

    url = base_url.format(date_url)
    r = requests.get(url)

    report_name = 'situasi_terkini_{}.pdf'

    date_report = date.strftime('%Y_%m_%d')
    file_name = report_name.format(date_report)
    if r.status_code == 200:
        with open(dir + file_name, 'wb') as f:
            f.write(r.content)
        return file_name
    else:
        return None

# DOWNLOAD MISSING DATA/PDF


print('DOWNLOADING REPORT')

valid_date = []
for date in diff:
    status = download_report(date, dir='dataset/pdf/')
    valid_date.append(date) if status is not None else None

# PARSE/RETRIEVE INFORMATION


def _remove_special(text):
    for special in '() .':
        text = text.replace(special, '')
    return text.lower()


def _retrieve_text(date, file='situasi_terkini_{}.pdf', dir=''):
    path_file = dir + file.format(date.strftime('%Y_%m_%d'))

    raw = parser.from_file(path_file)

    return _remove_special(raw['content'])


def _retrieve_number(keyword, text):
    keyword = _remove_special(keyword)
    regex = re.compile(f'{keyword}:(\\d+)')
    res = regex.findall(text)
    if res:
        return int(res[0])
    else:
        return 0


text_to_find = [
    'Jumlah orang yang diperiksa',
    'Positif COVID-19',
    'Sembuh (Positif COVID-19)',
    'Meninggal (Positif COVID-19)',
    'Negatif COVID-19',
    'Proses Pemeriksaan'
]

col_text = [
    'jumlah_periksa',
    'konfirmasi',
    'sembuh',
    'meninggal',
    'negatif',
    'proses_periksa',
]


def _get_dict_covid(date, file='situasi_terkini_{}.pdf', dir=''):

    text = _retrieve_text(date, file=file, dir=dir)

    res = dict()
    res['tanggal'] = date + pd.DateOffset(-1)

    for info, col_name in zip(text_to_find, col_text):
        res[col_name] = _retrieve_number(info, text)

    res['catatan'] = '[automated]'
    return res


def add_new_data(dataset, new_dict):

    new_data = pd.DataFrame.from_dict(
        new_dict, orient='index'
    ).T.set_index('tanggal')

    return pd.concat((dataset, new_data), axis=0)

# ADD NEW DATA


print('READ REPORT AND ADD NEW DATASET')

for date in diff:
    new_data = _get_dict_covid(date, dir='dataset/pdf/')
    dataset = add_new_data(dataset, new_data)

print('SAVE DATASET')

save_path = 'dataset/data_infeksi_covid19_indonesia.csv'
dataset.to_csv(save_path)

print('SAVE LOG')

with open('log_data', 'a') as f:
    f.write('RUN: ' + now_jakarta.strftime('%Y-%m-%d %H:%M'))

print('FINISH')
