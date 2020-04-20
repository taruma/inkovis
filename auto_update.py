import re
from tika import parser
from datetime import datetime, timezone, timedelta
import pandas as pd
import requests
import logging
from bs4 import BeautifulSoup


logging.basicConfig(level=logging.DEBUG)

# MODULE SOUP


def _as_nama_bulan(month):
    nama_bulan = {
        1: 'januari',
        2: 'februari',
        3: 'maret',
        4: 'april',
        5: 'mei',
        6: 'juni',
        7: 'juli',
        8: 'agustus',
        9: 'september',
        10: 'oktober',
        11: 'november',
        12: 'desember'
    }

    return nama_bulan[month]


def url_from_date(date):
    text = (
        'https://covid19.kemkes.go.id/situasi-infeksi-emerging/' +
        'info-corona-virus/situasi-terkini-perkembangan-coronavirus-disease' +
        '-covid-19-' + '{day}-{month}-{year}' + '/')

    day = date.day
    month = _as_nama_bulan(date.month)
    year = date.year

    return text.format(day=day, month=month, year=year)


def get_soup_from_url(url):

    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        return soup


def get_pdf_link(soup, text_to_find='situasi_terkini'):
    for a in soup.find_all('a'):
        link = a.get('href')
        link = link if link is not None else ''
        if link.endswith('pdf') and (text_to_find in link.lower()):
            return link

# DOWNLOAD DATASET


print('DONWLOAD DATASET')

url_dataset = "dataset/data_infeksi_covid19_indonesia.csv"
dataset = pd.read_csv(url_dataset, index_col=0, parse_dates=True)

# FIND DIFFERENCE

print('CHECK DIFFERENCE')

now_jakarta = datetime.now(timezone(timedelta(hours=7)))
now_systems = datetime.now()

diff = pd.date_range('20200218', now_systems,
                     freq='D')[:-1].difference(dataset.index)
diff = diff + pd.DateOffset(days=1)

# DOWNLOAD


def scrape_for_reports(diff):

    reports = []

    for date in diff:
        _url = url_from_date(date)
        _soup = get_soup_from_url(_url)

        if _soup is not None:
            _link = get_pdf_link(_soup)
            _date_report = date.strftime('%Y_%m_%d')
            _report_name = 'situasi_terkini_{}.pdf'.format(_date_report)
            reports.append((_link, _report_name))

    return reports


reports = scrape_for_reports(diff)


def download_reports(reports, directory='dataset/pdf/'):
    res = []
    for link, name in reports:
        r = requests.get(link)
        if r.status_code == 200:
            with open(directory + name, 'wb') as f:
                f.write(r.content)
            print('SUCCESS: ', directory + name)
            res.append(directory + name)
    return res


print('DOWNLOADING REPORTS')

download_reports(reports)

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
    f.write('RUN: ' + now_jakarta.strftime('%Y-%m-%d %H:%M') + '\n')

with open('docs/_data/logdata.yml', 'w') as f:
    f.write("date: " + now_jakarta.strftime('%Y-%m-%d') + '\n')

print('FINISH')
