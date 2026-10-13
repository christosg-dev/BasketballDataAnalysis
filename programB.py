##########################
#   Christos Gunopulos   #
##########################

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the data
df = pd.read_csv("shots.csv")

# Get teams in file order
team_order = df["TEAM_NAME"].drop_duplicates().tolist()

# Filter made and missed shots
df_made = df[df["SHOT_MADE_FLAG"] == 1]
df_missed = df[df["SHOT_MADE_FLAG"] == 0]

# Count made shots
made_counts = df_made["TEAM_NAME"].value_counts().reindex(team_order, fill_value=0)
made_df = made_counts.reset_index()
made_df.columns = ["TEAM_NAME", "Made_Shots"]

# Count missed shots
missed_counts = df_missed["TEAM_NAME"].value_counts().reindex(team_order, fill_value=0)
missed_df = missed_counts.reset_index()
missed_df.columns = ["TEAM_NAME", "Missed_Shots"]

# Global fonts
plt.rcParams.update({
    'axes.titlesize': 16,
    'axes.labelsize': 14,
    'xtick.labelsize': 12,
    'ytick.labelsize': 12,
    'legend.fontsize': 12
})

# Made Shots per Team 
plt.figure(figsize=(12, 6))
sns.barplot(data=made_df, x="TEAM_NAME", y="Made_Shots", palette="Greens_d")
plt.title("Number of Made Shots per Team")
plt.xlabel("Team")
plt.ylabel("Made Shots")
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()

# Missed Shots per Team
plt.figure(figsize=(12, 6))
sns.barplot(data=missed_df, x="TEAM_NAME", y="Missed_Shots", palette="Reds_d")
plt.title("Number of Missed Shots per Team")
plt.xlabel("Team")
plt.ylabel("Missed Shots")
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()

# Made Shot Locations 
plt.figure(figsize=(10, 9))
sns.scatterplot(data=df_made, x="LOC_X", y="LOC_Y", hue="TEAM_NAME", palette="Set2", s=60, alpha=0.7, edgecolor="k", linewidth=0.5)

plt.title("Made Shot Locations")
plt.xlabel("Court X")
plt.ylabel("Court Y")
plt.legend(title="Team", bbox_to_anchor=(1.05, 1), loc='upper left')
plt.axhline(0, color='gray', linestyle='--', linewidth=0.5)
plt.grid(True, linestyle='--', linewidth=0.3)
plt.tight_layout()
plt.show()


