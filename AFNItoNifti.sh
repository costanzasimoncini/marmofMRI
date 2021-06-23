
marmoset="MarmoT1.nii"
outputname="brain"

# Convert nii.gz to nii


3dSkullStrip -input marmoset -prefix outputname -marmoset -orig_vol

3dAFNItoNIFTI $outputname+orig.HEAD
