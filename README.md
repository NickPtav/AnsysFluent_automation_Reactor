# AnsysFluent_automation_reactor

This repository contains two distinct CFD automation workflows developed using ANSYS tools, focusing on geometry generation, mesh creation, and solver configuration for chemical reactor applications.

The main goal is to demonstrate the flexibility and scalability of automated simulation pipelines in chemical engineering problems involving complex geometries and reactive flows.

## 📁 Repository Structure

├── micropillar/ # Geometry and mesh generation for a micropillar photoreactor
├── fluent_reaction_case/ # Automated CFD solver setup for a catalytic wall reactor with competitive


## 📌 Case Descriptions

### `micropillar/`

Contains scripts for the **parametric generation of CAD models** and **automated mesh creation** of a micropillar-based photoreactor.  
This geometry is used in CFD simulations of photocatalytic processes, and is suitable for both:

- **ANSYS Fluent** (fluid dynamics)
- **ANSYS Speos** (ray tracing)

Users can generate either:
- The internal fluid domain only (for CFD),
- Or the full solid model (for optical simulation).

### `fluent_reaction_case/`

Contains an automated workflow for setting up and executing **numerical simulations in ANSYS Fluent** for a planar catalytic reactor.  
This case involves **two competitive exothermic reactions** (A → B and A → C), and was developed for **parametric studies** and **optimization**.

Automation includes:
- Batch creation of Fluent input files,
- Solver execution across multiple configurations,
- Extraction of key simulation results (conversion, selectivity, temperature).

## ✅ Requirements

- Python 3.10+
- ANSYS Fluent (202X R1 or later)
- ANSYS SpaceClaim (for geometry generation)
- Conda (recommended for environment management)

See each folder’s `README.md` for detailed setup instructions, dependencies, and usage examples.

## 📚 Reference

The automated workflows presented here are part of a research study in CFD applied to chemical reactor engineering.  
Results from the optimization case will be published in the book:

> *Computational Fluid Dynamics in Chemical Engineering: Fundamentals and Applications*  
> Publication Date: July 1, 2026  
> ISBN: 9780443237119

---

This repository is intended to support reproducible simulations and promote the use of automation in advanced reactor modeling.

