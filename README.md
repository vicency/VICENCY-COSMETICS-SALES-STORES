# Vicency Cosmetics Sales Dashboard

This project is an interactive sales analysis dashboard for Vicency Cosmetics, built with Streamlit. It allows users to upload sales data and explore various performance metrics through dynamic filters and visualizations.

This application is based on the analysis performed in the `cosmet.ipynb` Jupyter Notebook.

## Features

-   **Interactive Dashboard**: A user-friendly web interface to visualize sales data.
-   **Dynamic Filtering**: Filter data by Country, Product, Sales Person, and Date Range.
-   **KPI Monitoring**: At-a-glance Key Performance Indicators like Total Sales, Boxes Shipped, and more.
-   **Rich Visualizations**: Interactive charts showing:
    -   Monthly Sales Trends
    -   Sales Performance by Country
    -   Sales Person Performance (Sales vs. Boxes Shipped)
    -   Top Selling Products in each Country
-   **Data Upload**: Easily upload your own `cosmetics.csv` file for analysis.
-   **Raw Data View**: Option to view the filtered tabular data.

## Technologies Used

-   **Python**: The core programming language.
-   **Streamlit**: For creating the interactive web application.
-   **Pandas**: For data manipulation and analysis.
-   **Plotly**: For creating interactive and dynamic visualizations.

## Setup and Installation

To run this dashboard on your local machine, follow these steps:

1.  **Clone the repository (or download the files)**
    If this project is in a Git repository, you can clone it. Otherwise, ensure all files are in the same directory.

2.  **Create a virtual environment (recommended)**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3.  **Install the required dependencies**
    A `requirements.txt` file is provided for easy installation.
    ```bash
    pip install -r requirements.txt
    ```

## How to Use

1.  **Run the Streamlit application**
    Open your terminal, navigate to the project directory, and run the following command:
    ```bash
    streamlit run app.py
    ```

2.  **Upload Data**
    Your web browser will open with the dashboard. Use the file uploader to upload the `cosmetics.csv` file.

3.  **Explore**
    Once the data is loaded, use the filters in the sidebar to explore the sales data. The KPIs and charts will update dynamically based on your selections.# VICENCY-COSMETICS-SALES-STORES
