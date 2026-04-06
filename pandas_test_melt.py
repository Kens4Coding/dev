import pandas as pd

df = pd.DataFrame(
    {
        "A": {0: "a", 1: "b", 2: "c"},
        "B": {0: 1, 1: 3, 2: 5},
        "C": {0: 2, 1: 4, 2: 6},
    }
)

# clear terminal and move cursor to top home position
print("\033[2J\033[H", end="")


print("\nStarting dataframe")
print(df.head())
print(df.index)

print("\ndf.melt()")
print(df.melt())

print("\ndf.melt(id_vars='A')")
print(df.melt(id_vars='A'))

print("\ndf.melt(id_vars='A',value_vars='B')")
print(df.melt(id_vars='A',value_vars='B'))

print("\ndf.melt(ignore_index=False)")
print(df.melt(ignore_index=False))


