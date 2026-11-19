# Central Tendancy of R Pixel Channel Data for Experiment A with Alcorns
import statistics
from numpy import mean

Alcorns1_number_list = [0.8, 0.8, 0.79]
avg = mean(Alcorns1_number_list)
print("The average of List is ", round(avg, 1))

r_pixel_data1 = [0.8, 0.8, 0.79]

x = statistics.mean(r_pixel_data1)

print(x)

y = statistics.mode(r_pixel_data1)

print(y)

z = statistics.median(r_pixel_data1)

print(z)

v = statistics.variance(r_pixel_data1)

print(v)