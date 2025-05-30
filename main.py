import os
from dotenv import load_dotenv
from src import KMLParser, get_data, extract, delete, compress, ImageCreation

def main():
    """
    Main function to execute the KML data processing workflow.
    This function has following steps:
    1. Load variables from a .env file.
    2. Retrieve the data from URL in KMZ format.
    3. Set up the directory structure.
    5. Extract the KML file from the KMZ archive.
    6. Parse the KML file to extract relevant data.
    7. Generate images based on the parsed data.
    8. Compress the output files into KMZ format.
    9. Clean up temporary files and directories.
    """

    # Load environment variables from .env file
    load_dotenv()
    # Get the environment variables
    url = os.getenv("URL")

    # Use monospace font
    font_url = "https://raw.githubusercontent.com/tsenart/sight/master/fonts/Consolas.ttf"

    current_file = os.path.abspath(__file__)
    root_dir = os.path.dirname(current_file)
    path_out = os.path.join(root_dir, "output")

    os.makedirs(path_out, exist_ok=True)
    path_kmz = os.path.join(path_out, "data.kmz")

    # Initialize the KMLParser
    parser = KMLParser()

    path_data = os.path.join(path_out, "data")

    get_data(url, path_kmz)

    path_data = os.path.join(path_out, "data")
    extract(path_kmz, path_data )

    # Delete the KMZ file after extraction
    delete(path_kmz)

    data_images_path = os.path.join(path_data, "images")
    # Delete the KML images for data correction
    delete(data_images_path)

    path_kml = os.path.join(path_data, "doc.kml")

    parser.parse_data(path_kml, path_out)

    # Remove the KML file after processing
    delete(path_data)

    # Generate new images
    img = ImageCreation(32, font_url, 26)

    for dir_name in os.listdir(path_out):
        dir_path = os.path.join(path_out, dir_name)
        img_dir_path = os.path.join(dir_path, "images")

        os.makedirs(img_dir_path, exist_ok=True)

        img_count = parser.data_count[dir_name]
        color = dir_name.split("-")[1]

        for i in range(img_count):
            img_name = dir_name + "-" + str(i+1).zfill(5)
            img.draw(i+1, img_name, color, img_dir_path)

        # Compress the generated files
        compress(dir_path, os.path.join(path_out, dir_name + ".kmz"))
        # Delete the uncompressed files
        delete(dir_path)

if __name__ == '__main__':
    main()
