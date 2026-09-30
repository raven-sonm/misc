# 🤖 DISCLAIMER: This code was output from CoPilot AI during a use case of trying to render a map in plotly
# This code is retained and uploaded for tracking purposes

import csv
import json
import sys
import os

def csv_to_geojson(csv_file_path, geojson_file_path, lat_field='lat', lon_field='lng'):
    """
    Convert a CSV file to a GeoJSON file.
    
    :param csv_file_path: Path to the input CSV file
    :param geojson_file_path: Path to the output GeoJSON file
    :param lat_field: Name of the latitude column in CSV
    :param lon_field: Name of the longitude column in CSV
    """
    features = []

    try:
        with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            # Normalize field names to lowercase for matching
            fieldnames = {name.lower(): name for name in reader.fieldnames}

            if lat_field.lower() not in fieldnames or lon_field.lower() not in fieldnames:
                raise ValueError(f"CSV must contain '{lat_field}' and '{lon_field}' columns.")

            for row in reader:
                try:
                    lat = float(row[fieldnames[lat_field.lower()]])
                    lng = float(row[fieldnames[lon_field.lower()]])
                except (ValueError, KeyError):
                    # Skip rows with invalid coordinates
                    continue

                # Create a GeoJSON feature
                feature = {
                    "type": "Feature",
                    "geometry": {
                        "type": "Polygon",
                        "coordinates": [lng, lat]
                    },
                    "properties": {k: v for k, v in row.items() if k not in (fieldnames[lat_field.lower()], fieldnames[lon_field.lower()])}
                }
                features.append(feature)

        # Create the GeoJSON structure
        geojson = {
            "type": "FeatureCollection",
            "features": features
        }

        # Write to file
        with open(geojson_file_path, 'w', encoding='utf-8') as geojsonfile:
            json.dump(geojson, geojsonfile, indent=4)

        print(f"✅ Successfully converted '{csv_file_path}' to '{geojson_file_path}'.")

    except FileNotFoundError:
        print(f"❌ Error: File '{csv_file_path}' not found.")
    except Exception as e:
        print(f"❌ Error: {e}")

# Example usage:
if __name__ == "__main__":
    # You can replace these with your own file paths
    input_csv = "data/Spreadsheet List of All counties in New Mexico export.csv"
    output_geojson = "TEST_GEO.geojson"

    # Optional: allow command-line arguments
    if len(sys.argv) >= 3:
        input_csv = sys.argv[1]
        output_geojson = sys.argv[2]

    csv_to_geojson(input_csv, output_geojson)
