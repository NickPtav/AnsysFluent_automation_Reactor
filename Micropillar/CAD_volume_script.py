

# Valores dos parâmetros
alt_reac_values    = [1.2, 2.1, 2.8, 1.5, 2.6, 1.9, 2.3, 1.7, 2.0, 1.4]
larg_reac_values   = [9.0, 12.5, 14.0, 10.2, 11.8, 8.5, 13.5, 15.0, 9.8, 12.0]
compri_reac_values = [25.0, 45.0, 60.0, 30.0, 55.0, 22.0, 48.0, 35.0, 40.0, 50.0]
num_rows_values    = [15, 30, 45, 20, 40, 25, 35, 18, 28, 32]
num_columns_values = [6, 9, 10, 7, 8, 5, 9, 10, 6, 7]

# Template do script SpaceClaim
template_script = """

# Python Script, API Version = V251
from math import sin, sqrt, cos, radians, tan, pi, acos
from clr import AddReference
AddReference("System")
from System import Double
from System import Array
#************************
# PARAMETERS
#************************

alt_reac    = {}            # Extrusion height (mm)
larg_reac   = {}
compri_reac = {}
num_rows    = {}           # Number of paralel rows with the center 
num_columns = {}            # Number of paralel columns with the center
angle       = 60
H           = (compri_reac/num_rows)
print(H)                            # Distance between paralel circles (mm)
L           = (H/2)/cos(angle)       # Distance between diagonal circles (mm)
V           = (larg_reac/num_columns)
print(V)
r           = 0.2            # Circles radius (mm)

#Fixed
pilar_area = (r**2)*pi


#***************************************
# CREATING REACTOR VOLUME (RETANGULO)
#***************************************

#~~~~~~~~~~~~~~~~
# 1 - Creating Metal plate
# Definir plano de esboço
sectionPlane = Plane.Create(Frame.Create(Point.Create(MM(0), MM(0), MM(0)), 
    Direction.DirZ, 
    Direction.DirX))
result = ViewHelper.SetSketchPlane(sectionPlane, None)


x_start = 0
z_start = 0
x_final = compri_reac
z_final = larg_reac

# Rectangle sketch
point1 = Point2D.Create(MM(0),MM(0))
point2 = Point2D.Create(MM(z_final),MM(x_start))
point3 = Point2D.Create(MM(z_final),MM(x_final))
result = SketchRectangle.Create(point1, point2, point3)

# Create surface
mode = InteractionMode.Solid
result = ViewHelper.SetViewMode(mode, None)
# EndBlock

# Extrusion
selection = FaceSelection.Create(GetRootPart().Bodies[0].Faces[0])
options = ExtrudeFaceOptions()
options.ExtrudeType = ExtrudeType.ForceIndependent
result = ExtrudeFaces.Execute(selection, MM(alt_reac), options)
# EndBlock

# Definir plano de esboço
sectionPlane = Plane.Create(Frame.Create(Point.Create(MM(1), MM(alt_reac + 2), MM(1)), 
    Direction.DirZ, 
    Direction.DirX))
result = ViewHelper.SetSketchPlane(sectionPlane, None)

x_start = 0
z_start = 0
x_final = compri_reac
z_final = larg_reac

#~~~~~~~~~~~~~~~~
# 2 - Creating chambers and channels
# 2D to cut out the volume of the plate

# Definir plano de esboço
sectionPlane = Plane.Create(Frame.Create(Point.Create(MM(0), MM(alt_reac + 1), MM(0)), 
    Direction.DirZ, 
    Direction.DirX))
result = ViewHelper.SetSketchPlane(sectionPlane, None)

# Initial position
x_start = V #(mm)
y_start = H #(mm)

# Loop to create circles and channels
# The right vision of the reactor is with the inlets and outlets in a vertical position
# In this way, the number of columns will determine the number of inlets and outlets.

for i in range(num_rows - 1): 
    for j in range(num_columns - 1):
        # Calculate the position of the circle's center
        x_center = x_start + j * V
        y_center = y_start + i * H
        
        # Create paralels circles
        origin = Point2D.Create(MM(x_center),MM( y_center))
        result_circle = SketchCircle.Create(origin, MM(r))
        
        # Add diagonal circles
        if i < num_rows - 2 and j < num_columns - 2:
            # Calculate the position of the diagonal circle's center
            x_diagonal = x_start + (j + 0.5000) * V
            y_diagonal = y_start + (i + 0.5000) * H
            
            # Create the diagonal circle
            origin_diagonal = Point2D.Create(MM(x_diagonal),MM(y_diagonal))
            result_diagonal = SketchCircle.Create(origin_diagonal, MM(r))

# Creating surface
mode = InteractionMode.Solid
result = ViewHelper.SetViewMode(mode, None)
# EndBlock

# Creating pilars group to extrusion
comp = Selection.Create(GetRootPart())
faces = comp.ConvertToFaces().FilterByArea(MM2(pilar_area - 0.0001),MM2(pilar_area+0.0001))
groupCamaras= faces.CreateAGroup('pilars')


# Extrusion
selection = FaceSelection.CreateByGroups('pilars' )
options = ExtrudeFaceOptions()
options.ExtrudeType = ExtrudeType.ForceCut
result = ExtrudeFaces.Execute(selection, MM(-alt_reac - 1), options)
#EndBlock

# -----------
# Nomear Inlet e Outlet
# 1 - Creating Inlet

sectionPlane = Plane.Create(Frame.Create(Point.Create(MM(-0.2), MM(0), MM(0)), 
    Direction.DirZ, 
    Direction.DirY))
result = ViewHelper.SetSketchPlane(sectionPlane, None)

x_start = 0
z_start = 0
x_final = alt_reac
z_final = larg_reac

# Rectangle sketch
point1 = Point2D.Create(MM(0),MM(0))
point2 = Point2D.Create(MM(z_final),MM(x_start))
point3 = Point2D.Create(MM(z_final),MM(x_final))
result = SketchRectangle.Create(point1, point2, point3)

# Create surface
mode = InteractionMode.Solid
result = ViewHelper.SetViewMode(mode, None)
# EndBlock

min_point =  Point.Create(MM(-0.2), MM(-0.1), MM(-0.1))
max_point = Point.Create(MM(-0.05), MM(alt_reac), MM(larg_reac))

BoundingBox = Box.Create(min_point, max_point)
faces = comp.ConvertToFaces().FilterByBoundingBox(BoundingBox)
faces.CreateAGroup('inlet')

x_final = 0.2
# Extrudar 1 face
selection = FaceSelection.CreateByGroups('inlet')
options = ExtrudeFaceOptions()
options.ExtrudeType = ExtrudeType.ForceAdd
result = ExtrudeFaces.Execute(selection, MM(-0.2), options)
# EndBlock

# 1 - Creating Outlet

sectionPlane = Plane.Create(Frame.Create(Point.Create(MM(compri_reac + 0.2), MM(0), MM(0)), 
    Direction.DirZ, 
    Direction.DirY))
result = ViewHelper.SetSketchPlane(sectionPlane, None)

x_start = 0
z_start = 0
x_final = alt_reac
z_final = larg_reac

# Rectangle sketch
point1 = Point2D.Create(MM(0),MM(0))
point2 = Point2D.Create(MM(z_final),MM(x_start))
point3 = Point2D.Create(MM(z_final),MM(x_final))
result = SketchRectangle.Create(point1, point2, point3)

# Create surface
mode = InteractionMode.Solid
result = ViewHelper.SetViewMode(mode, None)
# EndBlock

min_point =  Point.Create(MM(compri_reac + 0.1), MM(-0.1), MM(-0.1))
max_point = Point.Create(MM(compri_reac + 0.2), MM(alt_reac + 0.1), MM(larg_reac + 2))

BoundingBox = Box.Create(min_point, max_point)
faces = comp.ConvertToFaces().FilterByBoundingBox(BoundingBox)
faces.CreateAGroup('outlet')

# Extrudar 1 face
selection = FaceSelection.CreateByGroups('outlet')
options = ExtrudeFaceOptions()
options.ExtrudeType = ExtrudeType.ForceAdd
result = ExtrudeFaces.Execute(selection, MM(0.2), options)

#******************
# Save and Export
#******************
rows = str(num_rows)
columns = str(num_columns)
compri = str(compri_reac)
File_name = str("/" + "rows" + rows + "col" + columns + "compr" + compri + ".scdocx")
print(File_name)
Path = r"C:/Users/usuario/Documents/Nicole/Cap_Livro2/CAD/geometrias"
File_path = Path + File_name
DocumentSave.Execute(File_path)

"""

# Loop para criar e salvar os scripts com todas as combinações de valores

# Loop para criar e salvar os scripts com os valores correspondentes
for alt_reac, larg_reac, compri_reac, num_rows, num_columns in zip(alt_reac_values, larg_reac_values, compri_reac_values, num_rows_values, num_columns_values):
    # Substituir os valores no template do script
    script = template_script.format(alt_reac, larg_reac, compri_reac, num_rows, num_columns)
    
    # Substituir pontos por underscores nos nomes de arquivo
    compri_filename = str(compri_reac).replace(".", "_")
    
    # Nome do arquivo
    filename = f"C:/Users/usuario/Documents/Nicole/Cap_Livro2/CAD/scripts/script_r{num_rows}c{num_columns}comp{compri_filename}.py"
    
    # Salvar o script
    with open(filename, "w") as f:
        f.write(script)
