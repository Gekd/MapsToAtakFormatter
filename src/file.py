import os
import re
from zipfile import ZipFile, ZIP_DEFLATED
import shutil
import requests

def id_extraction(url) -> str:
    """Extract the ID from the URL.

    Keyword arguments:
        url -- the URL to extract the ID from
    """

    # Regex pattern to find the string between "?mid=" and "&usp="
    pattern = r"(?<=\?mid=)([^&]+)(?=&usp=)"

    return  re.search(pattern, url).group(0)


def get_data(url, path) -> None:
    """Get data from the URL and save it to a file.

    Keyword arguments:
        url -- the URL to get data from
        path -- the path to save the data to
        name -- the name of the file
        format -- the format of the file
    """

    # Extract the ID from the URL
    url_id = id_extraction(url)

    # Construct the new URL using the extracted ID
    new_url = f"https://www.google.com/maps/d/kml?mid={url_id}"

    # Send a GET request to the new URL
    response = requests.get(new_url, timeout=10)


    # Check if the response is successful
    if response.status_code != 200:
        raise requests.exceptions.HTTPError(f"Failed to retrieve data: {response.status_code}")

    # Check if the response content is empty
    if not response.content:
        raise ValueError("No content found in the response")

    # Save the response content to a file
    with open(path, "wb") as file:
        file.write(response.content)




def extract(path, extracted_file) -> None:
    """Unzip the downloaded file.

    Keyword arguments:
        path -- the path to the zip file
    """

    # Check if the file exists
    if not os.path.exists(path):
        raise FileNotFoundError(f"The file {path} does not exist")

    # Extract the file
    with ZipFile(path) as file:
        file.extractall(extracted_file)


def compress(path, path_out) -> None:
    """Zip the directory.

    Keyword arguments:
        path -- the path to the directory to zip
        path_out -- the path to save the zipped file
    """

    # Check if the directory exists
    if not os.path.exists(path):
        os.makedirs(path_out, exist_ok=True)


    # Create a zip file
    with ZipFile(path_out, 'w', compression=ZIP_DEFLATED) as new_file:
        for root, _, files in os.walk(path):
            for file in files:
                file_path = os.path.join(root, file)

                # Use arcname to maintain the directory structure inside the KMZ
                arcname = os.path.relpath(file_path, path)
                new_file.write(file_path, arcname=arcname)



def delete(path) -> None:
    """Delete file or directory.

    Keyword arguments:
        path -- the path to the file or directory to delete
    """
    if os.path.isfile(path):
        os.remove(path)
    else:
        shutil.rmtree(path)
