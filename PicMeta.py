from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
import sys
import os
import time

logo = r"""
██████╗ ██╗ ██████╗███╗   ███╗███████╗████████╗ █████╗ 
██╔══██╗██║██╔════╝████╗ ████║██╔════╝╚══██╔══╝██╔══██╗
██████╔╝██║██║     ██╔████╔██║█████╗     ██║   ███████║
██╔═══╝ ██║██║     ██║╚██╔╝██║██╔══╝     ██║   ██╔══██║
██║     ██║╚██████╗██║ ╚═╝ ██║███████╗   ██║   ██║  ██║
╚═╝     ╚═╝ ╚═════╝╚═╝     ╚═╝╚══════╝   ╚═╝   ╚═╝  ╚═╝

        [ 📸 FULL IMAGE METADATA EXTRACTOR 📸 ]
            GPS | EXIF | CAMERA | FILE INFO
                 Create by Rianto Termux
"""

print("memuat...")
time.sleep(2)


def banner():
    os.system("clear" if os.name != "nt" else "cls")
    print(logo)


def convert_to_degrees(value):
    d = float(value[0])
    m = float(value[1])
    s = float(value[2])
    return d + (m / 60.0) + (s / 3600.0)


def input_file():
    print("\033[32mMasukkan lokasi file gambar")
    print("\033[32mContoh: /sdcard/DCIM/Camera/foto.jpg\n")
    return input("\033[32mPath file: ").strip()


def get_file_info(image_path):
    print("\n\033[34m[ 📂 FILE INFO ]")
    print("\033[34m-" * 40)
    print(f"\033[34mNama File     : {os.path.basename(image_path)}")
    print(f"\033[34mLokasi        : {image_path}")
    print(f"\033[34mUkuran File   : {round(os.path.getsize(image_path)/1024, 2)} KB")


def get_image_info(image):
    print("\n\033[36m[ 🖼️ IMAGE INFO ]")
    print("\033[36m-" * 40)
    print(f"\033[36mFormat        : {image.format}")
    print(f"\033[36mMode          : {image.mode}")
    print(f"\033[36mResolusi      : {image.size[0]} x {image.size[1]}")


def get_full_metadata(exif_data):
    print("\n\033[33m[ 📜 FULL EXIF METADATA ]")
    print("-" * 40)

    for tag_id, value in exif_data.items():
        tag = TAGS.get(tag_id, tag_id)

        if tag == "GPSInfo":
            continue

        try:
            print(f"{tag:20}: {value}")
        except:
            print(f"{tag:20}: [Unreadable]")


def get_gps_data(exif):
    gps_data = {}

    for tag_id, val in exif.items():
        tag = TAGS.get(tag_id, tag_id)

        if tag == "GPSInfo":
            for key in val:
                gps_tag = GPSTAGS.get(key, key)
                gps_data[gps_tag] = val[key]

    return gps_data


def show_gps_info(gps_data):
    if not gps_data:
        print("\n[ 📍 GPS INFO ]")
        print("-" * 40)
        print("No GPS data found.")
        return

    try:
        lat = convert_to_degrees(gps_data["GPSLatitude"])
        if gps_data["GPSLatitudeRef"] != "N":
            lat = -lat

        lon = convert_to_degrees(gps_data["GPSLongitude"])
        if gps_data["GPSLongitudeRef"] != "E":
            lon = -lon

        print("\n[ 📍 GPS INFO ]")
        print("-" * 40)
        print(f"Latitude      : {lat}")
        print(f"Longitude     : {lon}")

        if "GPSAltitude" in gps_data:
            print(f"Altitude      : {gps_data['GPSAltitude']} meter")

        if "GPSTimeStamp" in gps_data:
            print(f"GPS Time      : {gps_data['GPSTimeStamp']}")

        print(f"Google Maps   : https://maps.google.com/?q={lat},{lon}")

    except Exception as e:
        print(f"GPS Error: {e}")


def get_gps_coords(image_path):
    try:
        if not os.path.isfile(image_path):
            print("\nFile tidak ditemukan.")
            return

        image = Image.open(image_path)

        get_file_info(image_path)
        get_image_info(image)

        exif = image._getexif()

        if not exif:
            print("\nNo metadata found.")
            return

        time.sleep(1)
        print("\n\033[96mmemuat metadata...")
        time.sleep(2)

        get_full_metadata(exif)

        gps_data = get_gps_data(exif)
        show_gps_info(gps_data)

    except Exception as e:
        print(f"\nError: {e}")


if __name__ == "__main__":
    banner()

    if len(sys.argv) > 1:
        get_gps_coords(sys.argv[1])
    else:
        file_path = input_file()
        if file_path:
            get_gps_coords(file_path)