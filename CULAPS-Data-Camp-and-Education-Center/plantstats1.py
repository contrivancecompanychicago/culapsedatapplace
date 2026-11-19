# Central Tendancy of R Pixel Channel Data for Experiment B with Alcorns
import statistics
from numpy import mean

Alcorns2_number_list = [0.212, 0.220, 0.220]
avg = mean(Alcorns2_number_list)
print("The average of List is ", round(avg, 1))

r_pixel_data2 = [0.212, 0.220, 0.220]

x = statistics.mean(r_pixel_data2)

print(x)

y = statistics.mode(r_pixel_data2)

print(y)

z = statistics.median(r_pixel_data2)

print(z)

v = statistics.variance(r_pixel_data2)

print(v)