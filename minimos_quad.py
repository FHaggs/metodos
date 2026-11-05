import numpy as np
import sympy as sp

# Dados
x_vals = np.array([0, 1, 2, 3, 4, 5], dtype=float)
y_vals = np.array([64.678, 65.028, 70.521, 52.127, 41.078, 47.316], dtype=float)

# Monta a matriz A com colunas: x^3, x^2, x, 1
A = np.vstack([x_vals**3, x_vals**2, x_vals, np.ones_like(x_vals)]).T

# Resolve o sistema: A.T @ A c = A.T @ y
ATA = A.T @ A
ATy = A.T @ y_vals
coeffs = np.linalg.solve(ATA, ATy)

a, b, c, d = coeffs
x = sp.Symbol('x')
poly = a*x**3 + b*x**2 + c*x + d

sp.pprint(sp.expand(poly), use_unicode=True)

