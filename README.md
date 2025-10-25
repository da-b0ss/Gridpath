# NextEra Energy Drone Optimization Challenge

## Project Setup

Follow these steps to set up and run the project:

### 1. Clone the Repository
```bash
git clone https://github.com/da-b0ss/The-Seeker 
cd The-Seeker
```

### 2. Set Up the Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the Pipeline
```bash
python main.py
```

This will:
- Load the data.
- Solve the routing problem.
- Generate the `drone_missions_map.html` file in the project root.

### 5. View the Output
Open `drone_missions_map.html` in your browser to view the interactive map of drone missions.

---

## Project Structure

```
.
├── data/
│   ├── asset_indexes.npy
│   ├── distance_matrix.npy
│   ├── photo_indexes.npy
│   ├── points_lat_long.npy
│   ├── polygon_lon_lat.wkt
│   ├── predecessors.npy
│   ├── waypoint_indexes.npy
├── src/
│   ├── __init__.py
│   ├── config.py
│   ├── data_loader.py
│   ├── routing.py
│   ├── path_decoder.py
│   ├── visualize.py
├── main.py
├── requirements.txt
├── .gitignore
├── venv/
└── drone_missions_map.html
```

### Key Files
- **`data/`**: Contains input data files.
- **`src/`**: Contains modular Python scripts for the pipeline.
- **`main.py`**: Entry point for the pipeline.
- **`requirements.txt`**: Lists Python dependencies.
- **`.gitignore`**: Specifies files to ignore in version control.
- **`drone_missions_map.html`**: Output file with the interactive map.

---

## Troubleshooting

### Common Issues
1. **Virtual Environment Not Activated**:
   - Ensure you see `(venv)` in your terminal prompt.
   - Run `source venv/bin/activate` to activate the virtual environment.

2. **Missing Dependencies**:
   - Run `pip install -r requirements.txt` to install all required packages.

3. **Index Out of Bounds Errors**:
   - Ensure all `.npy` and `.wkt` files are in the `data/` directory.

### Getting Help
Refer to the official documentation for tools used in this project:
- [Google OR-Tools Routing](https://developers.google.com/optimization/routing)
- [SciPy Dijkstra](https://docs.scipy.org/doc/scipy/reference/generated/scipy.sparse.csgraph.dijkstra.html)
- [Plotly](https://plotly.com/python/)

---
