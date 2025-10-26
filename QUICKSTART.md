# Quick Start Guide

## Installation

### 1. Install Backend Dependencies

```bash
cd backend
pip install -r requirements-api.txt
```

### 2. Install Frontend Dependencies

```bash
cd frontend
npm install
```

## Running the Application

### Option 1: Automatic (Recommended)

```bash
cd Testing
./start-dev.sh
```

This will automatically open both servers in separate terminal tabs.

### Option 2: Manual

**Terminal 1 - Backend:**
```bash
cd Testing/backend
python3 api.py
```

**Terminal 2 - Frontend:**
```bash
cd Testing/frontend
npm start
```

## Using the Application

1. Open browser to: `http://localhost:3000`
2. You'll see the Drone Missions Map with control buttons
3. Click **"Run main.py"** to regenerate the map with new data
4. Click **"Refresh Map"** to reload the current map

## Features

- 🚁 **Interactive Map** - View drone missions and flight zones
- 🔄 **Live Regeneration** - Click a button to run the pipeline
- ⚡ **Auto Refresh** - Map updates automatically after pipeline runs
- 📊 **Visual Feedback** - See success/error messages inline

## Architecture

```
┌─────────────────┐         ┌──────────────────┐
│  React Frontend │ ──HTTP──▶│  Flask Backend   │
│  (Port 3000)    │◀────────│  (Port 5000)     │
└─────────────────┘         └──────────────────┘
         │                           │
         │                           │
         ▼                           ▼
   Displays Map              Runs main.py
   (iframe HTML)             Generates HTML
```

## File Structure

```
Testing/
├── backend/
│   ├── api.py                    # Flask API server
│   ├── main.py                   # Drone pipeline
│   ├── requirements-api.txt      # Python dependencies
│   └── src/                      # Pipeline source code
│
├── frontend/
│   ├── src/
│   │   ├── DroneMissionsMap.tsx  # Map component with buttons
│   │   ├── App.tsx               # Main app
│   │   └── index.tsx             # Entry point
│   ├── public/
│   │   └── drone_missions_map.html  # Generated map
│   ├── package.json
│   └── index.html
│
├── start-dev.sh                  # Auto-start script
├── QUICKSTART.md                 # This file
└── START_SERVERS.md              # Detailed instructions
```

## API Endpoints

- `POST /api/run-pipeline` - Execute main.py and regenerate map
- `GET /api/health` - Health check

## Troubleshooting

**"Cannot connect to backend"**
- Ensure Flask server is running on port 5000
- Check `http://localhost:5000/api/health`

**"Map not updating"**
- Click "Refresh Map" button
- Check browser console for errors

**"Port already in use"**
- Kill process on port 5000 or 3000
- Or change ports in api.py / vite.config.ts

## Next Steps

- Modify `main.py` to change the routing algorithm
- Customize the map styling in the frontend
- Add more API endpoints for different operations

For more details, see [START_SERVERS.md](START_SERVERS.md)
