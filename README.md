# marmofMRI

This repository contains different tools for the preprocessing of small animal (rodents, marmosets, ...) fMRI, in particular resting state data.

Many tools exist for the analysis of human brain fMRI, but they often cannot be used directly on small animals fMRI, due to different image resolution and more important deformations of EPI under higher magnetic field. 

This repository is intended to support the processing performed with common tools such as SPM, FSL, ANTs and ITK-Snap. The project is currently under further development in order to be less dependent on other softwares. 


# Dependencies

	SPM
	FSL
	nibabel
	anstpy

# Usage

Resting state fMRI data must be previously processed in SPM or FSL. Users can run in SPM the proposed batch file 'preproc_fmri_marmo.mat' which performs slice timing, realignement and smoothing. Skull stripping must also be previously performed. We suggest PCNN3D algorithm published by "Chou et al., Robust automatic rodent brain extraction using 3-D pulse-coupled neural networks (PCNN). IEEE Trans Image Process. 2011 Sep;20(9):2554-64".

Principal files to be launched are 'bandpassfilter_recoverbrain.py' and 'compute_regressors_for_seed_based.py'.
The first one applies a band pass filter based on user-defined cut-off frequencies. The obtained image is very noisy so the resting state mean image is added to all volumes in order to recover brain anatomy. 

The obtained, filtered image can be used in Melodic FSL in order to find functional networks through  Independent Component Analysis (ICA). 
 
The obtained, filtered image can also be used in the 'compute_regressors_for_seed_based.py' file in order to compute the mean timecourse of any given ROI. This is intended to be used for later ROI to voxel Seed-Based analysis (for example in FSL Feat).