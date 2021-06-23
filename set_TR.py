import nibabel as nb

folder = "/Users/costanza/workspace/PROJETS/fMRI_marmo/210607_02_Josette3M/RestingState/"
imname = "sraRSJos3M"
suffix = ".nii"

# DEFINE NEW TR
TR = 2.0

filepath = "/Users/costanza/workspace/PROJETS/fMRI_marmo/210607_02_Josette3M/RestingState/sraRSJos3M.nii"
filepath_newTR = filepath[:filepath.find(".")] + "TR" + str(TR) + ".nii"
filename = folder + imname + suffix
img = nb.load(filename)

data = img.get_fdata()
hd = img.header
affine = img.affine
zooms = hd.get_zooms()[:3] + (TR,)
print(zooms)
hd.set_zooms(zooms)

newim = nb.Nifti1Image(data, affine, hd)
nb.save(newim, filepath_newTR)

# img.__class__(data, affine, hd)
# img.to_filename(filepath_newTR)