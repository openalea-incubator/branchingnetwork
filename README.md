# OpenAlea models, algorithms and simulation tools for Root Branching Network

The [Colloquium](https://dyco.lied.univ-paris-diderot.fr/BranchingNetworksFromExperimentToTheory_2025) is held in Paris, on 26 and 27 June 2025.

This repository share a 2D+t root system architecture (RSA) dataset reconstructed automatically from the HIRROS platform.

[OpenAlea](https://openalea.rtfd.io) is an open-source platform for
**branchingnetwork** Tutorial for the workshop on Branching Networks

[OpenAlea](https://openalea.rtfd.io) provides a set of packages for working on plant architecture
* [Mutliscale Tree Graph or MTG](https://mtg.rtfd.io) is a standard datastructure for querying, analysing, and visualising Plant Arhitecture.
* [RSML](https://github.com/openalea/rsml) is a format for representing Root System Architecture 
* [LPy](https://github.com/openalea/lpy) is a language and a (L-)system to simulate plants in 3D
* [Hydroroot](https://github.com/openalea/hydroroot) computes hydraulic fluxes in a root architecture
* [StructureAnalysis](https://github.com/openalea/StructureAnalysis) provides models for statistical analysis of the structure of the plants (Markov, Semi-Markov, Hidden-Semi_Markov models for sequence and tree)
* and much more (see https://github.com/openalea and https://github.com/openalea-incubator)

[RootSystemTracker](https://github.com/rocsg/rootsystemtracker/) reconstructs RSA from 2D+t images and  

## Authors
- Christophe Pradal ([@pradal](https://github/pradal) ) : Multiscale Tree Graph, Topological Analysis, Simulation, Software
- Fabrice Bauget ([@baugetfa](https://github/baugetfa)) : Hydraulic, RSML, Software
- Thomas Arsouze ([@thomasarsouze](https://github/thomasarsouze)) : software
- Frederic Boudon ([@fredboudon](https://github/fredboudon)): L-System Simulation, Tree Matching
- Jean-Baptiste Durand ([@jbdurand](https://github/jbdurand)) : Tree Markovian models, Structure Analysis
- Stathis Delivorias ([@jazzsta](https://github/jazzsta)) : Topological Data Analysis
- Romain Fernandez ([@rocsg](https://github/rocsg)) : Spatio-temporal image analysis and phenotyping
- Loaï Gandeel ([@Money-eng](https://github/Money-eng)) : Spatio-temporal image analysis and phenotyping, RSML
- Philippe Nacry (INRAE, IPSIM) : HIRROS, data acquisition

## Institute
* [CIRAD](https://www.cirad.fr), [UMR AGAP institute](https://umr-agap.cirad.fr/) and [UMR AMAP](https://amap.cirad.fr/).
* The [MaCS4Plants](https://macs4plants.cirad.fr/) network : Math & CS for modelling agroecosystems.
* INRAE IPSIM, Montpellier : hydraulic and root phenotyping
* inria and INRAE are members of the OpenAlea consortium

## Install

### Dependencies
Packages are on the [openalea3](https://anaconda.org/openalea3) channel

Dependencies : 
* openalea.mtg
* openalea.plantgl
* rsml



### Mamba / Conda
```bash
mamba create -n branch -c openalea3 -c conda-forge openalea.mtg oawidgets rsml networkx jupyterlab
```

To compute fluxes use
```bash
mamba activate branch
mamba install -c openalea3 -c conda-forge openalea.hydroroot
```

## Citations

### Multiscale plat and root representation
- Pradal, C., & Godin, C. (2020). MTG as a standard representation of plants in FSPMs.
- Lobet, G., Pound, M. P., Diener, J., Pradal, C. et al. (2015). Root system markup language: toward a unified root architecture description language. Plant physiology, 167(3), 617-627. https://doi.org/10.1104/pp.114.253625

### Root Hydraulic  Architecture
- Bauget, F., Protto, V., Pradal, C., Boursiac, Y., & Maurel, C. (2023). A root functional–structural model allows assessment of the effects of water deficit on water and solute transport parameters. Journal of Experimental Botany, 74(5), 1594-1608. https://doi.org/10.1093/jxb/erac471 
- Boursiac, Y., Pradal, C., Bauget, F., Lucas, M., Delivorias, S., Godin, C., & Maurel, C. (2022). Phenotyping and modeling of root hydraulic architecture reveal critical determinants of axial water transport. Plant Physiology, 190(2), 1289-1306. https://doi.org/10.1093/plphys/kiac281

### Plant Simulation with L-Systems
- Boudon, F., Pradal, C., Cokelaer, T., Prusinkiewicz, P., & Godin, C. (2012). L-Py: an L-system simulation framework for modeling plant architecture development based on a dynamic language. Frontiers in plant science, 3, 76. https://doi.org/10.3389/fpls.2012.00076

### Statistical Analysis of branching systems
- Hidden Markov Tree Models : Durand et al., [2004](https://doi.org/10.1109/TSP.2004.832006), [2005](https://doi.org/10.1111/j.1469-8137.2005.01405.x)
- Partially ordered Markov out-trees : [Fernique 2014](https://theses.hal.science/tel-01365814v1)

### Contributors

Thanks to all that ontribute making this package what it is !

<a href="https://github.com/openalea-incubator/branchingnetwork/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=openalea-incubator/branchingnetwork" />
</a>
