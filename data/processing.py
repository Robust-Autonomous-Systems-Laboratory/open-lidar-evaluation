from statsFunction import calculateStatistics
import matplotlib.pyplot as plt

# REPLACE WITH RELATIVE FILEPATHS TO PACKAGE ROOT
velodyne = calculateStatistics("/home/quin/sensor_ws/src/repeatability_processing/data/velodyne/clear/25m/lot24/*.csv")
ouster = calculateStatistics("/home/quin/sensor_ws/src/repeatability_processing/data/ouster/clear/25m/lot24/*.csv")
iris = calculateStatistics("/home/quin/sensor_ws/src/repeatability_processing/data/iris/clear/25m/lot24/*.csv")
ruby = calculateStatistics("/home/quin/sensor_ws/src/repeatability_processing/data/ruby/clear/25m/lot24/*.csv")

# ------------------------------------------------
# print all stats from function call

print("Lidar,  Overall Mean,  Overall Pop. Stddev,  Mean Pts on Target, n_trials,  t-test 95% CI Bounds")
print(f"Velodyne - {velodyne['mean']:.4f}, {velodyne['pstdev']:.4f}, {velodyne['mean_pts']:.4f}, {velodyne['n_trials']}, ({velodyne['lower_bound']:.4f}, {velodyne['upper_bound']:.4f})")
print(f"Ouster - {ouster['mean']:.4f}, {ouster['pstdev']:.4f}, {ouster['mean_pts']:.4f}, {ouster['n_trials']}, ({ouster['lower_bound']:.4f}, {ouster['upper_bound']:.4f})")
print(f"Ruby - {ruby['mean']:.4f}, {ruby['pstdev']:.4f}, {ruby['mean_pts']:.4f}, {ruby['n_trials']}, ({ruby['lower_bound']:.4f}, {ruby['upper_bound']:.4f})")
print(f"Iris - {iris['mean']:.4f}, {iris['pstdev']:.4f}, {iris['mean_pts']:.4f}, {iris['n_trials']}, ({iris['lower_bound']:.4f}, {iris['upper_bound']:.4f})")


# ------------------------------------------------
# plotting pmfs
plt.hist(ouster['values'], label='Ouster clear 25m', color='orange', bins=ouster['bins'], weights=ouster['weights'], histtype='stepfilled', alpha=0.5)
plt.hist(ruby['values'], label='Ruby clear 25m', color='blue', bins=ruby['bins'], weights=ruby['weights'], histtype='stepfilled', alpha=0.5)
plt.hist(velodyne['values'], label='Velodyne clear 25m', color='red', bins=velodyne['bins'], weights=velodyne['weights'], histtype='stepfilled', alpha=0.5)
plt.hist(iris['values'], label='Iris clear 25m', color='green', bins=iris['bins'], weights=iris['weights'], histtype='stepfilled', alpha=0.5)
plt.xlabel('Range')
plt.ylabel('Probability')
plt.legend()
plt.show()

