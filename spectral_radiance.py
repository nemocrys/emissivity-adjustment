import numpy as np
import matplotlib.pyplot as plt

############################
# Input
############################

# measurement specific
t1 = 160+273.15  # measured temperature [K]
eps1 = 0.95  # emissivity during measurement [-]

def eps2(T):  # This may be temperature dependent
    return .5
    # T -= 273.15  # using °C in the definition
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

# fig, ax = plt.subplots()
# T = np.linspace(273.15, 873.15)
# eps2_T = []
# for t in T:
#     eps2_T.append(eps2(t))
# ax.plot(T - 273.15, eps2_T)
# ax.set_xlabel("Temperature [°C]")
# ax.set_ylabel("Emissivity [-]")
# plt.show()

# wavelength range of device
l1 = 8e-6  # min. wavelength  [m]
l2 = 14e-6  # max. wavelength [m]

# for numerical computation
res = 1e4  # resolution for numerical integration
tol = 1e-2  # convergence tolerance
max_iter = 10000  # maximum number of iterations
relaxation = 0.1  # decrease in case of convergence problems

# physical constants
H = 6.62607015e-34  # J s
C = 299792458  # m/s
KB = 1.38064852e-23  # J/K, Boltzmann constant

############################
# Calculation
############################

f1 = C/l2
f2 = C/l1

def integral(f_min, f_max, eps, t):
    df = (f_max - f_min) / res
    f = np.arange(f_min + df/2, f_max + df/2, df)
    val = (eps * 2 * H * f**3 / C**2 / (np.exp(H*f / (KB * t)) - 1) * df).sum()
    return val

def compute_temperature(t1, print_=False):
    """Compute temperature with changed emissivity"""
    t2 = t1
    dt = 1 + tol
    i = 0
    integral_1 = integral(f1, f2, eps1, t1)

    converged = True
    while dt > tol:
        integral_2 = integral(f1, f2, eps2(t2), t2)
        t2_new = t2 * (integral_1 / integral_2)
        dt = abs(t2 - t2_new)
        t2_new = t2* (1-relaxation) + t2_new * relaxation  # relaxation
        t2 = t2_new
        i += 1
        if i > max_iter:
            print("maximum number of iterations exceeded.")
            converged = False
            return np.nan
        if print_:
            print(f"Iteration {i}: T = {t2:.3f} K")
    if print_:
        print(f"\nTemperature with Emissivity {eps2(t2)}: \t{t2:.3f} K")
        print(f"\nTemperature with Emissivity {eps2(t2)}: \t{t2 - 273.15:.3f}°C")
    return t2, eps2(t2)

if __name__ == "__main__":
    compute_temperature(t1, print_=True)
