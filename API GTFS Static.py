import requests
from datetime import datetime, timedelta
import io
import zipfile
import os


def download_and_extract_zip(url, directory):
    response = requests.get(url)
    if response.status_code == 200:
        zip_file = zipfile.ZipFile(io.BytesIO(response.content))
        zip_file.extractall(directory)
        print(f"Data berhasil diunduh dan diekstrak ke {directory}")
    else:
        print("Gagal mengunduh data")



base_directory = "D:\Humam\KTH\Github\Public Transport\Static"


base_url = "https://api.koda.trafiklab.se/KoDa/api/v2/gtfs-static/sl"
# API key
api_key = "   "

start_date = datetime(2021, 1, 12)
end_date = datetime(2021, 1, 13)


current_date = start_date
while current_date <= end_date:
    date_str = current_date.strftime('%Y-%m-%d')
    directory = os.path.join(base_directory, f"data_{date_str}")
    if not os.path.exists(directory):
        os.makedirs(directory)
    full_url = f"{base_url}?date={date_str}&key={api_key}"
    download_and_extract_zip(full_url, directory)

    current_date += timedelta(days=1)