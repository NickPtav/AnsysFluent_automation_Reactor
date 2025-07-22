# CFD Automation – Catalytic Wall Reactor with Competitive Reactions

This folder contains the files and automation scripts used for simulating a planar catalytic wall reactor with two competitive reactions:

- A → B (desired)
- A → C (undesired)

Both reactions are exothermic and occur at the reactor walls.

## 🎯 Objective

Automate the setup and execution of CFD simulations in ANSYS Fluent to generate datasets for optimization studies based on:

- Conversion of A  
- Selectivity toward B  
- Maximum temperature in the reactor

📚 Reference
This case study is part of the research published in the upcoming book:
Computational Fluid Dynamics in Chemical Engineering: Fundamentals and Applications (Release date: July 1, 2026. ISBN: 9780443237119)

## ⚙️ Requirements

- ANSYS Fluent 2025 (tested with version 25.1)  or less.
- Python 3.8+ (optional, for batch automation)  
- Linux or Windows with Fluent Student or with license. 

⚙️ Environment Setup
To run this automation script properly, it's recommended to use a dedicated Conda environment. Follow the steps below:
1. Create and activate the environment
   ```
    conda create -n fluent_env python=3.10
    conda activate fluent_env

   ```

2. Install required packages
   ```
   pip install ansys-fluent-core ansys-fluent-visualization
   pip install numpy matplotlib seaborn
   ```

3. Run the automation script
   ```
   python fluent_setup.py
   ```
