import geopandas as gpd
import pandas as pd
from shapely.geometry import Point

def csv_to_geojson(input_csv, output_geojson, lat_col='Latitude', lon_col='Longitude'):
    """
    Convert a CSV file to a GeoJSON file using GeoPandas.

    Parameters:
        input_csv (str): Path to the input CSV file.
        output_geojson (str): Path to the output GeoJSON file.
        lat_col (str): Name of the column containing latitude values.
        lon_col (str): Name of the column containing longitude values.
    """
    # Load the CSV data into a pandas DataFrame
    df = pd.read_csv(input_csv)

    # Check if the latitude and longitude columns exist
    if lat_col not in df.columns or lon_col not in df.columns:
        raise ValueError(f"Columns '{lat_col}' and/or '{lon_col}' not found in the CSV file.")

    # Create a GeoDataFrame with Point geometry
    geometry = [Point(xy) for xy in zip(df[lon_col], df[lat_col])]
    gdf = gpd.GeoDataFrame(df, geometry=geometry)

    # Set the CRS (Coordinate Reference System) to WGS84 (EPSG:4326)
    gdf.set_crs(epsg=4326, inplace=True)

    # Export to GeoJSON
    gdf.to_file(output_geojson, driver='GeoJSON')
    print(f"GeoJSON file has been saved to {output_geojson}")

# Example usage
csv_to_geojson('dataset/commodity_relevant_data/all_mines_and_mineral_deposits.csv', 'dataset/commodity_relevant_data/all_mines_and_mineral_deposits.geojson')
