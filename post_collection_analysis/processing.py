from statsFunction import calculateStatistics
import matplotlib.pyplot as plt
import os

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
data_dir = os.path.join(parent_dir, "repeatability_processing", "data")

# For comparison between lidar, point to same experiment and target range to select all extracted point CSVs
# Note: This is only an example and must be configured to match your own extracted data from the ROS pipeline!
lidarA_dir = os.path.join(data_dir, "experiment/lidarA/distance1/*.csv")
lidarB_dir = os.path.join(data_dir, "experiment/lidarB/distance1/*.csv")
lidarC_dir = os.path.join(data_dir, "experiment/lidarC/distance1/*.csv")
lidarD_dir = os.path.join(data_dir, "experiment/lidarD/distance1/*.csv")

# process all range data to calc stats from the specific experiment and target range
lidarA = calculateStatistics(lidarA_dir)
lidarB = calculateStatistics(lidarB_dir)
lidarC = calculateStatistics(lidarC_dir)
lidarD = calculateStatistics(lidarD_dir)

# print all stats from function call
print("Lidar,  Overall Mean,  Overall Pop. Stddev,  Mean Pts on Target, n_trials,  t-test 95% CI Bounds, Margin of Error")
print(f"lidarA - {lidarA['mean']:.4f}, {lidarA['pstdev']:.4f}, {lidarA['mean_pts']:.4f}, {lidarA['n_trials']}, ({lidarA['lower_bound']:.4f}, {lidarA['upper_bound']:.4f}), {lidarA['margin_error']:.4f}")
print(f"lidarB - {lidarB['mean']:.4f}, {lidarB['pstdev']:.4f}, {lidarB['mean_pts']:.4f}, {lidarB['n_trials']}, ({lidarB['lower_bound']:.4f}, {lidarB['upper_bound']:.4f}), {lidarB['margin_error']:.4f}")
print(f"lidarC - {lidarC['mean']:.4f}, {lidarC['pstdev']:.4f}, {lidarC['mean_pts']:.4f}, {lidarC['n_trials']}, ({lidarC['lower_bound']:.4f}, {lidarC['upper_bound']:.4f}), {lidarC['margin_error']:.4f}")
print(f"lidarD - {lidarD['mean']:.4f}, {lidarD['pstdev']:.4f}, {lidarD['mean_pts']:.4f}, {lidarD['n_trials']}, ({lidarD['lower_bound']:.4f}, {lidarD['upper_bound']:.4f}), {lidarD['margin_error']:.4f}")

# plotting pmfs
plt.hist(lidarA['values'], label='lidarA clear 25m', color='red', bins=lidarA['bins'], weights=lidarA['weights'], histtype='stepfilled', alpha=0.5)
plt.hist(lidarB['values'], label='lidarB clear 25m', color='orange', bins=lidarB['bins'], weights=lidarB['weights'], histtype='stepfilled', alpha=0.5)
plt.hist(lidarC['values'], label='lidarC clear 25m', color='green', bins=lidarC['bins'], weights=lidarC['weights'], histtype='stepfilled', alpha=0.5)
plt.hist(lidarD['values'], label='lidarD clear 25m', color='blue', bins=lidarD['bins'], weights=lidarD['weights'], histtype='stepfilled', alpha=0.5)

plt.xlabel('Range')
plt.ylabel('Probability')
plt.legend()
plt.show()
