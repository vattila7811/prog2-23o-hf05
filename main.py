import db
import stats

def main():
    data = db.load_data()
    print("data loaded")
    #stats.albums_per_year(data)
    #stats.frequent_names(data)
    #stats.band_album_sizes(data)
    stats.productive_bands(data)

main()