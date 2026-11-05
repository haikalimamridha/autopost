
import re


FIELDS = {
    "title": r"judul|title|nama",
    "price": r"harga|price",
    "description": r"deskripsi|description",
    "brand": r"brand|merk|merek",
    "category": r"kategori|category",
    "availability": r"ketersediaan|availability|stok|stock",
    "city": r"lokasi|location|kota",
}


def fill(page, key, value):
    if value is None or value == "":
        return False

    pattern = re.compile(FIELDS[key], re.I)

    locators = [
        page.get_by_label(pattern),
        page.get_by_placeholder(pattern),
        page.get_by_role("textbox", name=pattern),
    ]

    for locator in locators:
        try:
            if locator.count() > 0:
                locator.first.fill(str(value), timeout=3000)
                return True

        except Exception:
            continue

    return False
