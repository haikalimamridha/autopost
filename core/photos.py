
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent


def get_photos(photo_folder):
    if not photo_folder:
        print("Folder foto tidak ditentukan.")
        return []

    folder = Path(photo_folder)

    if not folder.is_absolute():
        folder = BASE_DIR / folder

    if not folder.exists() or not folder.is_dir():
        print(f"Folder foto tidak ditemukan: {folder}")
        return []

    extensions = {".jpg", ".jpeg", ".png", ".webp"}

    photos = sorted(
        str(file.resolve())
        for file in folder.rglob("*")
        if file.is_file() and file.suffix.lower() in extensions
    )

    print(f"\nDitemukan {len(photos)} foto:")

    for photo in photos:
        print(f"- {photo}")

    return photos


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
