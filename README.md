# stellar-evolution-emulators

## **Overview:**

This repository contains two Jupyter Notebooks: *stellar_evolution_emulators.ipynb* and *HNNI.ipynb*. 

The *stellar_evolution_emulators.ipynb* Notebook shows how to use the pre-trained machine-learning based surrogate models to make fast predictions of the classical photometric variables bolometric luminosity $\log L/L_\odot$, effective temperature $\log T_\mathrm{eff}/\mathrm{K}$ and surface gravity $\log g/\mathrm{[cm/s^2]}$ of stars during their evolution from the zero-age-main-sequence (ZAMS) up to the end of core-helium burning over a ZAMS mass range $M_\mathrm{ZAMS}/M_\odot \in (0.7, 300)$. The pre-trained models can be used for a variety of purposes, including rapid population synthesis and iterative-optimization based stellar parameter inference.

The *HNNI.ipynb* Notebook contains the *Hierarchical Nearest-Neighbor Interpolation* (HNNI) algorithm, which is an alternative method for interpolation of stellar evolution tracks. HNNI is more accurate but slower than the machine-learning based surrogate modeling. The HNNI algorithm requires access to the stellar evolution catalog data base, and here we use the MIST catalog pre-computed by [Choi et al. 2016](https://ui.adsabs.harvard.edu/abs/2016ApJ...823..102C/abstract). 

Both the machine-learning based surrogate models and HNNI are developed in [Maltsev et al. 2024](https://ui.adsabs.harvard.edu/abs/2024A%26A...681A..86M/abstract).

## **Package requirements:**
The following Python packages are required to run these Notebooks:

*stellar_evolution_emulators.ipynb*:
- scikit-learn version >= 1.3.0
- tensorflow version >= 2.5.0
- pickle
- numpy
- matplotlib
- pandas
- datetime

*HNNI.ipynb*:
- pandas
- numpy
- os
- sys
- matplotlib
