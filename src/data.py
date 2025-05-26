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
        self.added_styles = set()


    def strip_namespace(self, tag: str) -> str:
        """Strip the namespace from an XML tag.
        Args:
            tag (str): The XML tag to strip the namespace from.
        Returns:
            str: The tag without the namespace.
        """
        if '}' in tag:
            return tag.split('}', 1)[1]
        return tag


    def process_folder_children(self, original_element, new_folder_element, document, corrected_name, folder_nr) -> ET.Element:
        """Process the children of a Folder element and rename Placemarks.
        Args:
            element (ET.Element): The Folder element to process.
            new_element (ET.Element): The new element to append children to.
            namespace (str): The XML namespace for KML elements.
            number (str): The number associated with the folder for renaming.
        Returns:
            ET.Element: The new element with processed children.
        """
        child_count = 0
        for child in list(original_element):
            if self.strip_namespace(child.tag) == 'Placemark':
                point_elem = child.find('Point')
                coordinates_elem = None
                if point_elem is not None:
                    coordinates_elem = point_elem.find('coordinates')

                new_style_id = f"icon-{folder_nr}-{child_count}"

                new_placemark = ET.Element('Placemark')

                # Add name with non-breaking space
                name_elem = ET.SubElement(new_placemark, 'name')
                name_elem.text = '\u00A0'

                # Add styleUrl
                style_url_elem = ET.SubElement(new_placemark, 'styleUrl')
                style_url_elem.text = f"#{new_style_id}"

                # Add Point and coordinates
                if coordinates_elem is not None:
                    new_point = ET.SubElement(new_placemark, 'Point')
                    new_coords = ET.SubElement(new_point, 'coordinates')
                    new_coords.text = coordinates_elem.text.strip()

                new_folder_element.append(new_placemark)
                child_count += 1

                if new_style_id not in self.added_styles:
                    self.added_styles.add(new_style_id)
                    style_elem = ET.SubElement(document, 'Style', id=new_style_id)
                    icon_style = ET.SubElement(style_elem, 'IconStyle')
                    icon = ET.SubElement(icon_style, 'Icon')
                    href = ET.SubElement(icon, 'href')
                    href.text = f"images/{corrected_name}-{str(child_count).zfill(5)}.png"
            else:
                # Copy non-Placemark elements as is
                new_folder_element.append(child)

        self.data_count[corrected_name] = child_count
        return new_folder_element


    def save_element(self,new_element, output_dir) -> None:
        """Save the new KML element to a file.
        Args:
            new_element (ET.Element): The new KML element to save.
            output_dir (str): The directory where the KML file will be saved.
        """

        file_path = os.path.join(output_dir, "doc.kml")
        # Create the directory if it doesn't exist
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        with open(file_path, 'wb') as file:
            ET.ElementTree(new_element).write(file, encoding='utf-8', xml_declaration=True)


    def process_folder(self, element, output_path) -> None:
        """Process a Folder element and its children, rename Placemarks and save the new structure.
        Args:
            element (ET.Element): The Folder element to process.
            output_path (str): The directory where the new KML file will be saved.
        """

        element_name = element.find('name')
        if element_name is None:
            print("[Warning] Folder without a name found. Skipping.")
            return

        # Extract the element number
        element_number = element_name.text.strip().split(" - ")[0]

        if element_number not in self.data_correction:
            print(f"[Warning] Unknown folder type '{element_number}' found. Skipping.")
            return

        new_kml = ET.Element('kml', xmlns="http://www.opengis.net/kml/2.2")
        document = ET.SubElement(new_kml, 'Document')
        folder = ET.SubElement(document, 'Folder')

        name = self.data_correction[element_number]

        # Renaming new element with our naming convention
        ET.SubElement(folder, 'name').text = name

        folder = self.process_folder_children(element, folder, document, name, element_number)

        output_path = os.path.join(output_path, name)

        # Save the new KML structure to a file
        self.save_element(new_kml, output_path)




    def parse_data(self, file_path, output_path) -> None:
        """Parse the KML file and process its Folder elements.
        Args:
            file_path (str): Path to the KML file to be processed.
            output_path (str): Directory where the processed KML files will be saved.
        """

        # Load the .kml file
        tree = ET.parse(file_path)
        root = tree.getroot()

        # Remove the namespace for easier parsing
        for element in root.iter():
            element.tag = self.strip_namespace(element.tag)

        # Iterate through all the elements to find Folder tags
        for element in root.iter('Folder'):
            self.process_folder(element, output_path)
