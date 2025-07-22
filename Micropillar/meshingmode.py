# Importing packages
import ansys.fluent.core as pyfluent
from ansys.fluent.core import examples
import os
import time
import subprocess
import psutil

# Caminho para a pasta contendo os arquivos de geometria
geometry_folder = r'YOURDIRECTORY'

# Listar todos os arquivos de geometria na pasta
geometry_files = [f for f in os.listdir(geometry_folder) if f.endswith('.scdoc')]


# Função para garantir que todos os processos do Fluent sejam encerrados
def kill_fluent_processes():
    for process in psutil.process_iter(['pid', 'name']):
        if 'fluent.exe' in process.info['name']:
            p = psutil.Process(process.info['pid'])
            p.terminate()
            try:
                p.wait(timeout=15)
            except psutil.TimeoutExpired:

                
                p.kill()
                
# Função para realizar o meshing com um arquivo de geometria
def run_meshing(geometry_file):
    meshing_session = pyfluent.launch_fluent(mode="meshing", show_gui = True, processor_count= 1, product_version="25.1.0", dimension= 3, precision="double")
    meshing_session.health_check.check_health()

    # Construir o caminho completo para o arquivo de geometria
    geometry_path = os.path.join(geometry_folder, geometry_file)

    # Reading the CAD file, from SpaceClaim
    meshing_session.workflow.InitializeWorkflow(WorkflowType=r'Watertight Geometry')
    meshing_session.meshing.GlobalSettings.LengthUnit.set_state(r'mm')
    meshing_session.meshing.GlobalSettings.AreaUnit.set_state(r'mm^2')
    meshing_session.meshing.GlobalSettings.VolumeUnit.set_state(r'mm^3')
    meshing_session.workflow.TaskObject['Import Geometry'].Arguments.set_state({'FileName': geometry_path})
    meshing_session.workflow.TaskObject["Import Geometry"].Execute()

    # Setting the conditions to mesh
    # Local Sizing
    meshing_session.workflow.TaskObject["Add Local Sizing"].AddChildToTask()
    meshing_session.workflow.TaskObject["Add Local Sizing"].Execute()

    # Surface mesh
    meshing_session.workflow.TaskObject["Generate the Surface Mesh"].Arguments = {
        "CFDSurfaceMeshControls": {"MaxSize": 0.10}
    }
    meshing_session.workflow.TaskObject["Generate the Surface Mesh"].Execute()


    # Describing geometry
    meshing_session.workflow.TaskObject["Describe Geometry"].UpdateChildTasks(SetupTypeChanged=True)
    meshing_session.workflow.TaskObject['Describe Geometry'].Arguments.set_state({r'Multizone': r'Yes',r'NonConformal': r'No',r'SetupType': r'The geometry consists of only fluid regions with no voids',})
    meshing_session.workflow.TaskObject['Add Boundary Layers'].InsertNextTask(CommandName=r'AddMultiZoneControls', Select=True)
    meshing_session.workflow.TaskObject['Add MultiZone Controls'].InsertNextTask(CommandName=r'GenerateTheMultiZoneMesh', Select=True)
    meshing_session.workflow.TaskObject['Describe Geometry'].Execute()

    # Setting Boundaries
    meshing_session.workflow.TaskObject["Update Boundaries"].Execute()
    meshing_session.workflow.TaskObject["Update Regions"].Execute()

    #Add boundary layers
    meshing_session.workflow.TaskObject['Add Boundary Layers'].Arguments.set_state({r'AddChild': r'no',r'BLControlName': r'smooth-transition_1',r'LocalPrismPreferences': {r'Continuous': r'Continuous',},})
    meshing_session.workflow.TaskObject['Add Boundary Layers'].Execute()




    # CAUTION: the nomenclature of the solid body!!! 
    # options: s-olido , or "volume-volume"
    meshing_session.workflow.TaskObject['Add MultiZone Controls'].Arguments.set_state({r'CompleteRegionScope': [r's-lido'],r'ControlType': r'Regions',r'FillWith': r'Hex-Pave',r'Intervals': 10,r'LabelSourceList': [r'inlet', r'outlet'],r'MultiZName': r'mz-region_1',r'RegionScope': [r's-lido'],r'SourceMethod': r'Labels',r'UseSweepSize': r'yes',})
    meshing_session.workflow.TaskObject['Add MultiZone Controls'].AddChildAndUpdate(DeferUpdate=True)
    meshing_session.workflow.TaskObject['Add MultiZone Controls'].Execute()

    meshing_session.workflow.TaskObject['Generate the MultiZone Mesh'].Arguments.set_state({r'RegionScope': [r's-lido'],})
    meshing_session.workflow.TaskObject['Generate the MultiZone Mesh'].Execute()

   # Gerar o nome do arquivo de malha com base no nome do arquivo de geometria
    mesh_filename = geometry_file.replace('.scdoc', '_meshing.msh.h5')
    mesh_filepath = os.path.join(geometry_folder, mesh_filename)
    
    # Salvar a malha gerada
    meshing_session.tui.file.write_mesh(mesh_filepath)

    meshing_session.tui.exit()


    # Garantir que todos os processos do Fluent sejam encerrados
    kill_fluent_processes()


# Iterar sobre cada arquivo de geometria e realizar o meshing
for geometry_file in geometry_files:
    run_meshing(geometry_file)
