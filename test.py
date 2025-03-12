from matplotlib import pyplot as plt
from pydicom import dcmread
import numpy as np

ds = dcmread('/Users/Micah/Documents/2025-02-21_SM_W072115116/2025-02-21_SM_W072115116.CT.PET_1_SANDERSMEDICAL_(ADULT).0003.0006.2025.02.21.16.22.25.351987.923785634.IMA')

# print(ds.pixel_array.shape)
print(ds)
# print(ds.pixel_array.sum())

# np.savetxt("output.txt", ds.pixel_array, delimiter=" ", fmt="%d")

# Plot image
# plt.imshow(ds.pixel_array, cmap="gray")
# plt.show()