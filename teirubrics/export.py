from pathlib import Path
import re
from jinja2 import Environment, FileSystemLoader

from .tei import find_element, extract_text


def convert_roman_prefix(s):
    match = re.match(r"^(I+)([A-Z][a-z]+.*)", s)
    if match:
        roman, rest = match.groups()
        return str(len(roman)) + rest
    return s


def add_space_after_book(s):
    return re.sub(r"^([1-3]?[A-Za-z]+)(\d+:\d+b?)$", r"\1 \2", s)


def export_data(
    data, 
    key_name, 
    sigla, output_path:Path, 
    display_verse:bool=True, 
    display_folio:bool=True,
    display_facs:bool=True,
    title:str="",
):
    templates = Path(__file__).parent / "templates"
    env = Environment(loader=FileSystemLoader(templates))
    rubric_template = env.get_template('rubric.html')

    rows = []
    for key in data:
        row = [key]
        for siglum in sigla:
            if siglum in data[key]:
                items = []
                for element in data[key][siglum]:
                    head = find_element(element, ".//head")
                    if head is None:
                        continue
                    orig = find_element(head, ".//orig")
                    original_text = extract_text(orig)
                    translation_element = find_element(head, ".//reg[@type='translation']")
                    translation = extract_text(translation_element) if translation_element is not None else ""
                    translation = translation.replace(" .", ".")

                    anchor = find_element(element, ".//anchor")
                    facs = anchor.attrib.get("facs", "") if anchor is not None else ""
                    source = anchor.attrib.get("source", "") if anchor is not None else ""
                    if source.startswith("#"):
                        source = source[1:]
                    folio = anchor.attrib.get("n", "") if anchor is not None else ""

                    verse = element.attrib.get("corresp", "")
                    # change roman numerals to arabic at the start
                    verse = convert_roman_prefix(verse)
                    verse = add_space_after_book(verse)


                    item = rubric_template.render(
                        original_text=original_text,
                        translation=translation,
                        verse = verse if display_verse else "",
                        facs=facs if display_folio and display_facs else "",
                        source=source if display_folio else "",
                        folio=folio if display_folio else "",
                    )
                    items.append(item)
                cell = "<hr>\n".join(items)
            else:
                cell = ""
            row.append(cell)
        rows.append(row)

    table = env.get_template('table.html').render(
        rows=rows,
        headers=[key_name] + sigla,
    )
    page = env.get_template('page.html').render(
        title=title,
        content=table,
    )
    print("Exporting to", output_path)
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w") as f:
        f.write(page)    