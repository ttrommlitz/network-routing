# Size 1,000,000:
# Heap: 23.951926s
# Heap: 24.627461s
# Heap: 26.039794s
# Heap: 25.871552s
# Heap: 26.539010s

# Size 100,000: 
# Array: 253.673946s, Heap: 1.252837s. Heap is 202.480 times faster.
# Array: 256.743401s, Heap: 1.277287s. Heap is 201.007 times faster.
# Array: 269.162827s, Heap: 1.314397s. Heap is 204.780 times faster.
# Array: 257.996284s, Heap: 1.358808s. Heap is 189.870 times faster.
# Array: 255.431740s, Heap: 1.263468. Heap is 202.167 times faster. 

# Size 10,000:
# Array: 2.604941s, Heap: .077565s. Heap is 33.584 times faster.
# Array: 2.544218s, Heap: .075005s. Heap is 33.921 times faster.
# Array: 2.543854s, Heap: .075542s. Heap is 33.675 times faster.
# Array: 2.557218s, Heap: .074479s. Heap is 34.335 times faster.
# Array: 2.547877s, Heap: 0.075162s. Heap is 33.898 times faster.

# Size 1,000:
# Array: .057296s, Heap: .006839s. Heap is 8.378 times faster.
# Array: .058019s, Heap: .007078s. Heap is 8.197 times faster.
# Array: .056947s, Heap: .007024s. Heap is 8.107 times faster.
# Array: .055730s, Heap: .006975s. Heap is 7.990 times faster.
# Array: .054304s, Heap: .006921s. Heap is 7.846 times faster.

#Size 100:
# Array: .001574s, Heap: .001165s. Heap is 1.351 times faster.
# Array: .001588s, Heap: .001401s. Heap is 1.133 times faster.
# Array: .001780s, Heap: .001422s. Heap is  1.252 times faster.
# Array: .001658s, Heap: .001358s. Heap is 1.221 times faster.
# Array: .001609s, Heap: .001321s. Heap is 1.218 times faster.

x_vals = [100, 1000, 10000, 100000, 1000000]
# array_times is the average of the 5 array times for each size
# heap_times is the average of the 5 heap times for each size
array_times = [.001642, .056459, 2.559622, 262.880838, 26373.186639] # estimate is 26373.186639
heap_times = [.001333, .006967, .075551, 1.293359, 25.405949]

import matplotlib.pyplot as plt
import numpy as np

coef = np.polyfit(x=x_vals, y=array_times, deg=2)
x = np.linspace(100, 1000000, 1000)
y = coef[0] * x ** 2 + coef[1] * x + coef[2]

fig, (ax1, ax2) = plt.subplots(1, 2)
fig.suptitle('Empirical Analysis of Dijkstra\'s Algorithm')
ax1.scatter(x_vals, array_times)
ax1.set_xscale('log')
ax1.set_title('Array PQueue Analysis')

ax2.scatter(x_vals, heap_times)
ax2.set_xscale('log')
ax2.set_title('Heap PQueue Analysis')

for ax in [ax1, ax2]:
    ax.set_xlabel('Number of nodes (|V|)')
    ax.set_ylabel('Average Time to run Djikstra\'s Algorithm (sec)')

plt.show()