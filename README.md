# technician-routing

# Installation

- Create a new empty conda environment

conda create -n routing-user python=3.11
proceed = y
conda activate routing-user


- Download tar bz2 file

Install

conda install {path-to-tar.bz2}
Example:  conda install c:/users/foo/downloads/technician-routing-0.1.2-3.tar.bz2

[y] to proceed

conda install technician-routing -c ..\build

- Install Jupyter

conda install jupyter -y

- Run notebook




# packaging

CD to technician-routing\packaging
conda-build . --output-dir ..\build

File is ouput to {conda-install}\conda-bld\
Should in a subfolder, likely win-64
