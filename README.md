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



### Contributors

Thanks to all that ontribute making this package what it is !

<a href="https://github.com/openalea-incubator/branchingnetwork/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=openalea-incubator/branchingnetwork" />
</a>
