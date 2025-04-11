# RenderDoc2obj

import csv
import os
import numpy as np

# Verzeichnis mit den CSV-Dateien (ändere den Pfad, falls nötig)
input_directory = '.'  # Aktuelles Verzeichnis, oder z. B. 'C:/path/to/csvs'
output_file = 'merged.csv'

# Liste aller CSV-Dateien im Verzeichnis
csv_files = [f for f in os.listdir(input_directory) if f.endswith('.csv') and f != output_file]

if not csv_files:
    print("Keine CSV-Dateien im Verzeichnis gefunden!")
    exit()

# Sammle alle Vertex-Daten
all_vertices = []
headers = None

for csv_file in csv_files:
    print(f"Verarbeite: {csv_file}")
    with open(csv_file, 'r') as infile:
        reader = csv.DictReader(infile)
        # Speichere die Header der ersten Datei
        if headers is None:
            headers = reader.fieldnames
        elif reader.fieldnames != headers:
            print(f"Warnung: {csv_file} hat andere Spalten als die erste Datei!")
            continue
        # Füge alle Zeilen hinzu (VTX und IDX unverändert)
        for row in reader:
            all_vertices.append(row)

# Schreibe die kombinierte CSV-Datei
with open(output_file, 'w', newline='') as outfile:
    writer = csv.DictWriter(outfile, fieldnames=headers)
    writer.writeheader()
    writer.writerows(all_vertices)

print(f"Fertig! {len(all_vertices)} Vertices in {output_file} geschrieben.")


# Ursprüngliche View-Projection-Matrix aus cb0[4-7]
view_proj_matrix = np.array([
    [1.05239, 0.0,    0.0, 0.0],
    [0.0,    1.87091, 0.0, 0.0],
    [0.0,    0.0,    0.0, 0.025],
    [0.0,    0.0,    1.0, 0.0]
])

# Inverse berechnen (wird später angepasst, falls nötig)
try:
    inv_view_proj = np.linalg.inv(view_proj_matrix)
except np.linalg.LinAlgError:
    print("Matrix ist nicht invertierbar. Wir müssen cb0[6] überprüfen.")
    exit()

vertices = []
with open('merged.csv', 'r') as csvfile:
    reader = csv.DictReader(csvfile,skipinitialspace=True)
    for i, row in enumerate(reader):
        clip_coords = np.array([
            float(row['SV_POSITION.x']),
            float(row['SV_POSITION.y']),
            float(row['SV_POSITION.z']),
            float(row['SV_POSITION.w'])
        ])
        world_coords = inv_view_proj.dot(clip_coords)
        if world_coords[3] != 0:
            world_coords = world_coords / world_coords[3]
        vertices.append([world_coords[0], world_coords[1], world_coords[2]])
        # Debug: Ausgabe der ersten 5 Koordinaten
        if i < 5:
            print(f"Vertex {i}: {world_coords[0]}, {world_coords[1]}, {world_coords[2]}")

with open('ship.obj', 'w') as objfile:
    for v in vertices:
        objfile.write(f"v {v[0]} {v[1]} {v[2]}\n")


# Vertices aus der alten ship.obj lesen
vertices = []
with open('ship.obj', 'r') as objfile:  # Ersetze 'ship_old.obj' mit dem tatsächlichen Dateinamen
    for line in objfile:
        if line.startswith('v '):
            x, y, z = map(float, line.strip().split()[1:])
            vertices.append([x, y, z])

# Faces als Triangle List (jede 3 Vertices)
faces = []
for i in range(0, len(vertices), 3):
    if i + 2 < len(vertices):
        faces.append([i + 1, i + 2, i + 3])  # +1, da OBJ bei 1 beginnt

# Schreibe neue OBJ-Datei
with open('ship_with_faces.obj', 'w') as objfile:
    for v in vertices:
        objfile.write(f"v {v[0]} {v[1]} {v[2]}\n")
    for f in faces:
        objfile.write(f"f {f[0]} {f[1]} {f[2]}\n")

print(f"Erzeugt: {len(vertices)} Vertices, {len(faces)} Faces")