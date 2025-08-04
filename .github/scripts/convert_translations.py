import xml.etree.ElementTree as ET
import re
import os
from datetime import datetime


def xliff_to_po(xliff_file, po_file):
    tree = ET.parse(xliff_file)
    root = tree.getroot()

    ns = {'xliff': 'urn:oasis:names:tc:xliff:document:1.2'}

    translations = []
    for trans_unit in root.findall(".//xliff:trans-unit", ns):
        source_elem = trans_unit.find("xliff:source", ns)
        target_elem = trans_unit.find("xliff:target", ns)

        if source_elem is None:
            continue

        source_text = source_elem.text or ""
        target_text = target_elem.text if target_elem is not None else ""

        source_text = source_text.replace('"', '\\"').replace('\n', '\\n')
        target_text = target_text.replace('"', '\\"').replace('\n', '\\n')

        context_group = trans_unit.find("xliff:context-group", ns)
        if context_group is not None:
            contexts = context_group.findall("xliff:context", ns)
            for context in contexts:
                if context.text:
                    lines = context.text.split("\n")
                    for line in lines:
                        line = re.sub(r'&#13;', '', line)
                        if line.startswith("#. "):
                            msgctxt = line[3:].strip()
                            translations.append((msgctxt, source_text, target_text))

    translations.sort(key=lambda x: x[0])

    revision_date = datetime.now().strftime("%Y-%m-%d %H:%M%z")

    with open(po_file, 'w', encoding='utf-8') as po:
        po.write('msgid ""\n')
        po.write('msgstr ""\n')
        po.write('"Language: ua\\n"\n')
        po.write('"Project-Id-Version: ULP Reborn\\n"\n')
        po.write('"Language-Team: ULP Reborn Team\\n"\n')
        po.write(f'"PO-Revision-Date: {revision_date}\\n"\n')
        po.write('"Content-Type: text/plain; charset=utf-8\\n"\n')
        po.write('"Content-Transfer-Encoding: 8bit\\n"\n')
        po.write('"POT Version: 2.0\\n"\n\n')

        for msgctxt, msgid, msgstr in translations:
            po.write(f"#. {msgctxt}\n")
            po.write(f"msgctxt \"{msgctxt}\"\n")
            po.write(f"msgid \"{msgid}\"\n")
            po.write(f"msgstr \"{msgstr}\"\n\n")


if __name__ == "__main__":
    xliff_to_po("uk/temp.xliff", "ukrainian.po")
