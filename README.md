# stellar-evolution-emulators

## **Overview:**

This repository contains four Jupyter Notebooks *stellar_evolution_emulators.ipynb*, *HNNI.ipynb*, *ML-two-step-pipeline.ipynb* and *deep_learning_model_training.ipynb*. 

The *stellar_evolution_emulators.ipynb* Notebook shows how to use the pre-trained machine-learning based surrogate models to make fast predictions of the classical photometric variables bolometric luminosity $\log L/L_\odot$, effective temperature $\log T_\mathrm{eff}/\mathrm{K}$ and surface gravity $\log g/\mathrm{cm/s^2}$ of stars during their evolution from the zero-age-main-sequence (ZAMS) up to the end of core-helium burning over a ZAMS mass range $M_\mathrm{ZAMS}/M_\odot \in (0.7, 300)$. The pre-trained models can be used for a variety of purposes, including rapid population synthesis and iterative-optimization based stellar parameter inference.

The *HNNI.ipynb* Notebook contains the *Hierarchical Nearest-Neighbor Interpolation* (HNNI) algorithm, which is an alternative method for interpolation of stellar evolution tracks. HNNI is more accurate but slower than the machine-learning based surrogate modeling. The HNNI algorithm requires access to the stellar evolution catalog data base, and here we use the MIST catalog pre-computed by [Choi et al. 2016](https://ui.adsabs.harvard.edu/abs/2016ApJ...823..102C/abstract). 

Both the machine-learning based surrogate models and HNNI are developed in [Maltsev et al. 2024](https://ui.adsabs.harvard.edu/abs/2024A%26A...681A..86M/abstract).

The *ML-two-step-pipeline.ipynb* Notebook is a tutorial on how to use supervised learning to construct surrogate models of stellar evolution. It covers basic topics such as the regression problem formulation, performance scoring, data visualization, model selection and hyperparameter optimization. For simplicity, only non- deep learning models are used here (*Random Forest* and *k-nearest neighbor* regression models).

The *deep_learning_model_training.ipynb* Notebook is a tutorial-style demonstration how to construct a deep-learning based surrogate model of stellar evolution using *TensorFlow*. Here, we train a feedforward neural network architecture on the MIST catalog and track its learning in real-time using the *Tensorboard* callback. 

The last two Notebooks could serve as templates for future work on stellar evolution surrogate modeling. 

**Package requirements:**
In order to run the *stellar_evolution_emulators.ipynb*, you will need the following Python packages:
- scikit-learn version >= 1.3.0
- tensorflow version >= 2.5.0
- pickle
- numpy
- matplotlib
- pandas
- datetime

In order to run *HNNI.ipynb*, you will need only the following very basic packages:
- pandas
- numpy
- datetime
- os
- sys
- scikit-learn
- matplotlib

In order to run *deep_learning_model_training.ipynb*, 
