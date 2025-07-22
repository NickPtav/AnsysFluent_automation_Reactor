# CAD and Mesh Automation – Micropillar Photoreactor

This directory contains scripts for the automated generation of the CAD geometry and mesh of a **micropillar photoreactor**. The reactor is designed for **fluid flow and catalytic reactions** and is suitable for use in **CFD simulations** (e.g., ANSYS Fluent) and **optical simulations** (e.g., ray tracing in ANSYS Speos).

## 🧱 Reactor Overview

The reactor geometry consists of a rectangular microchannel with cylindrical pillars arranged in a structured pattern. This design enhances surface area and mixing, and is commonly used in **photocatalytic** applications.

## 🗂️ Key Files

- `CAD_volume_script.py`:  
  Generates only the **internal fluid domain**, sufficient for **CFD simulations** in ANSYS Fluent.

- `CAD_completemodel_script.py`:  
  Generates the **full geometry**, including solid components, suitable for **ray tracing simulations** in ANSYS Speos.

- `geometry_generator.py`:  
  Runs inside **ANSYS SpaceClaim** and executes the selected CAD script(s) to build the 3D models automatically.

- `meshingmode.py`:  
  Optional script to automate mesh generation using the geometries previously created.

## ▶️ How to Use

1. **Edit the CAD script parameters** (`CAD_volume_script.py` or `CAD_completemodel_script.py`) as needed to define pillar dimensions, spacing, channel size, etc.

2. **Set the output directory** where the CAD scripts will be saved.  
   ⚠️ *This path must match the directory that `geometry_generator.py` will later access.*

3. **Open ANSYS SpaceClaim** and run `geometry_generator.py` to build the geometries based on the saved scripts.

4. *(Optional)* Run `meshingmode.py` to generate the mesh files.  
   ⚠️ This script will search for geometries in a specified directory — make sure the geometry files are saved in the correct location.

## 💡 Notes

- All CAD and mesh parameters are fully customizable by the user through the provided Python scripts.
- Scripts can be executed via **Visual Studio Code** or directly from the **Anaconda Prompt** with the correct environment activated.
- Ensure ANSYS SpaceClaim is installed and properly licensed on your system.

## 📦 Dependencies

- ANSYS SpaceClaim (required to generate geometry)
- Python 3.10+
- Conda environment recommended

You may create a virtual environment using:

```bash
conda create -n cad_env python=3.10
conda activate cad_env
