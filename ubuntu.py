import os
import subprocess
import csv

# Command to create KML file using Exiftool
exiftool_cmd = ['exiftool', '-E', '-p', 'kml.fmt', 'Images']

# Run the Exiftool command and save the output to a file
with open('test.kml', 'w', encoding='utf-8') as kml_file:
    subprocess.run(exiftool_cmd, stdout=kml_file)

# Command to extract GPS coordinates using Exiftool and output formatted coordinates to a temporary file
extract_coordinates_cmd = ['exiftool', '-T', '-c', '"%.6f"', '-p', '"${Filepath};${GPSLatitude};${GPSLongitude};${GPSAltitude}"', 'Images']

# Run the command to extract GPS coordinates and save them to a temporary text file
with open('temp_coordinates.txt', 'w', encoding='utf-8') as txt_file:
    subprocess.run(extract_coordinates_cmd, stdout=txt_file)

# Read the contents of the temporary text file
with open('temp_coordinates.txt', 'r', encoding='utf-8') as file:
    lines = file.readlines()

# Process each line and remove unnecessary characters
formatted_lines = []
for line in lines:
    parts = line.split(';')
    if len(parts) >= 4:
        filepath = parts[0].strip('"')
        latitude = parts[1].strip(' N"')
        longitude = parts[2].strip(' E"')
        altitude = parts[2].strip(' m Above Sea Level" E')
        formatted_line = f"{filepath};{latitude};{longitude};{altitude}"
        formatted_lines.append(formatted_line)

# Define the headers for each category
headers = ['Filepath', 'Latitude', 'Longitude', 'Altitude']

# Write the formatted lines to a new CSV file with headers
with open('coordinates.csv', 'w', encoding='utf-8', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(headers)
    for line in formatted_lines:
        writer.writerow(line.split(';'))

# Remove the temporary text file
os.remove('temp_coordinates.txt')
