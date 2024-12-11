import geopandas as gpd
import pandas as pd
from shapely.geometry import Point, shape, MultiLineString
from shapely import wkt

def csv_to_geojson(input_csv, output_geojson, lat_col=None, lon_col=None, geometry_col=None):
    """
    Convert a CSV file to a GeoJSON file using GeoPandas.

    Parameters:
        input_csv (str): Path to the input CSV file.
        output_geojson (str): Path to the output GeoJSON file.
        lat_col (str, optional): Name of the column containing latitude values (used for Point geometries).
        lon_col (str, optional): Name of the column containing longitude values (used for Point geometries).
        geometry_col (str, optional): Name of the column containing WKT, GeoJSON, or multiline string geometries.
    """
    # Load the CSV data into a pandas DataFrame
    df = pd.read_csv(input_csv)

    if geometry_col:
        # Check if the geometry column exists
        if geometry_col not in df.columns:
            raise ValueError(f"Column '{geometry_col}' not found in the CSV file.")

        # Convert the geometry column to shapely geometries
        def parse_geometry(geom):
            if isinstance(geom, str):
                try:
                    # Attempt to parse as WKT directly
                    return wkt.loads(geom)
                except Exception as e:
                    raise ValueError(f"Invalid WKT geometry format: {geom}") from e
            return geom

        df['geometry'] = df[geometry_col].apply(parse_geometry)
        gdf = gpd.GeoDataFrame(df, geometry='geometry')
    elif lat_col and lon_col:
        # Check if the latitude and longitude columns exist
        if lat_col not in df.columns or lon_col not in df.columns:
            raise ValueError(f"Columns '{lat_col}' and/or '{lon_col}' not found in the CSV file.")

        # Create a GeoDataFrame with Point geometry
        geometry = [Point(xy) for xy in zip(df[lon_col], df[lat_col])]
        gdf = gpd.GeoDataFrame(df, geometry=geometry)
    else:
        raise ValueError("Either 'geometry_col' or both 'lat_col' and 'lon_col' must be provided.")

    # Set the CRS (Coordinate Reference System) to WGS84 (EPSG:4326)
    gdf.set_crs(epsg=4326, inplace=True)

    # Export to GeoJSON
    gdf.to_file(output_geojson, driver='GeoJSON')
    print(f"GeoJSON file has been saved to {output_geojson}")

# Example usage
# csv_to_geojson('dataset/commodity/gold_mines_and_mineral_deposits.csv', 'output.geojson', lat_col='latitude', lon_col='longitude')
csv_to_geojson('dataset/commodity_relevant_data/mineral_resource_potential.csv', 'dataset/commodity_relevant_data/mineral_resource_potential.geojson', geometry_col='geometry')
