# How to Start the Application

This guide explains how to run both the backend API and frontend servers.

## Prerequisites

1. **Python 3** with Flask installed
2. **Node.js** and npm installed
3. Backend dependencies installed
4. Frontend dependencies installed

## Installation

### Backend Setup

```bash
cd Testing/backend
pip install -r requirements-api.txt
```

### Frontend Setup

```bash
cd Testing/frontend
npm install
```

## Running the Application

You need to run **TWO** servers in **separate terminals**:

### Terminal 1: Backend API Server (Flask)

```bash
cd Testing/backend
python3 api.py
```

This will start the Flask API server on `http://localhost:5000`

You should see:
```
Starting Flask API server...
Main.py path: /path/to/Testing/backend/main.py
 * Running on http://0.0.0.0:5000
```

### Terminal 2: Frontend Dev Server (Vite)

```bash
cd Testing/frontend
npm start
```

This will start the Vite development server on `http://localhost:3000`

You should see:
```
VITE v5.x.x  ready in xxx ms

  ➜  Local:   http://localhost:3000/
  ➜  Network: use --host to expose
```

## Using the Application

1. Open your browser to `http://localhost:3000`
2. You'll see the Drone Missions Map with two buttons:
   - **Run main.py** - Executes the backend pipeline to regenerate the map
   - **Refresh Map** - Reloads the map display without running the pipeline

## How It Works

1. Click "Run main.py" button
2. Frontend sends POST request to `http://localhost:5000/api/run-pipeline`
3. Backend executes `main.py` which:
   - Loads challenge data
   - Solves routing
   - Generates `drone_missions_map.html` in `frontend/public/`
4. On success, the map automatically refreshes to show the new data

## Troubleshooting

### Backend Issues

**Error: "Module not found"**
```bash
cd Testing/backend
pip install flask flask-cors
```

**Error: "Address already in use"**
- Port 5000 is already taken
- Kill the process or change the port in `api.py`

### Frontend Issues

**Error: "Cannot connect to API"**
- Make sure the backend server is running on port 5000
- Check the browser console for CORS errors

**Error: "404 Not Found"**
- Make sure you're running `npm start` from the `Testing/frontend` directory
- Make sure `index.html` is in the root of the frontend directory

### CORS Errors

If you see CORS errors in the browser console, make sure:
1. Flask-CORS is installed: `pip install flask-cors`
2. The backend is running on port 5000
3. The frontend is accessing `http://localhost:5000` (not `127.0.0.1`)

## Stopping the Servers

Press `Ctrl+C` in each terminal to stop the servers.
