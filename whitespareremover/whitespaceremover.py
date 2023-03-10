from pathlib import Path
import xml.etree.ElementTree as ET

table_import = r'D:\AVID.AARS.54.1\Tables' #sti for tabellen, der skal rettes
table_paths = list(Path(table_import).glob('**/*.xml')) #finder de enkelte tabel-xml-filer i en aflevering

for path in table_paths:
    save_path = path.parent.joinpath(f"new_{path.name}") #til at undgå at tabelfilen bliver overskrevet

    for event, elem in ET.iterparse(path, events=['start-ns']): #finder namespace
        if "www.sa.dk" in elem[1]:
            table_ns = elem[1]

    ns = {'table_ns': table_ns} #namespaceregister

    tree = ET.parse(path) #variabel til indlæsning af tabel
    root = tree.getroot() #tabellens rod

    for col in root.findall('./table_ns:row/', ns): #fjerner whitespace fra strings
        if isinstance(col.text, str):
            col.text = col.text.strip()

    tree.write(path, encoding="UTF-8", xml_declaration=True, default_namespace=table_ns, method="xml") #overskriver tabelfilerne - husk at bruge save_path, hvis filen ikke skal overskrives

#print(ET.tostring(root, encoding='UTF-8', method="xml").decode('UTF-8')) #ikke vigtig, men kan vise, om xml-filen er indlæst korrekt.
