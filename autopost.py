import argparse
import json
import re
from pathlib import Path

from core.chrome import (
    PROFILE,
    PORT,
    start_chrome,
    wait_port,
)

from core.listing import load_listing

from core.photos import (
    get_photos,
    upload_photos,
)

from platforms.facebook import (
    select_category,
    select_condition,
    fill_description,
    fill_brand,
    fill_location,
    select_availability,
    publish_facebook,
)

from platforms.facebook import (
    select_category,
    select_condition,
    fill_description,
    fill_brand,
    fill_location,
    select_availability,
    publish_facebook,
)

from playwright.sync_api import sync_playwright


# ==================================================
# KONFIGURASI
# ==================================================

PLATFORMS = {
    "fb": {
        "name": "Facebook Marketplace",
        "url": "https://www.facebook.com/marketplace/create/item",
    },
    "cr": {
        "name": "Carousell",
        "url": "https://www.carousell.co.id/sell/",
    },
    "pl": {
        "name": "Preloved",
        "url": "https://preloved.co.id/sell",
    },
}

FIELDS = {
    "title": r"judul|title|nama",
    "price": r"harga|price",
    "description": r"deskripsi|description",
    "brand": r"brand|merk|merek",
    "category": r"kategori|category",
    "availability": r"ketersediaan|availability|stok|stock",
    "city": r"lokasi|location|kota",
}

# ==================================================
# LOGIN MANUAL
# ==================================================

def login():
    urls = [cfg["url"] for cfg in PLATFORMS.values()]

    print("\nMembuka Google Chrome dengan profil khusus autopost...")
    print("Lokasi profil:", PROFILE)

    start_chrome(urls=urls, debug=False)

    print("\nChrome sudah dibuka.")
    print("Silakan login secara manual:")
    print("1. Facebook Marketplace")
    print("2. Carousell")
    print("3. Preloved")
    print("\nSelesaikan CAPTCHA atau verifikasi jika diminta.")
    print("Untuk Preloved, gunakan login email jika tersedia.")

    input(
        "\nJika semua akun sudah berhasil login, "
        "tutup SEMUA jendela Chrome tersebut. "
        "Setelah Chrome tertutup, tekan Enter di terminal..."
    )

    print("\nProses login selesai.")
    print("Sesi disimpan pada:", PROFILE)


# ==================================================
# NAVIGASI
# ==================================================

def go(page, url):
    try:
        page.goto(
            url,
            wait_until="domcontentloaded",
            timeout=120000,
        )
    except Exception as e:
        print(
            f"Peringatan: halaman belum selesai dimuat "
            f"({type(e).__name__})."
        )


# ==================================================
# ISI FORM
# ==================================================

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

def upload_photos(page, files):
    if not files:
        print("Tidak ada foto untuk diunggah.")
        return False

    try:
        locator = page.locator('input[type="file"]')

        if locator.count() == 0:
            print("Input file tidak ditemukan.")
            return False

        locator.first.set_input_files(
            files,
            timeout=10000
        )

        print(f"{len(files)} foto berhasil dimasukkan.")
        return True

    except Exception as e:
        print("Upload foto gagal:", e)
        return False

# ==================================================
# AUTPOST
# ==================================================


def inspect_form(page):
    print("\n=== PEMERIKSAAN ELEMEN FORM ===")

    elements = page.locator(
        'input, textarea, '
        '[contenteditable="true"], '
        '[role="textbox"], '
        '[role="combobox"]'
    )

    for i in range(elements.count()):
        el = elements.nth(i)

        try:
            info = el.evaluate("""
                el => ({
                    tag: el.tagName,
                    type: el.getAttribute('type'),
                    role: el.getAttribute('role'),
                    placeholder: el.getAttribute('placeholder'),
                    ariaLabel: el.getAttribute('aria-label'),
                    contenteditable: el.getAttribute('contenteditable'),
                    text: el.innerText,
                    outerHTML: el.outerHTML.substring(0, 400)
                })
            """)

            print(f"\\nElement {i}:")
            print(info)

        except Exception:
            continue

def run(listing, keys):
    data = load_listing(listing)
    files = get_photos(data.get("photos"))

    print("\nMembuka Chrome dengan remote debugging...")
    print("Pastikan semua jendela Chrome dengan profil autopost sudah ditutup.")

    start_chrome(debug=True)

    if not wait_port():
        sys.exit(
            "Chrome tidak membuka port debugging.\n"
            "Pastikan semua jendela Chrome dengan profil autopost "
            "sudah ditutup sebelum menjalankan skrip."
        )

    with sync_playwright() as pw:

        browser = pw.chromium.connect_over_cdp(
            f"http://127.0.0.1:{PORT}"
        )

        if not browser.contexts:
            sys.exit("Profil Chrome tidak ditemukan.")

        context = browser.contexts[0]

        for key in keys:

            key = key.strip().lower()

            if key not in PLATFORMS:
                print(f"Platform tidak dikenal: {key}")
                continue

            cfg = PLATFORMS[key]

            print("\n" + "=" * 45)
            print(cfg["name"])
            print("=" * 45)

            page = context.new_page()

            go(page, cfg["url"])

            print("\n=== DATA LISTING ===")
            print(json.dumps(data, indent=4, ensure_ascii=False))

            print("\nURL:", page.url)
            print("Title:", page.title())

            input(
                "\nPastikan akun sudah login, "
                "selesaikan CAPTCHA/verifikasi jika diminta, "
                "dan pastikan form jual sudah terbuka. "
                "Tekan Enter untuk mengisi form..."
            )

            result = {}

            # Facebook: kategori dipilih melalui dropdown,
            # bukan diisi menggunakan fungsi fill().
            if key == "fb":

                for field in (
                    "title",
                    "price",
                ):
                    result[field] = fill(
                        page,
                        field,
                        data.get(field),
                    )

                result["category"] = select_category(
                    page,
                    data.get("category")
                )

                result["condition"] = select_condition(
                    page,
                    data.get("condition")
                )

                result["description"] = fill_description(
                    page,
                    data.get("description")
                )

                result["brand"] = fill_brand(
                    page,
                    data.get("brand")
                )

                result["availability"] = select_availability(
                    page,
                    data.get("availability")
                )

                result["city"] = fill_location(
                    page,
                    data.get("city")
                )

            # Platform selain Facebook menggunakan pengisian umum.
            else:

                for field in FIELDS:
                    result[field] = fill(
                        page,
                        field,
                        data.get(field),
                    )

            # Upload foto jika tersedia.
            if files:
                result["photos"] = upload_photos(page, files)

            filled = [
                field
                for field, success in result.items()
                if success
            ]

            missing = [
                field
                for field, success in result.items()
                if not success
            ]

            print("\n=== HASIL PENGISIAN ===")
            print("Berhasil:", filled)
            print("Perlu diisi manual:", missing)

            if key == "fb":

                input(
                    "\nSilakan periksa seluruh data dan foto di Chrome.\n"
                    "Jika sudah benar, tekan ENTER untuk "
                    "melanjutkan Next dan Publish otomatis..."
                )

                publish_facebook(page)

            else:

                input(
                    "\nSilakan periksa listing di Chrome. "
                    "Setelah selesai, tekan Enter untuk melanjutkan..."
                )

        print("\nSemua platform selesai diproses.")
        print("Chrome tetap dibiarkan terbuka.")

# ==================================================
# MAIN
# ==================================================

if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description="Autopost Marketplace"
    )

    parser.add_argument("listing", nargs="?")
    parser.add_argument("--login", action="store_true")
    parser.add_argument(
        "--platforms",
        default="fb,cr,pl",
    )

    args = parser.parse_args()

    if args.login:
        login()

    elif args.listing:
        run(
            args.listing,
            args.platforms.split(","),
        )

    else:
        parser.print_help()
