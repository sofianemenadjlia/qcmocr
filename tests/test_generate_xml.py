import unittest
import xml.etree.ElementTree as ET
import xml.dom.minidom


STUDENT_NUMBER_LENGTH = 8

expected_xml_str = '''<?xml version="1.0" ?>
<root>
	<liste_key>no</liste_key>
	<notes_id>0</notes_id>
	<copie>
		<student1>
			<id>29</id>
			<num>22118393</num>
			<confidence>87.5</confidence>
		</student1>
		<student2>
			<id>16</id>
			<num>22002907</num>
			<confidence>100.0</confidence>
		</student2>
		<student3>
			<id>31</id>
			<num>22002097</num>
			<confidence>100.0</confidence>
		</student3>
		<student4>
			<id>30</id>
			<num>22326648</num>
			<confidence>100.0</confidence>
		</student4>
		<student5>
			<id>15</id>
			<num>21724494</num>
			<confidence>75.0</confidence>
		</student5>
		<student6>
			<id>1</id>
			<num>22207890</num>
			<confidence>87.5</confidence>
		</student6>
		<student7>
			<id>28</id>
			<num>21907419</num>
			<confidence>100.0</confidence>
		</student7>
		<student8>
			<id>26</id>
			<num>22302085</num>
			<confidence>100.0</confidence>
		</student8>
		<student9>
			<id>17</id>
			<num>21919437</num>
			<confidence>87.5</confidence>
		</student9>
	</copie>
</root>'''

def generate_xml(matches, xml_folder):
    root = ET.Element("root")
    liste_key = ET.SubElement(root, "liste_key")
    liste_key.text = "no"
    notes_id = ET.SubElement(root, "notes_id")
    notes_id.text = "0"

    copie = ET.SubElement(root, "copie")
    for i, match in enumerate(matches, start=0):

        if i == len(matches):
            break
        
        student = ET.SubElement(copie, f"student{i+1}")
        student_id = ET.SubElement(student, "id")
        student_id.text = match[3]

        num = ET.SubElement(student, "num")
        num.text = match[1]
        resemblance = ET.SubElement(student, "confidence")
        resemblance.text = str(100 - (match[2] * 100 / STUDENT_NUMBER_LENGTH))

    xml_str = xml.dom.minidom.parseString(ET.tostring(root)).toprettyxml()

    with open(xml_folder, "w") as file:
        file.write(xml_str)

class TestGenerateXML(unittest.TestCase):
    def test_generate_xml(self):
        # Define sample matches
        matches = [
            ('22118393', '22118393', 1, '29'),
            ('22002907', '22002907', 0, '16'),
            ('22002097', '22002097', 0, '31'),
            ('22326648', '22326648', 0, '30'),
            ('21726894', '21724494', 2, '15'),
            ('22207830', '22207890', 1, '1'),
            ('21907419', '21907419', 0, '28'),
            ('22302085', '22302085', 0, '26'),
            ('21919937', '21919437', 1, '17')
        ]

        # Convert the expected XML string to a parsed ElementTree
        expected_xml_tree = ET.fromstring(expected_xml_str)

        # Create a temporary file to write the generated XML
        temp_xml_file = "temp.xml"

        # Call the generate_xml function
        generate_xml(matches, temp_xml_file)

        # Parse the generated XML
        generated_xml_tree = ET.parse(temp_xml_file)

        # Assert that the generated XML matches the expected XML
        self.assertEqual(ET.tostring(generated_xml_tree.getroot()), ET.tostring(expected_xml_tree))

if __name__ == '__main__':
    unittest.main()
