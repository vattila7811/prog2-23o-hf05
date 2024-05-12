import json
import os

ALBUMPATH = "Albums"


def load_album(band: str, album: str) -> dict:
    data = {}
    try:
        with open(os.path.join(ALBUMPATH, band, album), "r", encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError:
        pass
    except FileNotFoundError:
        pass
    return data


def load_data()-> dict:
    data = {}
    bands = {entry.name for entry in os.scandir(ALBUMPATH) if entry.is_dir()}
    for band in bands:
        albums = {entry.name for entry in os.scandir(os.path.join(ALBUMPATH, band)) if entry.is_file()}
        for album in albums:
            albumdata = load_album(band, album)
            if albumdata != {}:
                if band not in data.keys(): data[band] = {}
                data[band][album.replace('.json', '')] = albumdata
    return data


def collect_names(data: dict[str, dict]) -> set[str]:
    names = set()
    for albums in data.values():
        for albumdata in albums.values():
            try:
                personnel = albumdata["personnel"]
                for person in personnel:
                    names.add(person)
            except KeyError:
                pass
    return names
