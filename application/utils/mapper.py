import gmaps
import gmaps.datasets

gmaps.configure(api_key="AIzaSyCV7H6JuYtk0sh8EE8bn4Czh9aTRdmQLiQ")


def draw(dataframe):
    

    locations = dataframe[["latitude", "longitude"]]
    weights = dataframe["i alt"]

    fig = gmaps.figure()
    fig.add_layer(gmaps.heatmap_layer(locations, weights=weights))

    return fig
