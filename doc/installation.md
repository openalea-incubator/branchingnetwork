# Installation

You must use conda environment : <https://docs.conda.io/en/latest/index.html>

## Users

### Create a new environment with branchingnetwork installed in there

```bash

mamba create -n branchingnetwork -c openalea3 -c conda-forge  openalea.branchingnetwork
mamba activate branchingnetwork
```

Install branchingnetwork in a existing environment

```bash
mamba install -c openalea3 -c conda-forge openalea.branchingnetwork
```

### (Optional) Test your installation

```bash
mamba install -c conda-forge pytest
git clone https://github.com/openalea/branchingnetwork.git
cd branchingnetwork/test; pytest
```

## Developers

### Install From source

```bash
# Install dependency with conda
mamba env create -n phm -f conda/environment.yml
mamba activate branchingnetwork

# Clone branchingnetwork and install
git clone https://github.com/openalea/branchingnetwork.git
cd branchingnetwork
pip install .

# (Optional) Test your installation
cd test; pytest
```
