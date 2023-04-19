import xml.etree.ElementTree as ET
from pathlib import Path

# Load the XML file with the namespace map
xml_path = Path(r'D:\test\tableIndex.xml')
ET.register_namespace('',"http://www.sa.dk/xmlns/diark/1.0")
tree = ET.parse(xml_path)
root = tree.getroot()

# Define the list of conditions
conditions = [
    {"name": "DokBeskrivelse", "functionalDescription": "Dokumenttitel"},
    {"name": "DokDato", "functionalDescription": "Dokumentdato"},
    {"name": "SagsTitel", "functionalDescription": "Sagstitel"},
    {"name": "SagsNr", "functionalDescription": "Sagsidentifikation"},
    {"name": "CICSSAGSNR", "functionalDescription": "Sagsidentifikation"},
    {"name": "DAOSSagsnr", "functionalDescription": "Sagsidentifikation"}
]

# Find the columns that match the conditions and add the functionalDescription tag
for column in root.findall('.//{*}column'):
    if column.find('{*}name') is not None:
        name = column.find('{*}name')
    for cond in conditions:
        if (name.text == cond["name"] and not column.findall("{*}functionalDescription")):
            new_tag = ET.SubElement(column, "functionalDescription")
            new_tag.text = cond["functionalDescription"]

    # Save the modified XML file
    save_path = xml_path.parent.joinpath(f"new_{xml_path.name}")
    tree.write(save_path, encoding="UTF-8", xml_declaration=True, method="xml")
