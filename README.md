# marmofMRI

This repository contains different tools for the preprocessing of small animal fMRI (rodents, marmosets, ...), in particular resting state data.

Many tools exist for the analysis of human brain fMRI, but they often cannot be used directly on small animals fMRI, due to different image resolution and more important deformations of EPI under higher magnetic field. 

This repository is intended to support the processing performed with common tools such as SPM, FSL, ANTs and ITK-Snap. The project is currently under further development in order to be less dependent on other softwares. 

Before using marmofMRI, your resting state fMRI data must be processed in SPM or FSL: to this purpose, we propose the batch file 'preproc_fmri_marmo.mat' to be launche in SPM. The batch performs slice timing, realignement and smoothing. Skull stripping must also be previously performed. We suggest PCNN3D algorithm published by "Chou et al., Robust automatic rodent brain extraction using 3-D pulse-coupled neural networks (PCNN). IEEE Trans Image Process. 2011 Sep;20(9):2554-64".

The main script first applies a band pass filter based on user-defined cut-off frequencies. The obtained image is very noisy so the resting state mean image is added to all volumes in order to recover brain anatomy. 

The obtained, filtered image is later used in order to compute the mean timecourse of any given ROI. This is intended to be used for later ROI-to-voxel Seed-Based analysis (for example in FSL Feat).

The filtered image can also be used to find functional networks through Independent Component Analysis (ICA). Melodic FLS can be used to this purpose.


# Dependencies

	SPM12
	nibabel
	anstpy

# Usage

Before launching the main script, please be sure the following preprocessing have been performed:

- Preprocess your data by launching in SPM the proposed batch 'preproc_fmri_marmo.mat'
- Perform skull-stripping (e.g. with PCNN3D) on the mean image computed by SPM (called meanaYourData.nii) and save the obtained mask as 'meanaYourData_mask.nii'
- Segment (for example in ITK-snap) the ROI you want to use for Seed Based analysis and place it in a subfolder called ROI

Finally you can define your 'datapath' in the script 'main.py' and launch it.
