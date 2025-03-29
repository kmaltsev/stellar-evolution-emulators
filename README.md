# stellar-evolution-emulators

## **Overview:**

This repository contains two Jupyter Notebooks: *stellar-evolution-emulator-fitted-models.ipynb* and *HNNI.ipynb*. 

The *stellar-evolution-emulator-fitted-models.ipynb* Notebook shows how to use the pre-trained machine-learning based surrogate models (stored in the "/models/..." directory) to make fast predictions of the classical photometric variables bolometric luminosity $\log L/L_\odot$, effective temperature $\log T_\mathrm{eff}/\mathrm{K}$ and surface gravity $\log g/\mathrm{[cm/s^2]}$ of stars during their evolution from the zero-age-main-sequence (ZAMS) up to the end of core-helium burning over a ZAMS mass range $M_\mathrm{ZAMS}/M_\odot \in (0.7, 300)$. The pre-trained models are trained and tested on the MIST catalog pre-computed by [Choi et al. 2016](https://ui.adsabs.harvard.edu/abs/2016ApJ...823..102C/abstract). The fitted models can be used for a variety of purposes, including rapid population synthesis and iterative-optimization based stellar parameter inference.

The *HNNI.ipynb* Notebook contains the *Hierarchical Nearest-Neighbor Interpolation* (HNNI) algorithm, which is an alternative method for automated interpolation of stellar evolution tracks that does not require their segmetation into separate evolutionary phases. HNNI is more accurate but slower than the machine-learning based surrogate modeling, and predicts any stellar evolution variable of interest. While *HNNI* has been demonstrated to work on the MIST catalog, the method itself is general.

Both the machine-learning based surrogate models and HNNI are developed in [Maltsev et al. 2024](https://ui.adsabs.harvard.edu/abs/2024A%26A...681A..86M/abstract).

## **Package requirements:**
The following Python packages are required to run these Notebooks:

*stellar-evolution-emulator-fitted-models.ipynb*:
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
- matplotlib

## **Stellar evolution catalog data:**
The *stellar-evolution-emulator-fitted-models.ipynb* Notebook runs without the need to access any stellar evolution catalog data base. In order to make predictions of stellar evolution tracks, the pre-trained models stored in the "/models/..." directory need to be loaded instead.

The *HNNI* algorithm requires access to the stellar evolution catalog data base. In the *HNNI.ipynb* Notebook, we use the MIST catalog. Due to file size limitations on GitHub, we have not uploaded the relevant catalog data into this repository. In order to reproduce the results and plots in the Notebook, you will need to proceed as follows:
1. download the MIST EEP tracks for v/vcrit=0.0 and [Fe/H]=+0.00 from the [MIST packaged model grid data base](https://waps.cfa.harvard.edu/MIST/model_grids.html#eeps). Verify that the downloaded directory is "Fe-H0.0vvcrit0.0".
2. After you git clone this repository, move the downloaded MIST EEP files into the "data/MIST" directory.
3. Furthermore, you will also need to create and download additional EEP tracks for the same parameters using the [MIST Web Interpolator](https://waps.cfa.harvard.edu/MIST/interp_tracks.html), for two lists of (ZAMS) masses: those listed in the "data/name-massWebInt.xlsx" and in the "data/name-massTest.xlsx" files. These will be used as additional catalog data and as test data, respectively.
4. Integrate these three data sets into the "data/MIST" directory.
   
However, instead of reproducing the MIST example you might also want to directly proceed with your own stellar evolution catalog data base. In that case, 
1. Modify the data directory path in the *HNNI_routines.py*,
2. Either modify the MIST_data_reader() function (defined in *processing_and_plot_routines.py* script) for reading in your catalog data set,
   or replace cell 20 in the Notebook altogether by your own wrapper function for reading in your data set.
3. For compatibility with the scripts used here, make sure your catalog data is casted into the data frame format as the *catalog_data* dictionary in the Notebook example, 

## Questions:**
Contact me if you have any questions or something does not work: kiril.maltsev@h-its.org
