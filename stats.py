import matplotlib.pyplot as plt
from matplotlib.axes import Axes
import db

def albums_per_year(data: dict[str, dict]):
    statistics = {}
    for albums in data.values():
        for albumdata in albums.values():
            try:
                year = int(albumdata["year"])
                count = statistics.get(year, 0)
                count += 1
                statistics[year] = count
            except KeyError:
                pass
            except TypeError:
                pass
    statistics = sorted([(year, count) for year, count in statistics.items()])
    plt.plot([year for year, _ in statistics], [count for _, count in statistics], marker='o')
    plt.show()


def frequent_names(data: dict[str, dict]):
    names = db.collect_names(data)
    first_names = {}
    for name in names:
        first_name = name.split()[0]
        count = first_names.get(first_name, 0)
        count += 1
        first_names[first_name] = count
    first_names = sorted([(am, fn) for fn, am in first_names.items() if am >=10])
    plt.suptitle("Most common names in rock bands")
    plt.barh( [am for _, am in first_names], [fn for fn, _ in first_names])
    plt.show()


BAND_THRESHOLD = 8
ALBUM_THRESHOLD = 16
def size_occurance(data: dict[str, dict], keyname: str, threshold: int) -> list[tuple[int, int]]:
    occurances = {}
    for albums in data.values():
        for album in albums.values():
            try: 
                size = len(album[keyname])
                if size > 0:
                    if size > threshold: size = threshold
                    count = occurances.get(size, 0) + 1
                    occurances[size] = count
            except KeyError:
                pass    
    return sorted([(size, count) for size, count in occurances.items()])


def band_album_sizes(data: dict[str, dict]):
    band_sizes = size_occurance(data, "personnel", BAND_THRESHOLD)
    album_sizes = size_occurance(data, "tracks", ALBUM_THRESHOLD)

    fig, axs = plt.subplots(1, 2, figsize=(10,5))
    ax0 : Axes = axs[0]
    ax1 : Axes = axs[1]
    ax0.pie([count for _, count in band_sizes], labels=[str(size) if size < BAND_THRESHOLD else f"{BAND_THRESHOLD}+" for size, _ in band_sizes])
    ax0.set_title("Band sizes")
    ax1.pie([count for _, count in album_sizes], labels=[str(size) if size < ALBUM_THRESHOLD else f"{ALBUM_THRESHOLD}+" for size, _ in album_sizes])
    ax1.set_title("Album sizes")
    plt.show()


def band_release_years(data: dict[str, dict]) -> dict[str, list[int]]:
    releases = {}
    for band, albums in data.items():
        for album in albums.values():
            year = album["year"]
            years = list(releases.get(band, []))
            years.append(year)
            releases[band] = years
    return releases


def productive_bands(data: dict[str, dict]):
    releases = band_release_years(data)
    release_counts = sorted([(band, years) for band, years in releases.items() if len(years) >=5 ], key=lambda x: x[0].casefold())
    
    
    plt.figure(figsize=(10,6))
    plt.barh([band for band, _ in release_counts], [len(years) for _, years in release_counts] )
    plt.title("Number of released albums by bands".title())
    plt.tight_layout(pad=2)
    plt.show()

    plt.figure(figsize=(10,6))
    release_scatter = [(band, year) for band, years in release_counts for year in years]
    plt.scatter([year for _, year in release_scatter], [band for band, _ in release_scatter], marker="s", color="black")
    plt.title("Album releases by band by year".title())
    plt.tight_layout(pad=2)
    plt.show()

    

