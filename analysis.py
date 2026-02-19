import pandas as pd
import numpy as np
from scipy import stats
from outlier import remove_outliers_excel

# ---------- FILE PATH ----------
raw_file = "raw_data.xlsx"
clean_file = "cleaned_data.xlsx"

# ---------- REMOVE OUTLIERS ----------
original_df = pd.read_excel(raw_file)
cleaned_df = remove_outliers_excel(raw_file, clean_file)

print("\n===== DATA CLEANING =====")
print("Original Participants:", len(original_df))
print("After Outlier Removal:", len(cleaned_df))
print("Removed:", len(original_df) - len(cleaned_df))

# ---------- ERROR COLUMNS ----------
error_cols = [
    'Control Error',
    'Baseline Error',
    'Length 200 Error',
    'Length 400 Error',
    'Thick 1px Error',
    'Thick 5px Error',
    'Fins 2 Error',
    'Angle 30 Error',
    'Angle 150 Error',
    'Brentano Error'
]

# ---------- DESCRIPTIVE STATISTICS ----------
summary = []

for col in error_cols:
    mean = cleaned_df[col].mean()
    std = cleaned_df[col].std()
    mean_abs = cleaned_df[col].abs().mean()

    summary.append([col, mean, std, mean_abs])

summary_df = pd.DataFrame(summary,
                          columns=["Condition", "Mean % Error", "Std Dev", "Mean |% Error|"])

print("\n===== DESCRIPTIVE STATISTICS =====\n")
print(summary_df)

summary_df.to_csv("summary_stats.csv", index=False)

# ---------- CONTROL vs BASELINE ----------
control = cleaned_df['Control Error']
baseline = cleaned_df['Baseline Error']

t_stat, p_val = stats.ttest_rel(control, baseline)

print("\n===== CONTROL vs BASELINE =====")
print("Paired t-test")
print("t =", t_stat)
print("p =", p_val)

# ---------- DEVICE EFFECT ----------
device_col = "Device being used to attempt this test"

if device_col in cleaned_df.columns:

    illusion_cols = error_cols[1:]  # exclude control
    cleaned_df["Overall_Illusion"] = cleaned_df[illusion_cols].abs().mean(axis=1)

    print("\n===== DEVICE EFFECT =====")

    device_df = cleaned_df.dropna(subset=[device_col])

    device_means = device_df.groupby(device_col)["Overall_Illusion"].mean()
    print("\nMean Illusion Strength by Device:")
    print(device_means)

    devices = device_df[device_col].unique()

    if len(devices) == 2:
        group1 = device_df[device_df[device_col] == devices[0]]["Overall_Illusion"]
        group2 = device_df[device_df[device_col] == devices[1]]["Overall_Illusion"]

        t_stat, p_val = stats.ttest_ind(group1, group2)

        print("\nIndependent t-test between devices")
        print("t =", t_stat)
        print("p =", p_val)
# ---------- PLOTTING SECTION ----------
import matplotlib.pyplot as plt

print("\n===== GENERATING PLOTS =====")

# 1️⃣ Overall Illusion Strength Across Conditions
mean_abs = cleaned_df[error_cols].abs().mean()

plt.figure()
mean_abs.plot(kind='bar')
plt.ylabel("Mean Absolute % Error")
plt.title("Illusion Strength Across Conditions")
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig("plot_overall_conditions.png")
plt.close()


# 2️⃣ Angle Effect Plot
angle_cols = ['Angle 30 Error', 'Baseline Error', 'Angle 150 Error']
angle_means = cleaned_df[angle_cols].abs().mean()

plt.figure()
angle_means.plot(kind='bar')
plt.ylabel("Mean Absolute % Error")
plt.title("Effect of Fin Angle on Illusion Strength")
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig("plot_angle_effect.png")
plt.close()


# 3️⃣ Length Effect Plot
length_cols = ['Length 200 Error', 'Baseline Error', 'Length 400 Error']
length_means = cleaned_df[length_cols].abs().mean()

plt.figure()
length_means.plot(kind='bar')
plt.ylabel("Mean Absolute % Error")
plt.title("Effect of Line Length on Illusion Strength")
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig("plot_length_effect.png")
plt.close()


# 4️⃣ Device Effect Plot
device_col = "Device being used to attempt this test"

if device_col in cleaned_df.columns:
    illusion_cols = error_cols[1:]  # exclude control
    cleaned_df["Overall_Illusion"] = cleaned_df[illusion_cols].abs().mean(axis=1)

    device_df = cleaned_df.dropna(subset=[device_col])
    device_means = device_df.groupby(device_col)["Overall_Illusion"].mean()

    plt.figure()
    device_means.plot(kind='bar')
    plt.ylabel("Mean Absolute % Error")
    plt.title("Illusion Strength by Device Type")
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig("plot_device_effect.png")
    plt.close()

print("Plots saved successfully.")

print("\nAnalysis Complete.")
