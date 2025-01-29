import pandas as pd
import matplotlib.pyplot as plt

def extract_execution_times(file_paths, executor_labels):
    all_data = []

    for file_path, executor_label in zip(file_paths, executor_labels):
        with open(file_path, "r") as file:
            lines = file.readlines()

        extracted_lines = [line for line in lines if "OK created sql table model" in line]

        data = {}
        for line in extracted_lines:
            parts = line.split("sql table model ")
            if len(parts) > 1:
                table_part = parts[1].split(" ......")[0]
                time_part = line.split("[OK in ")[-1].replace("s]\n", "")
                try:
                    time_taken = float(time_part)
                    data[table_part] = time_taken
                except ValueError:
                    continue

        all_data.append(pd.DataFrame(data.items(), columns=["Tabela", f"Czas wykonania ({executor_label})"]))

    final_df = all_data[0]
    for df in all_data[1:]:
        final_df = pd.merge(final_df, df, on="Tabela", how="outer")

    final_df.insert(0, "Nr", range(1, len(final_df) + 1))

    sum_values = [final_df[col].sum() / 60 if final_df[col].dtype in ['float64', 'int64'] else None for col in final_df.columns[2:]]
    sum_row = [None, "SUMA (minuty)"] + sum_values
    sum_df = pd.DataFrame([sum_row], columns=final_df.columns)

    final_df = pd.concat([final_df, sum_df], ignore_index=True)

    return final_df

def generate_execution_plot(df, output_file="execution_plot.png"):
    df_filtered = df.iloc[:-1]  # Remove last row with sum
    df_filtered = df_filtered.drop(columns=["Nr"])  # Remove column "Nr"
    df_filtered.set_index("Tabela").plot(kind="barh", figsize=(15, 10))
    plt.title("Czas wykonania dla wszystkich przypadków")
    plt.xlabel("Czas (s)")
    plt.ylabel("Tabela")
    plt.legend(title="Executors")
    plt.savefig(output_file)
    plt.close()

def generate_total_execution_plot(df, output_file="total_execution_plot.png"):
    sum_row = df.iloc[-1, 2:].dropna()  # Extract the last row with sums
    sum_row.plot(kind="bar", figsize=(10, 6))
    plt.title("Łączny czas wykonania dla poszczególnych executorów")
    plt.ylabel("Czas wykonania (min)")
    plt.xticks(rotation=45)
    plt.savefig(output_file)
    plt.close()

file_paths = ["1Executor.txt", "2Executor.txt", "5Executor.txt"]
executor_labels = ["Executors = 1", "Executors = 2", "Executors = 5"]
execution_table = extract_execution_times(file_paths, executor_labels)

print(execution_table)

execution_table.to_csv("execution_times.csv", index=False)

generate_execution_plot(execution_table)
generate_total_execution_plot(execution_table)
