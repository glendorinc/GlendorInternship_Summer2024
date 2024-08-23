import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

thresholds = {
    'Dlib_afniDefaced_euclidean_l2_30': 0.27,
    'Dlib_fslDefaced_euclidean_l2_30': 0.26,
    'dlib_pydeface_euclidean_l2_30': 0.33,
    'Facenet512_afniDefaced_cosine_30': 0.17,
    'Facenet512_fslDefaced_cosine_30': 0.21,
    'Facenet512_pydeface_cosine_30': 0.34,
    'VGG-Face_afniDefaced_cosine_30': 0.26,
    'VGG-Face_fslDefaced_cosine_30': 0.21,
    'VGG-Face_pydeface_cosine_30': 0.52,
}


# Full path to the CSV file
CSVPATH = '/Users/avnoorludhar/Desktop/uwindsor/Glendor/testingImages100x100/FinalResultsCSVs/30%CSV'
OUTPUT_FOLDER = '/Users/avnoorludhar/Desktop/uwindsor/Glendor/testingImages100x100/FinalResultsCSVs/TableFinal'
num_TorF_pos = []

for CSVNAME, threshold in thresholds.items():
    data = pd.read_csv(os.path.join(CSVPATH, CSVNAME + '.csv'))

    # Convert to numpy array
    scores = data.to_numpy()

    # Delete the first column of labels
    scores = np.delete(scores, 0, axis=1)

    # Number of rows and columns
    n, m = scores.shape

    # Expected answer with the main diagonal all filled with 1s
    expectedAns = np.zeros((n, m))
    np.fill_diagonal(expectedAns, 1)
    predicted_labels = (scores <= threshold).astype(int)

    truePos = np.sum((predicted_labels == 1) & (expectedAns == 1))
    trueNeg = np.sum((predicted_labels == 0) & (expectedAns == 0))
    falsePos = np.sum((predicted_labels == 1) & (expectedAns == 0))
    falseNeg = np.sum((predicted_labels == 0) & (expectedAns == 1))

    num_TorF_pos.append((CSVNAME, f"{threshold:.2f}", truePos, falsePos, falseNeg, f"{n}x{m}"))

# Create a figure with one subplot for the table
fig, ax = plt.subplots(1, 1, figsize=(16, 10))

# Create a table with thresholds, true positives, and false positives
table_data = [list(item) for item in num_TorF_pos]

# Add table to the plot
table = plt.table(cellText=table_data, colLabels=["CSVFile", "Threshold", "True Positives", "False Positives", "False Negative", "Matrix Size"], cellLoc="center", loc="center")

# Set font size and scale the table
table.auto_set_font_size(False)
table.set_fontsize(14)
table.scale(1, 1.5)

# Adjust column widths key represents the row and column we are in
for key, cell in table.get_celld().items():
    cell.set_fontsize(14)
    if key[1] == 0:  # Header row
        cell.set_width(0.25)  # Increase width of the first column
    else:
        cell.set_width(0.1)  # Normal width for other columns

# Adjust layout to make room for the table
ax.axis('off') 
plt.tight_layout()

# Create the folder if it does not exist
if not os.path.exists(OUTPUT_FOLDER):
    os.makedirs(OUTPUT_FOLDER)

# Save the figure to the output folder
output_file = os.path.join(OUTPUT_FOLDER, 'finalTableResults.png')
plt.savefig(output_file)

# Show the plot
plt.show()
