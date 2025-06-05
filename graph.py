import time
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
from decimal import Decimal, getcontext


# Function to benchmark (assumed to be provided)
def func1(precision):
    # Example implementation (replace with actual function)
    # This is a dummy function for demonstration
    getcontext().prec = precision

    # Chudnovsky algorithm
    C = 426880 * Decimal(10005).sqrt()
    M = 1
    L = 13591409
    X = 1
    K = 6
    S = L
    for i in range(1, precision):
        M = (K**3 - 16 * K) * M // i**3
        L += 545140134
        X *= -262537412640768000
        S += Decimal(M * L) / X
        K += 12

    pi = C / S
    return str(pi)


# Benchmark different precisions
precisions = [10, 20, 50, 100, 200, 500, 1000]  # , 2000, 5000]
times = []
for p in precisions:
    start = time.perf_counter()
    func1(p)
    elapsed = time.perf_counter() - start
    times.append(elapsed)
    print(f"Precision: {p}, Time: {elapsed:.4f} seconds")

# Save results to Excel
df = pd.DataFrame({"Precision": precisions, "Time": times})
df.to_excel("timing_results.xlsx", index=False)

# Plot precision vs time
plt.figure()
plt.plot(df["Precision"], df["Time"], "bo-")
plt.xlabel("Precision")
plt.ylabel("Time (seconds)")
plt.title("Precision vs Execution Time")
plt.grid(True)
plt.savefig("precision_vs_time.png")
plt.close()


# Define models for fitting
def linear_model(x, a, b):
    return a * x + b


def quadratic_model(x, a, b, c):
    return a * x**2 + b * x + c


def cubic_model(x, a, b, c, d):
    return a * x**3 + b * x**2 + c * x + d


def exponential_model(x, a, b):
    return a * np.exp(b * x)


def power_model(x, a, b):
    return a * x**b


def logarithmic_model(x, a, b):
    return a + b * np.log(x)


models = [
    ("Linear", linear_model),
    ("Quadratic", quadratic_model),
    ("Cubic", cubic_model),
    ("Exponential", exponential_model),
    ("Power", power_model),
    ("Logarithmic", logarithmic_model),
]

# Fit models and find the best one
x = df["Precision"].values
y = df["Time"].values
best_r_squared = -np.inf
best_model_info = None

for name, model in models:
    try:
        params, _ = curve_fit(model, x, y, maxfev=10000)
        y_pred = model(x, *params)
        ss_res = np.sum((y - y_pred) ** 2)
        ss_tot = np.sum((y - np.mean(y)) ** 2)
        r_squared = 1 - (ss_res / ss_tot)
        print(f"{name} R-squared: {r_squared:.4f}")
        if r_squared > best_r_squared:
            best_r_squared = r_squared
            best_model_info = (name, model, params)
    except Exception as e:
        print(f"Failed to fit {name}: {e}")

# Output best model and plot fit
if best_model_info is not None:
    best_name, best_model, best_params = best_model_info
    equation = ""
    if best_name == "Linear":
        equation = f"y = {best_params[0]:.4f}x + {best_params[1]:.4f}"
    elif best_name == "Quadratic":
        equation = (
            f"y = {best_params[0]:.4f}x² + {best_params[1]:.4f}x + {best_params[2]:.4f}"
        )
    elif best_name == "Cubic":
        equation = f"y = {best_params[0]:.4f}x³ + {best_params[1]:.4f}x² + {best_params[2]:.4f}x + {best_params[3]:.4f}"
    elif best_name == "Exponential":
        equation = f"y = {best_params[0]:.4f}e^{{{best_params[1]:.4f}x}}"
    elif best_name == "Power":
        equation = f"y = {best_params[0]:.4f}x^{{{best_params[1]:.4f}}}"
    elif best_name == "Logarithmic":
        equation = f"y = {best_params[0]:.4f} + {best_params[1]:.4f}ln(x)"

    print(f"\nBest fitting model: {best_name} with R-squared {best_r_squared:.4f}")
    print(f"Best fit equation: {equation}")

    # Plot best fit
    plt.figure()
    plt.plot(x, y, "bo", label="Data")
    x_fit = np.linspace(min(x), max(x), 500)
    y_fit = best_model(x_fit, *best_params)
    plt.plot(x_fit, y_fit, "r-", label=f"Best Fit: {best_name}")
    plt.xlabel("Precision")
    plt.ylabel("Time (seconds)")
    plt.title("Precision vs Time with Best Fit Model")
    plt.legend()
    plt.grid(True)
    plt.savefig("best_fit_model.png")
    plt.close()
else:
    print("No suitable model found.")
