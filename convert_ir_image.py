import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
import spectral_radiance

spectral_radiance.eps1 = 0.95  # Emissivity of measurement
def eps2(T):  # This may be temperature dependent
    T -= 273.15  # using °C in the definition

    # from Literature
    # if T < 150:
    #     return 0.35
    # elif T < 250:
    #     return 0.35 + (T-150)/100 *0.05
    # elif T < 350:
    #     return 0.4 + (T-250)/100 * 0.1
    # elif T < 450:
    #     return 0.5 + (T-350)/ 100 * 0.2
    # elif T < 500:
    #     return 0.7 + (T-450) / 50 * 0.05
    # else:
    #     return 0.65 +.1

    # from experiment
    if T < 100:
        return 0.84
    elif T < 107:
        return 0.84 + (T - 100) / 7 * 0.01
    elif T < 118:
        return 0.85 + (T - 107) / 11 * 0.02
    elif T < 150:
        return 0.87 + (T - 118) / 32 * 0.16
    else:
        return 1.03

def eps2_from_lit(T):
        # from Literature
    T -= 273.15  # using °C in the definition
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

fig, ax = plt.subplots()
T = np.linspace(273.15, 373.15)
eps2_T = []
for t in T:
    eps2_T.append(eps2(t))
ax.plot(T - 273.15, eps2_T, "--", color="#1f77b4")
T = np.linspace(373.15, 150 + 273.15)
eps2_T = []
for t in T:
    eps2_T.append(eps2(t))
ax.plot(T - 273.15, eps2_T, "-", color="#1f77b4", label="Bestimmt mit Sticker")
T = np.linspace(150 + 273.15, 473.15)
eps2_T = []
for t in T:
    eps2_T.append(eps2(t))
ax.plot(T - 273.15, eps2_T, "--", color="#1f77b4")

T = np.linspace(273.15, 473.15)
eps2_T = []
for t in T:
    eps2_T.append(eps2_from_lit(t))
ax.plot(T - 273.15, eps2_T, "-", color="#ff7f0e", label="Schätzung nach Literatur")

T = np.linspace(273.15, 473.15)
eps2_T = []
for t in T:
    eps2_T.append( 0.6394)
ax.plot(T - 273.15, eps2_T, "-", color="#2ca02c", label="Konstante aus Literatur")

ax.set_xlabel("Temperature [°C]")
ax.set_ylabel("Emissivity [-]")
ax.legend()
plt.show()


# def sim_eps(T):
#     if T/1685<0.593:
#         return 0.46*1.39
#     else:
#         return 0.46*(1.96-0.96*T/1685)

# fig, ax = plt.subplots()
# T = np.linspace(273.15, 1400 +273.15)
# eps2_T = []
# for t in T:
#     eps2_T.append(sim_eps(t))
# ax.plot(T - 273.15, eps2_T)
# ax.set_xlabel("Temperature [°C]")
# ax.set_ylabel("Emissivity [-]")
# plt.show()

measurement_raw = np.loadtxt("./img_0130.csv", delimiter=";")

temp_conversion = {}
temp_emissivity = {}
for t_raw in np.linspace(0, 500, 501):
    print(f"pre-computing conversion for T = {t_raw}°C")
    t_new, eps = spectral_radiance.compute_temperature(t_raw + 273.15)
    temp_conversion.update({round(t_raw): round(t_new - 273.15)})
    temp_emissivity.update({round(t_raw): eps})

measurement_raw_flat = measurement_raw.flatten()
measurement_adj = np.zeros(measurement_raw_flat.shape)
new_emissivity = np.zeros(measurement_raw_flat.shape)
for i in range(len(measurement_raw_flat)):
    print(f"Processing point {i + 1} of {len(measurement_raw_flat)}")
    measurement_adj[i] = temp_conversion[round(measurement_raw_flat[i])]
    new_emissivity[i] = temp_emissivity[round(measurement_raw_flat[i])]
measurement_adj = measurement_adj.reshape(measurement_raw.shape)
new_emissivity = new_emissivity.reshape(measurement_raw.shape)

fig1, ax1 = plt.subplots()
ax1.axis('off')
line = ax1.imshow(measurement_raw, extent=[1,measurement_raw.shape[1],1,measurement_raw.shape[0]], cmap='jet', aspect='equal')
divider = make_axes_locatable(ax1)
cax = divider.append_axes("right", size="5%", pad=0.05)
fig1.colorbar(line, cax=cax)
ax1.set_title("As recorded (eps = 0.95)")

fig2, ax2 = plt.subplots()
ax2.axis('off')
line = ax2.imshow(measurement_adj, extent=[1,measurement_raw.shape[1],1,measurement_raw.shape[0]], cmap='jet', aspect='equal')
divider = make_axes_locatable(ax2)
cax = divider.append_axes("right", size="5%", pad=0.05)
fig2.colorbar(line, cax=cax)
ax2.set_title("Adjusted T-dependent emissivity")

plt.show()
