##########################
#   Christos Gunopulos   # 
##########################

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set(style="whitegrid")

# Load CSV file
df = pd.read_csv("shots.csv")

def apply_hatching(ax, hatches):
    bars = ax.patches
    for bar, hatch in zip(bars, hatches):
        bar.set_hatch(hatch)
        bar.set_edgecolor('black')  # Improve contrast

hatch_patterns = ['/', '\\', '|', '-', '+', 'x', 'o', 'O', '.', '*']


# Ensure that you accept numeric data
df['SHOT_MADE_FLAG'] = pd.to_numeric(df['SHOT_MADE_FLAG'], errors='coerce')
df['SHOT_ATTEMPTED_FLAG'] = pd.to_numeric(df['SHOT_ATTEMPTED_FLAG'], errors='coerce')


### 1. Field Goal % by Shot Zone (Bar Chart) ###
zone_fg = df.groupby(['SHOT_ZONE_BASIC']).agg(
    Attempts=('SHOT_ATTEMPTED_FLAG', 'sum'),
    Makes=('SHOT_MADE_FLAG', 'sum')
)
zone_fg['FG%'] = (zone_fg['Makes'] / zone_fg['Attempts']) * 100

plt.figure(figsize=(10, 6))
ax = sns.barplot(x=zone_fg.index, y=zone_fg['FG%'], palette="Blues_d")
apply_hatching(ax, hatch_patterns * (len(zone_fg) // len(hatch_patterns) + 1))
plt.title("Field Goal % by Shot Zone")
plt.ylabel("FG%")
plt.xlabel("Shot Zone")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()



### 2. Shot Chart by Outcome (Bar Count by Location Zone) ###
# Bar chart of attempts by shot area
area_shot_counts = df.groupby(['SHOT_ZONE_AREA', 'SHOT_MADE_FLAG']).size().unstack().fillna(0)
area_shot_counts.columns = ['Missed', 'Made']
area_shot_counts[['Missed', 'Made']].plot(
    kind='bar', stacked=True, figsize=(12,6), colormap='coolwarm', edgecolor='black'
)
plt.title("Shot Attempts by Court Area")
plt.xlabel("Shot Zone Area")
plt.ylabel("Number of Shots")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()


### 3. Time-Based Shot Analysis (Bar Chart) ###
# Group by time intervals (e.g., every 15 seconds remaining)
df['Time_Remaining'] = df['MINUTES_REMAINING'] * 60 + df['SECONDS_REMAINING']
df['Time_Bin'] = pd.cut(df['Time_Remaining'], bins=range(0, 721, 30))
time_counts = df['Time_Bin'].value_counts().sort_index()

plt.figure(figsize=(12,6))
ax = sns.barplot(x=time_counts.index.astype(str), y=time_counts.values, palette="Greens_d")
apply_hatching(ax, hatch_patterns * (len(time_counts) // len(hatch_patterns) + 1))
plt.title("Shot Frequency by Time Remaining in Quarter")
plt.xlabel("Time Remaining (seconds bins)")
plt.ylabel("Number of Shots")
plt.xticks(rotation=90)
plt.tight_layout()
plt.show()


### 4. Field Goal % by Action Type (Bar Chart) ###
type_fg = df.groupby('ACTION_TYPE').agg(
    Attempts=('SHOT_ATTEMPTED_FLAG', 'sum'),
    Makes=('SHOT_MADE_FLAG', 'sum')
)
type_fg['FG%'] = (type_fg['Makes'] / type_fg['Attempts']) * 100
type_fg = type_fg[type_fg['Attempts'] >= 2]

plt.figure(figsize=(12, 6))
ax = sns.barplot(x=type_fg.index, y=type_fg['FG%'], palette="Purples_d")
apply_hatching(ax, hatch_patterns * (len(type_fg) // len(hatch_patterns) + 1))
plt.title("Field Goal % by Action Type")
plt.ylabel("FG%")
plt.xlabel("Action Type")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()



### 5. Field Goal % by Shot Distance (Bar Chart) ###
distance_fg = df.groupby('SHOT_DISTANCE').agg(
    Attempts=('SHOT_ATTEMPTED_FLAG', 'sum'),
    Makes=('SHOT_MADE_FLAG', 'sum')
)
distance_fg['FG%'] = (distance_fg['Makes'] / distance_fg['Attempts']) * 100
distance_fg = distance_fg[distance_fg['Attempts'] >= 2]

plt.figure(figsize=(12, 6))
ax = sns.barplot(x=distance_fg.index, y=distance_fg['FG%'], palette="coolwarm")
apply_hatching(ax, hatch_patterns * (len(distance_fg) // len(hatch_patterns) + 1))
plt.title("FG% as a Function of Shot Distance")
plt.xlabel("Shot Distance (feet)")
plt.ylabel("Field Goal %")
plt.xticks(rotation=90)
plt.tight_layout()
plt.show()


df['SHOT_DISTANCE'] = pd.to_numeric(df['SHOT_DISTANCE'], errors='coerce')
# Group by shot distance
distance_fg = df.groupby('SHOT_DISTANCE').agg(
    Attempts=('SHOT_ATTEMPTED_FLAG', 'sum'),
    Makes=('SHOT_MADE_FLAG', 'sum')
)
distance_fg['FG%'] = (distance_fg['Makes'] / distance_fg['Attempts']) * 100

# Filter low-attempt distances 
distance_fg = distance_fg[distance_fg['Attempts'] >= 1]

# Reset index for plotting
distance_fg = distance_fg.reset_index()

def apply_hatching(ax, hatches):
    bars = ax.patches
    for bar, hatch in zip(bars, hatches):
        bar.set_hatch(hatch)
        bar.set_edgecolor('black')

hatch_patterns = ['/', '\\', '|', '-', '+', 'x', 'o', '.', '*', 'O']
hatch_list = (hatch_patterns * (len(distance_fg) // len(hatch_patterns) + 1))[:len(distance_fg)]


# Plots
plt.figure(figsize=(12, 6))
ax = sns.barplot(data=distance_fg, x='SHOT_DISTANCE', y='FG%', palette="coolwarm")
apply_hatching(ax, hatch_list)

plt.title("Field Goal % as a Function of Shot Distance")
plt.xlabel("Shot Distance (feet)")
plt.ylabel("Field Goal %")
plt.xticks(rotation=90)
plt.tight_layout()
plt.show()


#### 
df['SHOT_ATTEMPTED_FLAG'] = pd.to_numeric(df['SHOT_ATTEMPTED_FLAG'], errors='coerce')

# Group by distance and count attempts
distance_attempts = df.groupby('SHOT_DISTANCE')['SHOT_ATTEMPTED_FLAG'].sum()

# Convert to percentage
attempt_percentages = (distance_attempts / distance_attempts.sum()) * 100
attempt_percentages = attempt_percentages.reset_index(name='Attempt %')

def apply_hatching(ax, hatches):
    bars = ax.patches
    for bar, hatch in zip(bars, hatches):
        bar.set_hatch(hatch)
        bar.set_edgecolor('black')

# Define hatching patterns
hatch_patterns = ['/', '\\', '|', '-', '+', 'x', 'o', '.', '*', 'O']
hatch_list = (hatch_patterns * (len(attempt_percentages) // len(hatch_patterns) + 1))[:len(attempt_percentages)]

# Plots
plt.figure(figsize=(12, 6))
ax = sns.barplot(data=attempt_percentages, x='SHOT_DISTANCE', y='Attempt %', palette="viridis")
apply_hatching(ax, hatch_list)

plt.title("Percentage of Shot Attempts by Distance")
plt.xlabel("Shot Distance (feet)")
plt.ylabel("Attempt Percentage (%)")
plt.xticks(rotation=90)
plt.tight_layout()
plt.show()





