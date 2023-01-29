import datetime

import src.main.python.horse.scrapper_utils as scrapper_utils

def download_canalturf_meetings(start_date, end_date):
    print('--- download_canalturf_meetings ---')
    scrapper_utils.download_canalturf_meetings(start_date, end_date)

def download_canalturf_races(start_date, end_date):
    print('--- download_canalturf_races ---')
    scrapper_utils.download_canalturf_races(start_date, end_date)

def download_canalturf_horses(start_date, end_date):
    print('--- download_canalturf_horses ---')
    scrapper_utils.download_canalturf_horses(start_date, end_date)

if __name__ == '__main__':
    start_date_test = datetime.datetime.strptime('2021-01-01', "%Y-%m-%d")
    end_date_test = datetime.datetime.strptime('2021-01-01', "%Y-%m-%d")

    # download_canalturf_meetings(start_date_test, end_date_test)
    # download_canalturf_races(start_date_test, end_date_test)
    download_canalturf_horses(start_date_test, end_date_test)
