import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
from sklearn.metrics import auc, roc_auc_score

METRIC = "euclidean_l2"
CSVNAME = f'dlib_pydeface_{METRIC}_70'   #name of the CSV to be analyzed
CSVPATH = '/Users/avnoorludhar/Desktop/uwindsor/Glendor/testingImages100x100/FinalResultsCSVs/70%CSV'  #path to the CSV
NUMOFTHRESHOLDS = 100
OUTPUT_FOLDER = '/Users/avnoorludhar/Desktop/uwindsor/Glendor/testingImages100x100/FinalResultsCSVs/PRCFinal'

data = pd.read_csv(CSVPATH + '/' + CSVNAME + '.csv')
# Convert to numpy array
scores = data.to_numpy()

# Delete the first column of labels
scores = np.delete(scores, 0, axis=1)

# Number of rows and columns
n, m = scores.shape

# Expected answer with the main diagonal all filled with 1s
expectedAns = np.zeros((n, m))
np.fill_diagonal(expectedAns, 1)

# Arrays to hold the TPR values (y), FPR values (x), precision values, and number of true positives and false positives for each threshold
tpr_list = []
num_TorF_pos = []
fpr_list = []
precision_list = []

# Creates an array of 100 evenly spaced values between 0 and 1
thresholds = np.linspace(0, 1 if METRIC == 'cosine' else 1.41, NUMOFTHRESHOLDS)

# Iterate through each threshold
for threshold in thresholds:
    # Creates an array of 1s and 0s for if the specific score is under the threshold
    predicted_labels = (scores <= threshold).astype(int)

    truePos = np.sum((predicted_labels == 1) & (expectedAns == 1))
    trueNeg = np.sum((predicted_labels == 0) & (expectedAns == 0))
    falsePos = np.sum((predicted_labels == 1) & (expectedAns == 0))
    falseNeg = np.sum((predicted_labels == 0) & (expectedAns == 1))

    # Formula for true positive rate (recall) which will be on the y-axis of our PRC graph
    truePosRate = truePos / (truePos + falseNeg + 1e-10)
    # Formula for false positive rate which will be on the x-axis
    falsePosRate = falsePos / (falsePos + trueNeg + 1e-10)
    # Formula for precision
    precision = truePos / (truePos + falsePos + 1e-10)

    # Add these data points to the arrays
    tpr_list.append(truePosRate)
    fpr_list.append(falsePosRate)
    precision_list.append(precision)
    num_TorF_pos.append((truePos, falsePos))

# calculate AUC score
auc_score = 1 - roc_auc_score(expectedAns.flatten(), scores.flatten())

#numpy arrays for all arrays calculated
tpr_list_np = np.array(tpr_list)
fpr_list_np = np.array(fpr_list)
precision_list_np = np.array(precision_list)

# determine the optimal threshold (Youden's J statistic) = max(tpr-fpr)
# however FPR stays low since there are such a huge number of non matches in the dataset
j_scores = tpr_list_np - fpr_list_np
optimal_idx = np.argmax(j_scores)
optimal_threshold_auc = thresholds[optimal_idx]

#number of true positives and false positives at the optimal threshold
number_of_true_pos = num_TorF_pos[optimal_idx][0]
number_of_false_pos = num_TorF_pos[optimal_idx][1]

# Create a figure with two subplots
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))

# Plot the ROC Curve on the first subplot
ax1.plot(fpr_list, tpr_list, marker='o', label=f'AUC = {auc_score:.4f}\nOptimal Threshold = {optimal_threshold_auc:.2f}\nTrue Positives = {number_of_true_pos}\nFalse Positives = {number_of_false_pos}')
ax1.set_xlabel('False Positive Rate')
ax1.set_ylabel('True Positive Rate')
ax1.set_title('ROC Curve for ' + CSVNAME)
ax1.grid()
ax1.legend()

# Calculate AUC-PR score
precision_np = np.array(precision_list)
recall_np = np.array(tpr_list)
auprc = auc(recall_np, precision_np)

# Determine the optimal threshold by maximizing the F1 score
f1_scores = 2 * (precision_np * recall_np) / (precision_np + recall_np + 1e-10)
optimal_idx = np.argmax(f1_scores)
optimal_threshold_prc = thresholds[optimal_idx]

# Number of true positives and false positives at the optimal threshold
number_of_true_pos = num_TorF_pos[optimal_idx][0]
number_of_false_pos = num_TorF_pos[optimal_idx][1]

# Plot the PRC Curve on the second subplot
ax2.plot(tpr_list, precision_list, marker='o', label=f'AUPRC = {auprc:.4f}\nOptimal Threshold = {optimal_threshold_prc:.2f}\nTrue Positives = {number_of_true_pos}\nFalse Positives = {number_of_false_pos}')
ax2.set_xlabel('Recall (TPR)')
ax2.set_ylabel('Precision')
ax2.set_title('Precision-Recall Curve for ' + CSVNAME)
ax2.grid()
ax2.legend()


# Create a table with thresholds, true positives, and false positives
table_data = []
for i in range(optimal_idx - 5, optimal_idx + 7):
    table_data.append([f"{thresholds[i]:.2f}", num_TorF_pos[i][0], num_TorF_pos[i][1]])

# Add table to the plot
table = plt.table(cellText=table_data, colLabels=["Threshold", "True Positives", "False Positives"], cellLoc="center", loc="bottom", bbox=[0, -1.2, 1, 1])

# Adjust layout to prevent overlap
plt.subplots_adjust(left=0.1, bottom=0.5)

fig.text(0.05, 0.05, f'Matrix size: {n} x {m}', fontsize=12)

# Create the folder if it does not exist
if not os.path.exists(OUTPUT_FOLDER):
    os.makedirs(OUTPUT_FOLDER)

# Save the figure to the output folder
output_file = os.path.join(OUTPUT_FOLDER, f'{CSVNAME}_ROC_PRC.png')
plt.savefig(output_file)

# Show the plot
plt.show()
