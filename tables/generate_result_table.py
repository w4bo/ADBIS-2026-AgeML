import pandas as pd
import numbers
from pathlib import Path

INPUT_DIR = Path(__file__).parent
OUTPUT_DIR = Path(__file__).parent

DATASET_NAME_MAP = {
    "wilt": "Wilt",
    "texture": "Texture",
    "madelon": "Madelon",
    "har": "HAR",
    "adult": "Adult",
    "mnist_784": "MNIST_784",
    "ames_housing": "Ames Housing",
    "california_housing": "California Housing",
    "auto_mpg": "Auto MPG",
}

def is_better(row):
    best = row["Best Score"]
    base = row["Baseline"]
    problem = row["Problem"]

    if pd.isna(best) or pd.isna(base):
        return False

    if problem == "classification":
        return best > base

    if problem == "regression":
        return best < base

    return False

def pretty_dataset_name(name: str) -> str:
    return DATASET_NAME_MAP.get(str(name).lower(), str(name))

def pretty_model_name(name: str) -> str:
    name = name.replace("-", " ")
    parts = name.split()

    pretty_parts = []
    for p in parts:
        if "_" in p and all(x.isdigit() for x in p.split("_")):
            pretty_parts.append(p.replace("_", "."))
        else:
            pretty_parts.append(p.capitalize())

    return " ".join(pretty_parts)

def format_value(v):
    if pd.isna(v):
        return ""

    if isinstance(v, numbers.Number):
        if isinstance(v, int):
            return f"{v:,}"
        return f"{v:,.3f}"

    return str(v)

def latex_escape(s):
    s = str(s)
    return (
        s.replace("&", "\\&")
         .replace("%", "\\%")
         .replace("$", "\\$")
         .replace("#", "\\#")
         .replace("_", "\\_")
         .replace("{", "\\{")
         .replace("}", "\\}")
    )

def build_column_format(columns):
    fmt = []
    for col in columns:
        if "Time" in col:
            fmt.append("c")
        elif col in [
            "Best Score",
            "Actual P.",
            "Input Tokens",
            "Output Tokens",
            "Total Tokens",
            "Putative Cost ($)"
        ]:
            fmt.append("r")
        else:
            fmt.append("l")
    return "".join(fmt)

def df_to_latex_rows(df):
    rows = []
    for _, row in df.iterrows():

        better = is_better(row)

        values = []
        for col_name, v in row.items():
            if col_name == "Problem":
                continue

            val = format_value(v)
            val = latex_escape(val)

            if col_name == "Best Score" and better:
                val = f"\\textbf{{{val}}}"

            values.append(val)

        rows.append(" & ".join(values) + " \\\\")
    return rows

def process_file(csv_path):
    raw_model_name = csv_path.stem.replace("-results", "")
    model_name = pretty_model_name(raw_model_name)

    df = pd.read_csv(csv_path)

    df["Dataset"] = df["Dataset"].apply(pretty_dataset_name)

    columns_to_keep = [
        "Dataset",
        "Best Test-set Score",
        "Baseline",
        "Actual Time",
        "Equivalent Time",
        "LLM Inference Time",
        "ML Training Time",
        "Actual Pipelines",
        "Input Tokens",
        "Output Tokens",
        "Total Tokens",
        "Putative Cost ($)",
        "Problem"
    ]

    df = df[columns_to_keep]
    # Rename Actual Pipelines into Actual P.
    df = df.rename(columns={"Actual Pipelines": "Actual P."})
    df = df.rename(columns={"Best Test-set Score": "Best Score"})

    df_class = df[df["Problem"] == "classification"]
    df_reg = df[df["Problem"] == "regression"]

    columns = df_class.columns[:-1]
    col_format = build_column_format(columns)

    latex = []
    latex.append("\\begin{table*}[ht!]")
    latex.append("\\centering")
    latex.append("\\small")
    latex.append("\\resizebox{\\textwidth}{!}{%")

    latex.append(f"\\begin{{tabular}}{{{col_format}}}")
    latex.append("\\hline")

    header = " & ".join([latex_escape(c) for c in columns]) + " \\\\"
    latex.append(header)
    latex.append("\\hline")

    latex.extend(df_to_latex_rows(df_class))
    latex.append("\\hline")
    latex.extend(df_to_latex_rows(df_reg))

    latex.append("\\hline")
    latex.append("\\end{tabular}")
    latex.append("}")

    caption = (
        f"Results obtained with {model_name}. "
        f"Balanced accuracy is used for classification tasks (first six) and RMSE for regression tasks (last three). "
        f"Values in bold indicate better performance than the baseline. "
        f"Actual P. stands for the actual number of pipelines correctly executed (out of the budget of 30). "
    )

    label = f"tab:{raw_model_name.replace('-', '_')}_results"

    latex.append(f"\\caption{{{latex_escape(caption)}}}")
    latex.append(f"\\label{{{label}}}")
    latex.append("\\end{table*}")

    output_path = OUTPUT_DIR / f"{raw_model_name}-table.tex"

    with open(output_path, "w") as f:
        f.write("\n".join(latex))

    print(f"Generated: {output_path}")

def main():
    csv_files = list(INPUT_DIR.glob("*-results.csv"))

    if not csv_files:
        print("No CSV files found in tables/")
        return

    for csv_file in csv_files:
        process_file(csv_file)

if __name__ == "__main__":
    main()