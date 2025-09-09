# ----------------------------------------------------------------------------------
# Imports

from pathlib import Path
import ansys.fluent.core as pyfluent
from ansys.fluent.core import examples
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib import image
from ansys.fluent.parametric import ParametricProject, ParametricStudy

# ----------------------------------------------------------------------------------
# User-defined inputs
vel_temp_values = [(1.0, 300)]

# Number of desired simulations
n_samples = 10  # you can increase it to 100, 200, etc.

# Parameter ranges
bounds = {
    "A1": (1e13, 2e16),
    "Ea1": (1e8, 3e8),
    "n1": (100, 600),
    "A2": (1e13, 2e16),
    "Ea2": (1e8, 3e8),
    "n2": (100, 600),
}

# Function that generates the values
def generate_samples(bounds_dict, n):
    return {
        key: np.random.uniform(low, high, n)
        for key, (low, high) in bounds_dict.items()
    }

# Generates all combinations
samples = generate_samples(bounds, n_samples)
# ----------------------------------------------------------------------------------
for i in range(n_samples):
    vel, temp = vel_temp_values[0] 

    # Taking random values from the sample
    A1 = samples["A1"][i]
    Ea1 = samples["Ea1"][i]
    n1 = samples["n1"][i]
    A2 = samples["A2"][i]
    Ea2 = samples["Ea2"][i]
    n2 = samples["n2"][i]

    # Launch Fluent solver
    solver = pyfluent.launch_fluent(ui_mode="gui", processor_count=1, product_version="25.1.0", version="2d", precision="double")

    # Read mesh and set units
    solver.settings.file.read_mesh(file_name=r"C:/Users/usuario/Documents/Nicole/Cap_Livro2/reactor_mesh.msh")
    solver.tui.define.units("length", "mm")
    solver.mesh.check()
    solver.mesh.quality()

    # Enable physical models
    solver.setup.models.viscous.model = "laminar"
    solver.setup.models.species.model.option = "species-transport"
    solver.setup.models.species.reactions.enable_volumetric_reactions = True
    solver.setup.models.species.reactions.enable_wall_surface = True
    solver.setup.models.species.wall_surface_options.heat_of_surface_reactions = True
    solver.setup.models.species.options.diffusion_energy_source = True

    # Define all species (copy from database and customize if needed)
    for sp in ["water-vapor", "oxygen", "nitrogen"]:
        solver.tui.define.materials.copy("fluid", sp)

    species_custom = ["spe-a", "spe-b", "spe-c", "spe-d"]
    for sp in species_custom:
        solver.settings.setup.materials.database.copy_by_name(type="fluid", name="air", new_name=sp)
        solver.setup.materials.fluid[sp] = {
            "density": {"option": "constant", "value": 1.225},
            "specific_heat": {"option": "constant", "value": 1006.43},
            "thermal_conductivity": {"option": "constant", "value": 0.0242},
            "viscosity": {"option": "constant", "value": 0.000017894},
            "molecular_weight": {"option": "constant", "value": 28.966},
            "formation_entropy": {"option": "constant", "value": 194336}
        }

    # Mixture and reaction definition
    parameters = [
        "mixture-template", "mixture-template",
        "yes", "4",
        *species_custom,
        "0", "0", "yes", "2",

        # Reaction 1
        "reaction-1", "yes", "no", "no",
        "1", "spe-a", "1", "1",
        "1", "spe-b", "1", "1",
        str(A1), str(Ea1), str(n1), "no", "no",

        # Reaction 2
        "reaction-2", "yes", "no", "no",
        "1", "spe-a", "1", "1",
        "1", "spe-c", "1", "1",
        str(A2), str(Ea2), str(n2), "no", "no",
    ]

    solver.tui.define.materials.change_create(*parameters)

    solver.settings.setup.materials.mixture['mixture-template'] = {
        "density": {"option": "volume-weighted-mixing-law"},
        "specific_heat": {"option": "mixing-law"},
        "thermal_conductivity": {"option": "mass-weighted-mixing-law"},
        "viscosity": {"option": "mass-weighted-mixing-law"},
        "mass_diffusivity": {"option": "kinetic-theory"},
    }

    # Cell zone conditions
    solver.settings.setup.cell_zone_conditions.fluid['fff_entrance'].reaction.react = False
    solver.settings.setup.cell_zone_conditions.fluid['fff_reactor'].reaction.react = False

    # Boundary conditions - Inlet
    solver.settings.setup.boundary_conditions.velocity_inlet = {
        'inlet': {
            'name': 'inlet',
            'momentum': {
                'velocity_specification_method': 'Magnitude, Normal to Boundary',
                'reference_frame': 'Absolute',
                'velocity_magnitude': {'option': 'value', 'value': vel},
                'initial_gauge_pressure': {'option': 'value', 'value': 0}
            },
            'turbulence': None,
            'thermal': {'temperature': {'option': 'value', 'value': temp}},
            'species': {
                'specify_species_in_mole_fractions': True,
                'species_mole_fraction': {
                    'spe-a': {'option': 'value', 'value': 0.1},
                    'spe-b': {'option': 'value', 'value': 0},
                    'spe-c': {'option': 'value', 'value': 0}
                }
            }
        }
    }

    # Wall boundary conditions
    solver.settings.setup.boundary_conditions.wall["reactive_wall"].species.react = True

    # Load UDF
    solver.tui.define.user_defined.compiled_functions("load", "libudf")

    # Residual criteria
    solver.tui.solve.monitors.residual.convergence_criteria("1e-04", "1e-04", "1e-04", "1e-06", "1e-08", "1e-08", "1e-08")

    # Initialize solution
    solver.tui.solve.initialize.compute_defaults.velocity_inlet()
    solver.solution.initialization.standard_initialize()

    # Set UDF thermal boundary condition
    solver.tui.define.user_defined.function_hooks("surface-reaction-rate", '"RXN_ARRHENIUS::libudf"')
    wall_bc = solver.settings.setup.boundary_conditions.wall["reactive_wall"]
    wall_bc.thermal.thermal_condition = "Heat Flux"
    wall_bc.thermal.heat_flux.option = "udf"
    wall_bc.thermal.heat_flux.udf = "HEAT_PROFILE_RXN_PARALLEL::libudf"

    # Final initialization
    solver.tui.solve.initialize.compute_defaults.velocity_inlet()
    solver.solution.initialization.standard_initialize()

    # Run the simulation
    solver.settings.solution.run_calculation.iterate(iter_count=1000)

    # Save case/data file with identifying name
    file_name = f"sim_{i+1:03d}_A1_{int(A1)}_Ea1_{int(Ea1)}_A2_{int(A2)}_Ea2_{int(Ea2)}"
    solver.file.write(file_type='case-data', file_name=file_name)

    # Exit solver
    solver.exit()
