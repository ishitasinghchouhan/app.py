# data analyser
import pandas as pd
import matplotlib.pyplot as plt

def analyse_data(file_path):
    # 1. Read CSV file
    df = pd.read_csv(file_path)

    # 2. Basic information
    rows, columns = df.shape

    print("\n==== DATA SUMMARY ====")
    print(f"Rows: {rows}")
    print(f"Columns: {columns}")

    print("\nColumn Names:")
    print(list(df.columns))

    # 3. Missing Values
    print("\n==== MISSING VALUES ====")
    print(df.isnull().sum())

    # 4. Remove duplicate rows
    duplicates = df.duplicated().sum()
    df = df.drop_duplicates()

    print(f"\nDuplicate rows removed: {duplicates}")

    # 5. Statistical analysis
    print("\n==== STATISTICS ====")
    print(df.describe())

    # 6. Find numerical columns
    numerical_columns = df.select_dtypes(include="number").columns

    print("\n==== NUMERICAL COLUMNS ====")
    print(list(numerical_columns))

    # 7. Calculate averages
    print("\n==== AVERAGES ====")

    for column in numerical_columns:
        average = df[column].mean()
        print(f"{column}: {average:.2f}")

    # 8. Create graphs
    for column in numerical_columns:
        plt.figure()

        df[column].plot(kind="hist")

        plt.title(f"Distribution of {column}")
        plt.xlabel(column)
        plt.ylabel("Frequency")

        plt.savefig(f"{column}_graph.png")
        plt.show()

    # Return the cleaned data
    return df


# Main program
if __name__ == "__main__":
    file_path = input("Enter CSV file path: ")
    analyse_data(file_path)
