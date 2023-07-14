import pandas as pd
from typing import List
from fastapi import FastAPI, UploadFile, File, Request, Form
import matplotlib.pyplot as plt
import seaborn as sns

app = FastAPI()

def generate_line_graph(data):
    # Generate line graph using matplotlib or seaborn
    # Replace this with your own logic to generate line graphs
    plt.plot(data.index, data.values)
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.title("Line Graph")
    plt.grid(True)
    plt.show()

def generate_bar_graph(data):
    # Generate bar graph using matplotlib or seaborn
    # Replace this with your own logic to generate bar graphs
    plt.bar(data.index, data.values)
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.title("Bar Graph")
    plt.grid(True)
    plt.show()

def calculate_statistics(data):
    # Calculate statistics using pandas or other libraries
    # Replace this with your own logic to calculate statistics
    stats = {
        "mean": data.mean(),
        "median": data.median(),
        "min": data.min(),
        "max": data.max()
    }
    return stats

@app.post("/merge_tables")
async def merge_tables(
    request: Request,
    files: List[UploadFile] = File(...),
    key1: str = Form(...),
    key2: str = Form(...),
    y_columns: List[str] = Form(...),
    graph_functions: List[str] = Form(...)
):
    try:
        # Verify if at least two files have been uploaded
        if len(files) < 2:
            return {"error": "At least two files must be uploaded"}

        dataframes = []
        for file in files:
            # Load each file as a DataFrame
            dataframe = pd.read_csv(file.file, encoding='latin1')
            dataframes.append(dataframe)

        # Perform table merge using the specified merge keys
        merged_table = dataframes[0]
        if key1 and key2:
            merged_table = pd.merge(merged_table, dataframes[1], left_on=key1, right_on=key2)
        else:
            for i in range(1, len(dataframes)):
                merged_table = pd.merge(merged_table, dataframes[i])

        graphs = []
        stats = {}

        for column in y_columns:
            graph_data = {
                "column": column,
                "graphs": []
            }

            column_data = merged_table[column]

            for graph_function in graph_functions:
                graph = {}

                if graph_function == "line":
                    graph["type"] = "line"
                    generate_line_graph(column_data)
                elif graph_function == "bar":
                    graph["type"] = "bar"
                    generate_bar_graph(column_data)
                else:
                    return {"error": f"Unsupported graph function: {graph_function}"}

                graph_data["graphs"].append(graph)

            graphs.append(graph_data)

        for column in y_columns:
            column_stats = calculate_statistics(merged_table[column])
            stats[column] = column_stats

        return {"merged_table": merged_table, "graphs": graphs, "stats": stats}
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.2", port=8000)
