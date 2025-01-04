import xml.etree.ElementTree as ET
import re
import os

def xliff_to_po(xliff_file, po_file):
    tree = ET.parse(xliff_file)
    root = tree.getroot()

    # Namespace handling
    ns = {'xliff': 'urn:oasis:names:tc:xliff:document:1.2'}

    # Parse translations
    translations = []
    for trans_unit in root.findall(".//xliff:trans-unit", ns):
        source_text = trans_unit.find("xliff:source", ns).text
        target_text = trans_unit.find("xliff:target", ns).text

        # Handle None target_text
        if target_text is None:
            target_text = ""

        # Escape double quotes
        source_text = source_text.replace('"', '\\"')
        target_text = target_text.replace('"', '\\"')

        # Replace newline characters with \n
        source_text = source_text.replace('\n', '\\n')
        target_text = target_text.replace('\n', '\\n')

        # Extract contexts
        context_group = trans_unit.find("xliff:context-group", ns)
        if context_group is not None:
            contexts = context_group.findall("xliff:context", ns)
            for context in contexts:
                if context.text:
                    lines = context.text.split("\n")
                    for line in lines:
                        line = re.sub(r'&#13;', '', line)  # Remove XML encoded line breaks
                        if line.startswith("#. "):
                            msgctxt = line[3:].strip()
                            translations.append((msgctxt, source_text, target_text))

    # Sort translations by msgctxt
    translations.sort(key=lambda x: x[0])

    # Write to .po file
    with open(po_file, 'w', encoding='utf-8') as po:
        for msgctxt, msgid, msgstr in translations:
            po.write(f"#. {msgctxt}\n")
            po.write(f"msgctxt \"{msgctxt}\"\n")
            po.write(f"msgid \"{msgid}\"\n")
            po.write(f"msgstr \"{msgstr}\"\n\n")
    
    # Remove temp file
    os.remove(xliff_file)

xliff_to_po("uk/temp.xliff", "ukrainian.po")

