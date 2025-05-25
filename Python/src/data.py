import os
import xml.etree.ElementTree as ET


class KMLParser:
    """Class to parse KML files and extract specific data.

    This class reads KML files, extracts relevant information, and saves it in a new format.
    It focuses on processing Folder elements within the KML structure.

    Attributes:
        file_path (str): Path to the KML file to be processed.
        namespace (str): XML namespace for KML elements.
    """

    def __init__(self):
        self.namespace = '{http://www.opengis.net/kml/2.2}'
        self.path = os.getcwd()
        self.data_count = {
            "0-red": 0,
            "1-white": 0,
            "2-blue": 0,
            "3-green": 0,
            "4-yellow": 0,
        }
        self.data_correction = {
            "0": "0-red",
            "1": "2-blue",
            "2": "3-green",
            "3": "4-yellow",
            "4": "1-white",
        }



    def process_folder_children(self, element, new_element, namespace, number) -> ET.Element:
        """Process the children of a Folder element and rename Placemarks.
        Args:
            element (ET.Element): The Folder element to process.
            new_element (ET.Element): The new element to append children to.
            namespace (str): The XML namespace for KML elements.
            number (str): The number associated with the folder for renaming.
        Returns:
            ET.Element: The new element with processed children.
        """
        child_count = -1
        for child in element:
            child_count += 1
            if child.tag == f"{namespace}Placemark" and child.find(f"{namespace}name") is not None:
                child.find(f"{namespace}name").text = self.data_correction[number] + "-" + str(child_count).zfill(5)

            # Append the modified (or unmodified) child to the new element
            new_element.append(child)

        self.data_count[self.data_correction[number]] = child_count

        return new_element


    def save_element(self,new_element, output_dir) -> None:
        """Save the new KML element to a file.
        Args:
            new_element (ET.Element): The new KML element to save.
            output_dir (str): The directory where the KML file will be saved.
        """

        file_path = os.path.join(output_dir, os.path.basename(output_dir) + ".kml")
        # Create the directory if it doesn't exist
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        with open(file_path, 'wb') as file:
            ET.ElementTree(new_element).write(file, encoding='utf-8', xml_declaration=True)


    def process_folder(self, element, output_path) -> None:
        """Process a Folder element and its children, renaming Placemarks and saving the new structure.
        Args:
            element (ET.Element): The Folder element to process.
            output_path (str): The directory where the new KML file will be saved.
        """

        # Create a new KML structure
        new_element = ET.Element('kml', xmlns=self.namespace)
        # Add a Document tag to the new KML
        document = ET.SubElement(new_element, 'Document')
        folder = ET.SubElement(document, 'Folder')

        # Extract the element number
        nr = element.find(f'{self.namespace}name').text.strip().split(" - ")[0]

        if nr in self.data_correction:
            # Renaming new element with our naming convention
            ET.SubElement(folder, f'{self.namespace}name').text = self.data_correction[nr]

            folder = self.process_folder_children(element, folder, self.namespace, nr)

            output_path = os.path.join(output_path, self.data_correction[nr])

            # Save the new KML structure to a file
            self.save_element(new_element, output_path)
        # If the folder type is not recognized, raise a warning
        else:
            print(f"[Warning] Unknown folder type '{nr}' found. Skipping.")




    def parse_data(self, file_path, output_path) -> None:
        """Parse the KML file and process its Folder elements.
        Args:
            file_path (str): Path to the KML file to be processed.
            output_path (str): Directory where the processed KML files will be saved.
        """

        # Load the .kml file
        tree = ET.parse(file_path)
        root = tree.getroot()

        # Iterate through all the elements to find Folder tags
        for element in root.iter():
            # Layers are represented with Folder tag
            if element.tag.endswith('Folder') and element.find(f"{self.namespace}name") is not None:
                self.process_folder(element, output_path)
