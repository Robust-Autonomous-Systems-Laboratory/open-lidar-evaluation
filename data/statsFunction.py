import csv
import glob
import math
import statistics
import numpy as np
from scipy import stats


def calculateStatistics(filepath):

    points_on_target = []
    values = []
    trial_means = []
    
    for file in glob.glob(filepath):
       
        trial_values = []
        # load each file
        with open(file, 'r', newline='') as csvfile:
            reader = csv.reader(csvfile)

            # iterate over each row in the file, append number of pts on target per scan
            for row in reader:
                points_on_target.append(len(row))

                # append range of each point in a scan
                for i in enumerate(row):
                    values.append(float(row[i[0]]))
                    trial_values.append(float(row[i[0]]))

        # trial stats:
        trial_means.append(statistics.mean(trial_values))

    range = max(values)- min(values)
    pstdev = statistics.pstdev(values)
    mean = statistics.mean(values)
    mean_pts = statistics.mean(points_on_target)

    bins = np.arange(min(values), max(values) + pstdev, pstdev)

    # 95% confidence interval
    n = len(trial_means)
    SE = statistics.stdev(trial_means) / math.sqrt(n) # standard error

    t_score = stats.t.ppf((1 + 0.95) / 2, df=n-1)
    ME = t_score * SE # margin of error
    lower_bound = mean - ME
    upper_bound = mean + ME

    # pmf weights
    weights = np.ones_like(values) / len(values) 

    return {"values": values, 
            "mean": mean, 
            "pstdev": pstdev,
            "range": range,
            "mean_pts": mean_pts,
            "bins": bins,
            "weights": weights,
            "lower_bound": lower_bound,
            "upper_bound": upper_bound,
            "n_trials": n}
