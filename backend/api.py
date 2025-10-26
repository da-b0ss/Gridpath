#!/usr/bin/env python3
"""
Simple Flask API to run the drone challenge pipeline and serve the generated map.
"""
import os
import sys
import subprocess
import json
from flask import Flask, jsonify, send_from_directory, request
from flask_cors import CORS

# Add the backend directory to the path so we can import from src
sys.path.insert(0, os.path.dirname(__file__))

from src.routing import SEARCH_TIME_LIMIT_SECONDS
from src import config

app = Flask(__name__)
CORS(app)  # Enable CORS for React frontend

# Path to the main.py script
MAIN_PY_PATH = os.path.join(os.path.dirname(__file__), 'main.py')
FRONTEND_PUBLIC_PATH = os.path.join(os.path.dirname(__file__), '../frontend/public')
FLEET_CONFIG_PATH = os.path.join(os.path.dirname(__file__), 'data', 'fleet_config.json')

# API timeout = routing timeout + 30 second buffer
API_TIMEOUT = SEARCH_TIME_LIMIT_SECONDS + 30

@app.route('/api/run-pipeline', methods=['POST'])
def run_pipeline():
    """
    Execute main.py to regenerate the drone missions map.
    Accepts fleet configuration from the frontend.
    """
    print(f"\n{'='*60}")
    print(f"Starting pipeline execution...")
    print(f"Timeout: {API_TIMEOUT} seconds")
    print(f"{'='*60}\n")

    try:
        # Get fleet configuration from request
        request_data = request.get_json() or {}
        fleet_capacities = request_data.get('fleet_capacities', None)

        # Validate fleet configuration
        if fleet_capacities:
            # Ensure it's a list of numbers
            if not isinstance(fleet_capacities, list) or len(fleet_capacities) < 1 or len(fleet_capacities) > 30:
                return jsonify({
                    'success': False,
                    'message': 'Fleet must have between 1 and 30 drones'
                }), 400

            # Validate each capacity
            for capacity in fleet_capacities:
                if not isinstance(capacity, (int, float)) or capacity < 0 or capacity > config.STANDARD_BATTERY_CAPACITY:
                    return jsonify({
                        'success': False,
                        'message': f'Each drone capacity must be between 0 and {config.STANDARD_BATTERY_CAPACITY}'
                    }), 400

            # Save fleet configuration to JSON file
            os.makedirs(os.path.dirname(FLEET_CONFIG_PATH), exist_ok=True)
            with open(FLEET_CONFIG_PATH, 'w') as f:
                json.dump({'fleet_capacities': fleet_capacities}, f)

            print(f"Fleet configuration saved: {len(fleet_capacities)} drones")
            print(f"Capacities: {fleet_capacities}")
        else:
            # Remove existing config file if no fleet specified
            if os.path.exists(FLEET_CONFIG_PATH):
                os.remove(FLEET_CONFIG_PATH)
            print("Using default fleet configuration")

        # Run main.py as a subprocess
        import time
        start_time = time.time()

        result = subprocess.run(
            ['python3', MAIN_PY_PATH],
            cwd=os.path.dirname(MAIN_PY_PATH),
            capture_output=True,
            text=True,
            timeout=API_TIMEOUT  # Dynamic timeout based on routing.py + 30 seconds
        )

        elapsed_time = time.time() - start_time
        print(f"\nPipeline completed in {elapsed_time:.2f} seconds")

        if result.returncode == 0:
            print(f"✓ Pipeline succeeded")
            print(f"Output preview: {result.stdout[:200]}...")

            map_path = os.path.join(FRONTEND_PUBLIC_PATH, 'drone_missions_map.html')
            if os.path.exists(map_path):
                print(f"✓ Map file exists at: {map_path}")
                file_timestamp = os.path.getmtime(map_path)
            else:
                print(f"✗ Warning: Map file not found at: {map_path}")
                file_timestamp = None

            return jsonify({
                'success': True,
                'message': f'Pipeline executed successfully in {elapsed_time:.2f}s',
                'output': result.stdout,
                'timestamp': file_timestamp,
                'elapsed_time': elapsed_time
            })
        else:
            print(f"✗ Pipeline failed with return code {result.returncode}")
            print(f"Error: {result.stderr[:500]}")
            return jsonify({
                'success': False,
                'message': 'Pipeline execution failed',
                'error': result.stderr,
                'output': result.stdout
            }), 500

    except subprocess.TimeoutExpired as e:
        print(f"✗ Pipeline timed out after {API_TIMEOUT} seconds")
        return jsonify({
            'success': False,
            'message': f'Pipeline execution timed out after {API_TIMEOUT} seconds'
        }), 500
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error executing pipeline: {str(e)}'
        }), 500

@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint."""
    return jsonify({'status': 'ok'})

if __name__ == '__main__':
    print("Starting Flask API server...")
    print(f"Main.py path: {MAIN_PY_PATH}")
    print(f"Frontend public path: {FRONTEND_PUBLIC_PATH}")
    print(f"API timeout: {API_TIMEOUT} seconds (routing timeout + 30 second buffer)")
    app.run(host='0.0.0.0', port=5000, debug=True)
