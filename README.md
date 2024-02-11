# technician-routing

This project contains a library with a toolkit and demo application for routing HVAC technicians efficiently

# Installation

To install you will need to have python installed, our instructions will use anaconda

## 1. Download Anaconda

If not already done, download anaconda here and install it

https://www.anaconda.com/download

## 2. Create a new empty conda environment

Open anaconda prompt

    conda create -n routing-user python=3.11
    
[y] to proceed

    conda activate routing-user

## 3. Install the toolkit

There are a few ways to do this

### i. Install the built package from gitlab

Download tar bz2 file from this repo and install it to your conda environment
- conda install {path-to-tar.bz2}

Example:

    conda install c:/users/foo/downloads/technician-routing-0.1.2-3.tar.bz2


[y] to proceed


### ii.  Download source code and add to environment

Download the source from gitlab from the repo and either put its location in your path or type similar to

    conda develop c:/users/foo/path/to/technician_routing


replacing the path above with the real path to the technician_routing folder

## 4. Finish the conda environment you built

You will need to also install the dependencies of the routing toolkit

There is a file requirements.txt in the root of this project

In your new environment, install from the requirements file

    pip install -r c:/path/to/requirements.txt

Also explained here
- https://stackoverflow.com/questions/7225900/how-can-i-install-packages-using-pip-according-to-the-requirements-txt-file-from




# Packaging

These are meant to be instructions for the developer, to build a new tar.bz2

CD to technician-routing\packaging
conda-build . --output-dir ..\build

File is ouput to {conda-install}\conda-bld\
Should in a subfolder, likely win-64
