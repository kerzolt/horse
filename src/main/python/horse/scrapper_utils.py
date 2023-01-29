import logging
import datetime
import uuid
import re
import requests
import io
from os.path import exists, join
from bs4 import BeautifulSoup

from src.main.python.common import config
from src.main.python.common.db_utils import create_connection

# Logging
logging.basicConfig(level=logging.DEBUG)
LOGGER = logging.getLogger('scrapper_utils')

connection = create_connection()

#TODO
# deplacer les fct communes dans common/scrapper_utils
# rename horse_scrapper

def download_html(url, path, filename=""):
    # Init filename + filepath
    if filename == "":
        filename = get_filename_from_url(url)
    filepath = "{}{}".format(path, filename)

    # DL si n'existe pas deja
    if not exists(filepath):
        # Requete
        page = requests.get(url)
        html = page.text

        # Write file
        LOGGER.debug("Write {}{}".format(path, filename))
        with io.open(filepath, "w", encoding="utf-8") as file:
            file.write(html)
            
    return filepath

def get_filename_from_url(url):
    html_filename = re.search("[^/]*\.html$", url)
    if html_filename:
        filename = html_filename.group(0)
    else:
        filename = "{}.html".format(str(uuid.uuid1()))
        LOGGER.error("Impossible de trouver le nom du fichier dans l'url [{}] => filename = [{}]".format(url, filename))

    return filename

def load_html_from_file(filename):
    html = ""

    with open(filename, 'r') as file:
        html = file.read()

    return html

#---
# Canalturf
#---
def download_canalturf_meetings(start_date, end_date):
    for day_index in range(abs((start_date - end_date).days) + 1):
        date = start_date + datetime.timedelta(days=day_index)
        date_as_string = date.strftime('%Y-%m-%d')
        url = "{}?date={}".format(config["CANAL_TURF"]["RACES_LIST_URL"], date_as_string)

        download_html(url, config["CANAL_TURF"]["HTML_MEETINGS_PATH"], "{}_meetings.html".format(date_as_string))

def get_meetings_panels(html):
    soup = BeautifulSoup(html, "html.parser")
    races_accordion = soup.find(id="acc-listecourses")

    return races_accordion.find_all("div", class_="panel")

def get_meeting_location(meeting_html):
    location_title = meeting_html.find("span", class_="text-lg").text
    pos = location_title.find(" - ")
    if pos >= 0:
        location = location_title[pos + 3:]
    else:
        location = location_title

    return location

def download_meeting_races(meeting_html, date_as_string):
    races_html = meeting_html.find_all("div", class_="list-group-item")
    for race_html in races_html:
        # race_title = race_html.find("strong").text

        forecast_bton_html = race_html.find("a", class_="btn-primary")
        forecast_url = forecast_bton_html['href']
        forecast_filename = "{}_{}".format(date_as_string, get_filename_from_url(forecast_url))
        download_html(forecast_url, config["CANAL_TURF"]["HTML_RACES_FORECAST_PATH"], forecast_filename)

        result_bton_html = race_html.find("a", class_="btn-danger")
        result_url = result_bton_html['href']
        result_filename = "{}_{}".format(date_as_string, get_filename_from_url(result_url))
        download_html(result_url, config["CANAL_TURF"]["HTML_RACES_RESULTS_PATH"], result_filename)

def download_canalturf_races(start_date, end_date):
    for day_index in range(abs((start_date - end_date).days) + 1):
        date = start_date + datetime.timedelta(days=day_index)
        date_as_string = date.strftime('%Y-%m-%d')

        filepath = "{}{}".format(config["CANAL_TURF"]["HTML_MEETINGS_PATH"], "{}_meetings.html".format(date_as_string))
        if exists(filepath):
            # Load html
            html = load_html_from_file(filepath)
            # Recup liste des meetings
            meetings_panel = get_meetings_panels(html)
            for meeting_html in meetings_panel:
                download_meeting_races(meeting_html, date_as_string)
        else:
            LOGGER.error("Le fichier meetings [{}] n'existe pas".format(filepath))

def download_canalturf_horses(start_date, end_date):
    for day_index in range(abs((start_date - end_date).days) + 1):
        date = start_date + datetime.timedelta(days=day_index)
        date_as_string = date.strftime('%Y-%m-%d')

        # results_files = [f for f in listdir(config["CANAL_TURF"]["HTML_RACES_RESULTS_PATH"]) if f.startswith(date_as_string)]
        results_files = ["2021-01-01_229564_prix-de-chambly.html"]
        for results_file in results_files:
            html = load_html_from_file(join(config["CANAL_TURF"]["HTML_RACES_RESULTS_PATH"], results_file))
            soup = BeautifulSoup(html, "html.parser")
            horses_a_html = soup.find_all("a", href=lambda value: value and value.startswith(config["CANAL_TURF"]["HORSES_URL"]))
            for horse_a_html in horses_a_html:
                url = horse_a_html['href']
                horse_id = url.split("=", 1)[1]
                download_html(url, config["CANAL_TURF"]["HTML_HORSES_PATH"], "horse_{}.html".format(horse_id))
