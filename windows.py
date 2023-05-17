import os
import subprocess

# Get the current working directory
current_directory = os.getcwd()

# Change directory command
change_directory_cmd = f'cd /d {current_directory}'

# Run the change directory command
subprocess.run(change_directory_cmd, shell=True)

# Command to create KML file using Exiftool
exiftool_cmd = 'exiftool -E -p kml.fmt Images > test.kml'

# Run the Exiftool command to create the KML file
subprocess.run(exiftool_cmd, shell=True)

# Command to extract GPS coordinates using Exiftool and output formatted coordinates to a CSV file
extract_coordinates_cmd = 'exiftool -T -c "%.6f" -p "${Filepath};${GPSLatitude};${GPSLongitude};${GPSAltitude}" Images > coordinates.csv'

# Run the command to extract GPS coordinates and save them to a CSV file
subprocess.run(extract_coordinates_cmd, shell=True)

# Read the contents of the CSV file
with open('coordinates.txt', 'r',encoding='utf-8') as file:
    lines = file.readlines()

# Process the header line
header = 'Failinimi(Kaustateega);Laiuskraad;Pikkuskraad;Kõrgus'


# Process each line and remove 'N' from Latitude and 'E' from Longitude
for i in range(1, len(lines)):
    parts = lines[i].split(';')
    filename = parts[0]
    latitude = parts[1].replace(' N', '')
    longitude = parts[2].replace(' E', '')
    height = parts[3].replace(' m Above Sea Level', '').strip() if len(parts) > 3 else ''
    lines[i] = f'{filename};{latitude};{longitude};{height}\n'

# Write the updated lines back to the CSV file
with open('coordinates.txt', 'w',encoding='utf-8') as file:
    file.write(header + '\n')
    file.writelines(lines)