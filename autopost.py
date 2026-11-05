import argparse
import json
import sys

from core.forms import FIELDS, fill
from core.browser import go

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
    select_category as select_facebook_category,
    select_condition,
    fill_description,
    fill_brand,
    fill_location,
    select_availability,
    publish_facebook,
)
from platforms.carousell import (
    select_category as select_carousell_category,
    inspect_listing_fields,
    fill_listing_basic,
    select_condition as select_carousell_condition,
    fill_brand as fill_carousell_brand,
    select_deal_methods,
    publish_carousell,
    select_size,
)
from platforms.preloved import (
    inspect_preloved_form,
    inspect_preloved_controls,
    fill_preloved_basic,
    select_preloved_category,
    publish_preloved,
    detect_preloved_category,
    select_preloved_size,
    select_preloved_brand,
    select_preloved_condition,
    select_preloved_colors,
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
        "url": "https://preloved.co.id/sell/",
    },
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
# AUTPOST
# ==================================================

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

            # Khusus Preloved: buka halaman jual setelah login
            if key == "pl":
                go(page, "https://preloved.co.id/login")
            else:
                go(page, cfg["url"])

            print("\n=== DATA LISTING ===")
            print(json.dumps(data, indent=4, ensure_ascii=False))

            print("\nURL:", page.url)
            print("Title:", page.title())

            if key == "pl":
                input(
                    "\nLogin ke akun Preloved terlebih dahulu.\n"
                    "Setelah berhasil login dan masuk Dashboard, "
                    "tekan ENTER untuk membuka halaman jual..."
                )
            else:
                input(
                    "\nPastikan akun sudah login, "
                    "selesaikan CAPTCHA/verifikasi jika diminta, "
                    "dan pastikan form jual sudah terbuka. "
                    "Tekan Enter untuk mengisi form..."
                )

            
            result = {}

            # ==========================================
            # FACEBOOK MARKETPLACE
            # ==========================================
            if key == "fb":

                for field in ("title", "price"):
                    result[field] = fill(
                        page,
                        field,
                        data.get(field),
                    )

                result["category"] = select_facebook_category(
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

                if files:
                    result["photos"] = upload_photos(page, files)

                filled = [
                    field for field, success in result.items()
                    if success
                ]

                missing = [
                    field for field, success in result.items()
                    if not success
                ]

                print("\n=== HASIL PENGISIAN FACEBOOK ===")
                print("Berhasil:", filled)
                print("Perlu diisi manual:", missing)

                input(
                    "\nSilakan periksa seluruh data dan foto di Chrome.\n"
                    "Jika sudah benar, tekan ENTER untuk "
                    "melanjutkan Next dan Publish otomatis..."
                )

                publish_facebook(page)

            # ==========================================
            # CAROUSELL
            # ==========================================
            elif key == "cr":

                if files:
                    result["photos"] = upload_photos(page, files)

                select_carousell_category(page)

                basic_results = fill_listing_basic(page, data)

                result["brand"] = fill_carousell_brand(
                    page,
                    data.get("brand")
                )

                result.update({
                    field: True for field in basic_results
                })

                result["condition"] = select_carousell_condition(
                    page,
                    data.get("condition")
                )

                result["size"] = select_size(
                    page,
                    data.get("size")
                )
                
                result["deal_methods"] = select_deal_methods(
                    page,
                    data.get("deal_methods", [])
                )

                filled = [
                    field for field, success in result.items()
                    if success
                ]

                print("\n=== HASIL PENGISIAN CAROUSELL ===")
                print("Berhasil:", filled)

                print(
                    "Dilewati: availability, city "
                    "(tidak tersedia pada form Carousell ini)."
                )

                input(
                    "\nSilakan periksa seluruh data listing di Chrome.\n"
                    "Jika sudah benar, tekan ENTER untuk menekan List now..."
                )

                publish_carousell(page)

            # ==========================================
            # PRELOVED
            # ==========================================

            elif key == "pl":
                print("\n=== NAVIGASI PRELOVED ===")

                # Pastikan halaman Dashboard sudah terbuka setelah login
                print("Halaman saat ini:", page.url)

                # Cari tombol atau link Jual
                jual = page.get_by_role(
                    "link",
                    name="Jual",
                    exact=True
                )

                if jual.count() == 0:
                    jual = page.get_by_role(
                        "button",
                        name="Jual",
                        exact=True
                    )

                if jual.count() == 0:
                    print("Tombol Jual tidak ditemukan.")
                    input("Tekan Enter untuk melanjutkan...")
                    continue

                print("Tombol Jual ditemukan. Mengklik...")

                jual.first.click()
                page.wait_for_timeout(3000)

                print("\n=== HASIL NAVIGASI ===")
                print("URL:", page.url)
                print("Title:", page.title())

                # Isi field dasar
                result = fill_preloved_basic(page, data)

                # Upload foto
                if files:
                    result["photos"] = upload_photos(page, files)

                # Deteksi kategori secara otomatis
                category_path = detect_preloved_category(data)

                if category_path:
                    print("\nKategori terdeteksi:", " > ".join(category_path))

                    result["category"] = select_preloved_category(
                        page,
                        category_path
                    )
                else:
                    result["category"] = False
                    print("Kategori perlu ditentukan secara manual.")

                # Pilih size
                result["size"] = select_preloved_size(
                    page,
                    data.get("size", "")
                )

                # Pilih brand
                result["brand"] = select_preloved_brand(
                    page,
                    data.get("brand", "")
                )

                # Pilih condition
                result["condition"] = select_preloved_condition(
                    page,
                    data.get("condition", "")
                )

                # Pilih warna
                result["colors"] = select_preloved_colors(
                    page,
                    data.get("color", [])
                )

                # Tampilkan hasil pengisian
                filled = [
                    field for field, success in result.items()
                    if success
                ]

                missing = [
                    field for field, success in result.items()
                    if not success
                ]

                print("\n=== HASIL PENGISIAN PRELOVED ===")
                print("Berhasil:", filled)
                print("Perlu diisi manual:", missing)

                # Tunggu konfirmasi pengguna
                input(
                    "\nPeriksa form Preloved di Chrome. "
                    "Tekan Enter untuk menerbitkan produk..."
                )

                # Klik tombol Terbitkan produk
                print("\n=== MENERBITKAN PRODUK ===")
                page.wait_for_timeout(1000)
                publish_button = page.get_by_role(
                    "button",
                    name="Terbitkan produk",
                    exact=True
                )

                if publish_button.count() == 0:
                    print("Tombol Terbitkan produk tidak ditemukan.")

                elif not publish_button.is_enabled():
                    print("Tombol Terbitkan produk belum aktif.")
                    print("Periksa kembali field yang wajib diisi.")

                else:
                    publish_button.click()
                    page.wait_for_timeout(3000)

                    print("Tombol Terbitkan produk berhasil diklik.")
                    print("URL saat ini:", page.url)

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
