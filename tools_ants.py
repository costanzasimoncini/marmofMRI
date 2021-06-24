import ants
import numpy as np

def ch_pxdim_to_human_sizeAnts(img, factor):
    sp = ants.get_spacing(img)[:3]
    new_sp = tuple([s * factor for s in sp])

    if len(ants.get_spacing(img)) > 3 :
        TR = ants.get_spacing(img)[3]
        print(TR)
        new_sp = new_sp + (TR,)

    ants.set_spacing(img, new_sp)
    return img