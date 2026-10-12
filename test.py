from pathlib import Path
import pandas as pd

base = Path("Ass2-1/Results/minihack_maze_groq")

for file in base.rglob("*_run_00.csv"):
    df = pd.read_csv(file)
    print("File:", file)
    print("Total step reward:", df["Reward"].sum())
    print("Last step reward:", df["Reward"].iloc[-1])
