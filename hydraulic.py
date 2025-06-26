#!/usr/bin/env python
# coding: utf-8

# # Read architecture from RSML file and run a simulation
# This is the notebook version of the example in read the doc. It is a small example to illustrate how to use the RSML format (http://rootsystemml.github.io/). The architecture is the arabidopsis-simple example http://rootsystemml.github.io/images/examples/arabidopsis-simple.rsml.

# Point to the source files if the notebook is run locally, from a git repository clone for example, without hydroroot installation, but only the dependencies installed.

# In[1]:


import rsml
from hydroroot import radius
from hydroroot.main import hydroroot_flow
from oawidgets.plantgl import PlantGL
from hydroroot.display import mtg_scene, plot
from hydroroot.hydro_io import import_rsml_to_discrete_mtg, export_mtg_to_rsml
from pathlib import Path
from pprint import pprint
from read import split


# In[2]:


data = Path('data')/'UC1_HIRROS_arabidopsis'
rsa_files = list(data.glob('*.rsml'))
pprint(rsa_files)


# Read the RSML file and convert it into a *continuous* MTG. This is a MTG where each root (primary and lateral) is represented by one vertex. The geometry of each root is then stored in g_c.property('geometry').

# In[4]:


g = rsml.rsml2mtg(rsa_files[0])


# To be used in HydroRoot the MTG has to be converted to a *discrete* form of MTG, i.e. each vertex represent a representative elementary volume of a given length for example $10^{-4}$ m. In HydroRoot the lengths are in meter, therefore we must retrieve the resolution and the unit of the RSML file. 

# In[5]:


resolution = g.graph_properties()['metadata']['resolution'] # pixel to unit
unit = g.graph_properties()['metadata']['unit']
print(unit)


# In[6]:


resolution = resolution * 1e-6 # pixel to unit to m


# In[7]:


# Split the forest into 5 independent graphs
g1, g2, g3, g4, g5 = gs =  split(g)


# Build the discrete MTG

# In[8]:


g = import_rsml_to_discrete_mtg(g1, segment_length = 1.0e-4, resolution = resolution)


# Calculate some properties needed to simulate a sap flux from the root under overpressure. 

# In[9]:


g = radius.ordered_radius(g, 7.0e-5, 0.7) # root radii
g = radius.compute_relative_position(g) # Compute the position of each segment relative to the axis bearing it


# Some conductance data versus distance to tip

# In[10]:


k_radial_data=([0, 0.2],[330.0,330.0]) #unit: microL/(s.MPa.m**2)
K_axial_data=([0, 1.5e-2, 4.0e-2, 6.0e-2, 8.0e-2, 10.0e-2, 12.0e-2, 15.0e-2, 20.0e-2]
              ,[ 3.0E-05, 3.0E-04, 3.9E-04, 3.5E-04, 4.0E-04, 8.0E-04, 9.0E-04, 8.4E-04, 4.4E-04]) #microL.m/(s.Mpa)


# Flux and equivalent conductance calculation, for a root in an external hydroponic medium at 0.4 MPa, its base at 0.1 MPa, and with the conductances set above.

# In[11]:


g, keq, jv = hydroroot_flow(g, psi_e = 0.4, psi_base = 0.1, axial_conductivity_data = K_axial_data, radial_conductivity_data = k_radial_data)


# In[12]:


print('equivalent root conductance (microL/s/MPa): ',keq, 'sap flux (microL/s): ', jv)


# Display the local water uptake heatmap in 3D

# In[13]:


s = mtg_scene(g, prop_cmap = 'j') # create a scene from the mtg with the property j is the radial flux in ul/s
PlantGL(s) # display the root into the plantgl oawidget


# Export the MTG to RSML

# At this stage (2022-08-22) only the root length and the branching position are used to simulate architecture in hydroponic solution. The exact position in 3D is not stored in the discrete MTG form and so not exported to RMSL.

# In[13]:


export_mtg_to_rsml(g, "test.rsml", segment_length = 1.0e-4)


# The resolution of the RSML data is 1.0e-4 and the unit is meter.

# In[ ]:




