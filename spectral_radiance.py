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

# for numerical computation
res = 1e4  # resolution for numerical integration
tol = 1e-4  # convergence tolerance
max_iter = 1000  # maximum number of iterations
relaxation = 0.3  # decrease in case of convergence problems

# physical constants
H = 6.62607015e-34  # J s
C = 299792458  # m/s
KB = 1.38064852e-23  # J/K, Boltzmann constant

############################
# Calculation
############################

def integral(x_min, x_max, eps):
    dx = (x_max - x_min) / res
    x = np.arange(x_min + dx/2, x_max + dx/2, dx)
    val = (eps * x**3/ (np.exp(x) - 1) * dx).sum()
    return val

x = lambda lmbd, t: H * C / (KB * t * lmbd)

t2 = t1
dt = 1 + tol
i = 0
integral_1 = integral(x(l2, t1), x(l1, t1), eps1)

converged = True
while dt > tol:
    integral_2 = integral(x(l2, t2), x(l1, t2), eps2)
    t2_new = t1 * (integral_1 / integral_2) ** 0.25
    dt = abs(t2 - t2_new)
    t2_new = t2* (1-relaxation) + t2_new * relaxation  # relaxation
    t2 = t2_new
    i += 1
    if i > max_iter:
        print("maximum number of iterations exceeded.")
        converged = False
        break
    print(f"Iteration {i}: T = {t2:.3f} K")

if converged:
    print(f"\nTemperature with Emissivity {eps2}: \t{t2:.3f} K")
