# RenderDoc2obj
Generates obj file from RenderDoc capture CSV mesh data
# How to get the CVS files in RenderDoc?
## e.g. Elite Dangerous
* Start the game normally and get the executable and command line parameters with your favorite process tool like taskmanager, Process Explorer or Process Lasso
* Close the game
* Paste the settings in the program settings in RenderDoc and hit Launch
![image](https://github.com/user-attachments/assets/78cd90f1-7df9-4265-9840-ff729af0107e)

* Enter the game and hit F12 during the ship spinning loading screen.
* If you need other mesh data, get to the point in game where it is loaded and hit F12 to capture
* Exit the game

Back in RenderDoc we have the capture now.
Look for Colour Passes with high index counts, which indicates high ammount of vertices.

![image](https://github.com/user-attachments/assets/058b7390-81e8-4c36-b62a-a3b56c931e42)

Go to the Mesh Viewer Tab 

* double check the mesh, try out settings in the VS Out preview if you found the correct mesh

Right click the VS output data table -> Export to CVS
![image](https://github.com/user-attachments/assets/aa2b2c19-c448-4911-80aa-e1a80a372db2)
Repeat this process if the model is split into muliple meshes

From there on use the RenderDoc2obj script to convert all CSVs into one and finally into a OBJ file.

# Projection Matrix

Depending on the mesh, it's necessary to edit the projection matrix.
For ED loading screen models, this can be extracted from the Vertex Shader pipe line
![image](https://github.com/user-attachments/assets/be528a47-7364-409e-b221-f534d0ab79e9)
![image](https://github.com/user-attachments/assets/afb8e121-ba06-43b5-9bd9-daef1316b15e)

