import numpy as np

############################
# Input
############################

# measurement specific
t1 = 485.4  # measured temperature [K]
eps1 = 1  # emissivity during measurement [-]
eps2 = 0.8  # new emissivity [-]
# wavelength range of device
l1 = 2e-6  # min. wavelength  [m]
l2 = 2.6e-6  # max. wavelength [m]

# physical constants
H = 6.62607015e-34  # J s
C = 299792458  # m/s
KB = 1.38064852e-23  # J/K, Boltzmann constant

############################
# Calculation
############################

l_mean = (l1 + l2) / 2
C2 = H*C/KB
t2 = t1 / (1 + t1 * l_mean / C2 * np.log(eps2 / eps1))
print(f"\nTemperature with Emissivity {eps2}: \t{t2:.3f} K")
