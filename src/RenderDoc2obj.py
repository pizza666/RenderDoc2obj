# RenderDoc2obj
# usage:    copy all exported CVS files from RenderDoc into the same 
#           directory with this script
#           run script without any parameters "python RenderDoc2obj.py"
# generates:    ship.obj -> contains only vertices without faces
#               ship_with_faces.obj -> vertices with connected faces

import csv
import os
import numpy as np

# TODO: make the input directoy variable with arguments

input_directory = '.'  # current directory
output_file = 'merged.csv'

# read all CSVs
csv_files = [f for f in os.listdir(input_directory) if f.endswith('.csv') and f != output_file]

if not csv_files:
    print("Couln't find any CSV files!")
    exit()

# get all vertices 
all_vertices = []
headers = None

for csv_file in csv_files:
    print(f"Processing: {csv_file}")
    with open(csv_file, 'r') as infile:
        reader = csv.DictReader(infile)
        # store headers of the first file
        if headers is None:
            headers = reader.fieldnames
        elif reader.fieldnames != headers:
            print(f"Warning: {csv_file} has different headers!")
            continue
        # add all rows
        for row in reader:
            all_vertices.append(row)

# write vertices to file
with open(output_file, 'w', newline='') as outfile:
    writer = csv.DictWriter(outfile, fieldnames=headers)
    writer.writeheader()
    writer.writerows(all_vertices)

print(f"Done: {len(all_vertices)} vertices written to file {output_file} ")

# projection matrix aus cb0[4-7]
# TODO: this is the default projection matrix for the Elite Dangerous 
#       meshs from the loading screen. We need to import this later from 
#       a seperate file

view_proj_matrix = np.array([
    [1.05239, 0.0,    0.0, 0.0],
    [0.0,    1.87091, 0.0, 0.0],
    [0.0,    0.0,    0.0, 0.025],
    [0.0,    0.0,    1.0, 0.0]
])

# invert calculation 
try:
    inv_view_proj = np.linalg.inv(view_proj_matrix)
except np.linalg.LinAlgError:
    print("Warning: Matrix not invertable")
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
        # Debug: output of the first 5 vertices
        # TODO: add arguments for debugging and maybe output count of this part
        if i < 5:
            print(f"Debug: Vertex {i}: {world_coords[0]}, {world_coords[1]}, {world_coords[2]}")

with open('ship.obj', 'w') as objfile:
    for v in vertices:
        objfile.write(f"v {v[0]} {v[1]} {v[2]}\n")


# read vertices from ship.obj
# TODO: make the output files variable through arguments
vertices = []
with open('ship.obj', 'r') as objfile:
    for line in objfile:
        if line.startswith('v '):
            x, y, z = map(float, line.strip().split()[1:])
            vertices.append([x, y, z])

# write faces (every 3 vertices), this seem to work pretty well without any index table, atleast with the exports for Elite Dangerous
faces = []
for i in range(0, len(vertices), 3):
    if i + 2 < len(vertices):
        faces.append([i + 1, i + 2, i + 3])

# write file with faces
with open('ship_with_faces.obj', 'w') as objfile:
    for v in vertices:
        objfile.write(f"v {v[0]} {v[1]} {v[2]}\n")
    for f in faces:
        objfile.write(f"f {f[0]} {f[1]} {f[2]}\n")

print(f"Done: {len(vertices)} Vertices, {len(faces)} Faces")