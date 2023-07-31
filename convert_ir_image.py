import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
import spectral_radiance

############################
# Input
############################

spectral_radiance.l1 = 8e-6  # min. wavelength of measurement device [m]
spectral_radiance.l2 = 14e-6  # max. wavelength of measurement device [m]
spectral_radiance.eps1 = 0.95  # emissivity of measurement

# new emissivity (may be a function of temperature)
def eps2(T):  # This may be temperature dependent
    T -= 273.15  # using °C in the definition
    # from Literature
    if T < 150:
        return 0.35
    elif T < 250:
        return 0.35 + (T-150)/100 *0.05
    elif T < 350:
        return 0.4 + (T-250)/100 * 0.1
    elif T < 450:
        return 0.5 + (T-350)/ 100 * 0.2
    elif T < 500:
        return 0.7 + (T-450) / 50 * 0.05
    else:
        return 0.65 +.1
spectral_radiance.eps2 = eps2

# Temperature range
T_min = 273  # Kelvin
T_max = 773  # Kelvin

# for numerical computation, change in case of convergence issues
spectral_radiance.res = 1e4  # resolution for numerical integration
spectral_radiance.tol = 1e-2  # convergence tolerance
spectral_radiance.max_iter = 10000  # maximum number of iterations
spectral_radiance.relaxation = 0.1  # decrease in case of convergence problems

############################
# Calculation
############################
# load measurement data
measurement_raw = np.loadtxt("./img_0130.csv", delimiter=";")
measurement_raw += 273.15  # convert to Kelvin

# pre-compute temperature mapping
temp_conversion = {}
temp_emissivity = {}
for t_raw in np.linspace(T_min, T_max, T_max - T_min + 1):
    print(f"pre-computing conversion for T = {t_raw} K")
    t_new, eps = spectral_radiance.compute_temperature(t_raw)
    temp_conversion.update({round(t_raw): round(t_new)})
    temp_emissivity.update({round(t_raw): eps})

# convert measurement values
measurement_raw_flat = measurement_raw.flatten()
measurement_adj = np.zeros(measurement_raw_flat.shape)
new_emissivity = np.zeros(measurement_raw_flat.shape)
for i in range(len(measurement_raw_flat)):
    print(f"Processing point {i + 1} of {len(measurement_raw_flat)}")
    measurement_adj[i] = temp_conversion[round(measurement_raw_flat[i])]  # TODO replace with linear interpolation to get higher resolution
    new_emissivity[i] = temp_emissivity[round(measurement_raw_flat[i])]
measurement_adj = measurement_adj.reshape(measurement_raw.shape)
new_emissivity = new_emissivity.reshape(measurement_raw.shape)

# plot
fig1, ax1 = plt.subplots()
ax1.axis('off')
line = ax1.imshow(measurement_raw - 273.15, extent=[1,measurement_raw.shape[1],1,measurement_raw.shape[0]], cmap='jet', aspect='equal')
divider = make_axes_locatable(ax1)
cax = divider.append_axes("right", size="5%", pad=0.05)
fig1.colorbar(line, cax=cax)
ax1.set_title(f"As recorded (eps = {spectral_radiance.eps1})")

fig2, ax2 = plt.subplots()
ax2.axis('off')
line = ax2.imshow(measurement_adj - 273.15, extent=[1,measurement_raw.shape[1],1,measurement_raw.shape[0]], cmap='jet', aspect='equal')
divider = make_axes_locatable(ax2)
cax = divider.append_axes("right", size="5%", pad=0.05)
fig2.colorbar(line, cax=cax)
ax2.set_title("Adjusted emissivity")

plt.show()
