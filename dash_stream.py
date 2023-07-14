import streamlit as st
import requests

# Define the FastAPI server URL
FASTAPI_URL = "http://127.0.0.2:8000"

# Create the Streamlit app
def main():
    st.title("FastAPI - Streamlit Integration")

    # File upload
    uploaded_files = st.file_uploader("Upload CSV files", accept_multiple_files=True)

    # Key input
    key1 = st.text_input("Key 1")
    key2 = st.text_input("Key 2")

    # Column selection
    x_column = st.selectbox("X Column", ["gender", "product_id"])
    y_columns = st.multiselect("Y Columns", ["price", "age"])

    # Graph types
    graph_types = st.multiselect("Graph Types", ["line", "bar"])

    # Button to trigger the merge_tables API
    if st.button("Merge Tables"):
        # Prepare the data and files for the API request
        data = {
            "key1": key1,
            "key2": key2,
            "x_column": x_column,
            "y_columns": y_columns,
            "graph_types": graph_types
        }
        files = [("files", file) for file in uploaded_files]

        # Make the POST request to FastAPI
        response = requests.post(f"{FASTAPI_URL}/merge_tables_merge_tables_post", data=data, files=files)

        # Process the response
        if response.status_code == 200:
            result = response.json()
            st.write("Merged Table:")
            st.dataframe(result["merged_table"])

            st.write("Graphs:")
            for graph_data in result["graphs"]:
                for graph in graph_data["graphs"]:
                    graph_type = graph["type"]
                    graph_values = graph["data"]
                    st.write(f"{graph_type} graph:")
                    st.write(graph_values)

            st.write("Statistics:")
            st.write(result["stats"])

        else:
            st.error(f"Error: {response.status_code} - {response.text}")

# Run the Streamlit app
if __name__ == "__main__":
    main()
