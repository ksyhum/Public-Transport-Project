import requests
import py7zr
import os
import shutil

# Number of days to download
n = 2

# API Key dan URL Template
api_key = ""
url_template = "https://api.koda.trafiklab.se/KoDa/api/v2/gtfs-rt/sl/TripUpdates?date=2024-01-{day}&hour={hour}&key={key}"

# Base output directory
base_output_dir = r"D:\Humam\KTH\Github\Public Transport\extracted_files"

# Loop untuk setiap hari
for i in range(1, n + 1):
    day = 15 + i  # Set Date
    date_folder = os.path.join(base_output_dir, f"2024-01-{day}", f"{day:02d}")
    os.makedirs(date_folder, exist_ok=True)  # Buat folder tanggal

    for hour in range(0, 24):
        formatted_hour = f"{hour:02d}"
        filename = f"TripUpdates2024_{day}_{formatted_hour}.7z"

        # Build the download URL
        url = url_template.format(day=day, hour=formatted_hour, key=api_key)

        print(f"Downloading: {url}")

        # Download the file
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            with open(filename, "wb") as file:
                for chunk in response.iter_content(chunk_size=8192):
                    file.write(chunk)

            # Extract the archive directly into the date folder
            with py7zr.SevenZipFile(filename, mode="r") as zip_file:
                zip_file.extractall(path=date_folder)

            print(f"Downloaded and extracted: {filename} to {date_folder}")
        else:
            print(f"Failed to download: {url} (Status code: {response.status_code})")

        # Optional: Remove the downloaded file to save space
        if os.path.exists(filename):
            os.remove(filename)
