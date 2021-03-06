import scipy
import subprocess
import numpy as np
from scipy import interpolate
from matplotlib import pyplot as plt

figs = (
     ( # Fig1: Qsort vs random qsort on decreasing samples
         "decreasing_issue",
         (["-qrd", "0", "500_000", "50_000", "24"], 
          "Quicksort (pivot = random)", "g"),
         (["-qud", "0", "500_000", "50_000", "24"], 
          "Quicksort (pivot = last)", "r"),
     ),
     ( # Fig2: native qsort vs qsortg vs qsort random
         "native_and_polymorphism",
         (["-qr", "0", "50_000_000", "5_000_000", "24"], 
          "Quicksort on u32", "g"),
         (["-qc", "0", "50_000_000", "5_000_000", "24"], 
          "Native polymorph quicksort", "b"),
         (["-qg", "0", "50_000_000", "5_000_000", "24"], 
          "Handmade polymorph quicksort", "r"),
     ),
     ( # Fig3: radixsort in different basis
         "radixsort_basis",
         (["-rx", "0", "50_000_000", "5_000_000", "24", "2"], 
          "Radixsort, basis $2^2$", "aqua"),
         (["-rx", "0", "50_000_000", "5_000_000", "24", "3"], 
          "Radixsort, basis $2^3$", "green"),
         (["-rx", "0", "50_000_000", "5_000_000", "24", "4"], 
          "Radixsort, basis $2^4$", "purple"),
         (["-rx", "0", "50_000_000", "5_000_000", "24", "6"], 
          "Radixsort, basis $2^6$", "slategrey"),
         (["-rx", "0", "50_000_000", "5_000_000", "24", "8"], 
          "Radixsort, basis $2^8$", "blue"),
         (["-rx", "0", "50_000_000", "5_000_000", "24", "12"], 
          "Radixsort, basis $2^{12}$", "magenta"),
         (["-rx", "0", "50_000_000", "5_000_000", "24", "24"], 
          "Radixsort, basis $2^{24}$", "black"),
         (["-cs", "0", "50_000_000", "5_000_000", "24"], 
          "Counting sort", "red"),
     ),
     ( # Fig4: qsort vs radixsort vs counting sort
         "comparison",
         (["-qr", "0", "500_000_000", "50_000_000", "24"], 
          "Quicksort on u32", "g"),
         (["-rx", "0", "500_000_000", "50_000_000", "24", "8"], 
          "Radixsort", "b"),
         (["-cs", "0", "500_000_000", "50_000_000", "24"], 
          "Counting sort", "r"),
     ),
     ( # Fig5: qsort vs radixsort vs counting sort on small arrays
        "small_comparison",
        (["-qr", "0", "100_000", "5_000", "24"], 
         "Quicksort on u32", "g"),
        (["-rx", "0", "100_000", "5_000", "24", "8"], 
         "Radixsort", "b"),
        (["-cs", "0", "100_000", "5_000", "24"], 
         "Counting sort", "r"),
    ),

)

# Plot performance chart and export it to a png
def plot_performances(option, name, color):
    xi, yi = [], [] # x and y data for the chart
    option = [o.replace("_", "") for o in option]
    out = subprocess.check_output(["./out"] + option)
    # Parsing data
    for line in out.splitlines():
        # Decoding data from a single line
        line = line.decode("utf-8")
        print(line)
        data = line.split()
        # Getting x and y values
        x = int(data[-2][:-1])
        y = float(data[-1])
        xi.append(x)
        yi.append(y)
    # Plotting and interpolation
    xnew = np.linspace(0, max(xi), 1000)
    p = interpolate.interp1d(xi, yi, kind='cubic') # Cubic polynomial interp.
    plt.plot(xi, yi, "o", color=f"{color}", label=name)
    plt.plot(xnew, p(xnew), color=f"{color}")

if __name__ == "__main__":
    print("Cleaning project...")
    subprocess.call(["make", "clean"])
    
    print("Building project...")
    subprocess.call("make")
    
    print("Plotting performances...")
    for fig in figs:
        plt.clf()
        plt.cla()
        print("Processing fig...")
        for option in fig[1:]:
            print(f"Plotting \"{option[1]}\"...")
            plot_performances(*option)
        # format
        plt.ticklabel_format(style='sci', axis='x', scilimits=(0,0))
        plt.ylabel("Runtime (sec)")
        plt.xlabel("Array size")
        plt.legend(loc="best")
        plt.savefig(f"{fig[0]}.png")
        print("Fig done.")

