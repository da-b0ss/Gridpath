import React, { useEffect, useRef, useState } from 'react';
import DronePanel, { Drone } from './DronePanel';

interface DroneMissionsMapProps {
  /** Optional width of the map container */
  width?: string | number;
  /** Optional height of the map container */
  height?: string | number;
  /** API base URL */
  apiUrl?: string;
}

/**
 * DroneMissionsMap Component
 *
 * This component renders a drone missions map visualization using Plotly.
 * The visualization includes flight zones, drone missions, and various map layers.
 */
const DroneMissionsMap: React.FC<DroneMissionsMapProps> = ({
  width = '100%',
  height = '100vh',
  apiUrl = 'http://localhost:5000'
}) => {
  const iframeRef = useRef<HTMLIFrameElement>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [message, setMessage] = useState<string | null>(null);
  const [mapKey, setMapKey] = useState(Date.now());
  const [progress, setProgress] = useState(0);

  const SEARCH_TIME_LIMIT_SECONDS = 30; // Must match backend routing.py
  const STANDARD_BATTERY_CAPACITY = 37725; // Must match backend config.py

  // Drone fleet state
  const [drones, setDrones] = useState<Drone[]>([
    { id: 1, batteryCapacity: STANDARD_BATTERY_CAPACITY }
  ]);
  const [nextDroneId, setNextDroneId] = useState(2);

  useEffect(() => {
    // Any additional initialization logic can go here
  }, []);

  // Progress bar animation when loading
  useEffect(() => {
    if (isLoading) {
      setProgress(0);
      const startTime = Date.now();
      const duration = SEARCH_TIME_LIMIT_SECONDS * 1000; // Convert to milliseconds

      const interval = setInterval(() => {
        const elapsed = Date.now() - startTime;
        const newProgress = Math.min((elapsed / duration) * 100, 100);
        setProgress(newProgress);

        if (newProgress >= 100) {
          clearInterval(interval);
        }
      }, 50); // Update every 50ms for smooth animation

      return () => clearInterval(interval);
    } else {
      setProgress(0);
    }
  }, [isLoading]);

  // Drone management functions
  const handleAddDrone = () => {
    if (drones.length < 30) {
      setDrones([...drones, { id: nextDroneId, batteryCapacity: STANDARD_BATTERY_CAPACITY }]);
      setNextDroneId(nextDroneId + 1);
    }
  };

  const handleRemoveDrone = (id: number) => {
    if (drones.length > 1) {
      setDrones(drones.filter(drone => drone.id !== id));
    }
  };

  const handleUpdateCapacity = (id: number, capacity: number) => {
    setDrones(drones.map(drone =>
      drone.id === id ? { ...drone, batteryCapacity: capacity } : drone
    ));
  };

  const refreshDisplay = async () => {
    setIsLoading(true);
    setError(null);
    setMessage(null);

    try {
      // Prepare fleet configuration
      const fleetCapacities = drones.map(drone => drone.batteryCapacity);

      const response = await fetch(`${apiUrl}/api/run-pipeline`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          fleet_capacities: fleetCapacities
        })
      });

      const data = await response.json();

      if (data.success) {
        setMessage('Display refreshed successfully!');
        // Force iframe reload by updating the key
        setMapKey(Date.now());
      } else {
        setError(data.message || 'Failed to refresh display');
      }
    } catch (err) {
      setError(`Error: ${err instanceof Error ? err.message : 'Unknown error'}`);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div
      style={{
        width: typeof width === 'number' ? `${width}px` : width,
        height: typeof height === 'number' ? `${height}px` : height,
        display: 'flex',
        flexDirection: 'row',
        overflow: 'hidden',
        backgroundColor: '#0f1420'
      }}
    >
      {/* Main Map Section */}
      <div style={{
        flex: 1,
        display: 'flex',
        flexDirection: 'column',
        overflow: 'hidden'
      }}>
      {/* Control Panel */}
      <div style={{
        padding: '12px 24px',
        background: 'linear-gradient(135deg, #1a1f35 0%, #141824 100%)',
        borderBottom: '1px solid rgba(99, 102, 241, 0.15)',
        display: 'flex',
        gap: '14px',
        alignItems: 'center',
        flexWrap: 'wrap',
        boxShadow: '0 2px 12px rgba(0, 0, 0, 0.25)',
        flexShrink: 0
      }}>
        <button
          onClick={refreshDisplay}
          disabled={isLoading}
          style={{
            padding: '10px 20px',
            background: isLoading
              ? 'linear-gradient(135deg, #374151 0%, #1f2937 100%)'
              : 'linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%)',
            color: 'white',
            border: 'none',
            borderRadius: '6px',
            cursor: isLoading ? 'not-allowed' : 'pointer',
            fontSize: '14px',
            fontWeight: '600',
            transition: 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)',
            boxShadow: isLoading
              ? 'none'
              : '0 4px 12px rgba(99, 102, 241, 0.3), inset 0 1px 0 rgba(255, 255, 255, 0.1)',
            position: 'relative',
            overflow: 'hidden',
            display: 'flex',
            alignItems: 'center',
            gap: '8px'
          }}
          onMouseEnter={(e) => {
            if (!isLoading) {
              e.currentTarget.style.transform = 'translateY(-2px)';
              e.currentTarget.style.boxShadow = '0 6px 20px rgba(99, 102, 241, 0.4), inset 0 1px 0 rgba(255, 255, 255, 0.1)';
            }
          }}
          onMouseLeave={(e) => {
            if (!isLoading) {
              e.currentTarget.style.transform = 'translateY(0)';
              e.currentTarget.style.boxShadow = '0 4px 12px rgba(99, 102, 241, 0.3), inset 0 1px 0 rgba(255, 255, 255, 0.1)';
            }
          }}
        >
          <span style={{ fontSize: '16px' }}>
            {isLoading ? '⟳' : '↻'}
          </span>
          {isLoading ? 'Refreshing Display...' : 'Refresh Display'}
        </button>

        {/* Status Messages */}
        {message && (
          <div style={{
            padding: '6px 14px',
            backgroundColor: 'rgba(16, 185, 129, 0.12)',
            border: '1px solid rgba(16, 185, 129, 0.3)',
            borderRadius: '6px',
            color: '#34d399',
            fontSize: '13px',
            fontWeight: '500',
            display: 'flex',
            alignItems: 'center',
            gap: '6px',
            animation: 'fadeIn 0.3s ease-in'
          }}>
            <span style={{
              fontSize: '14px',
              display: 'flex',
              alignItems: 'center'
            }}>✓</span>
            {message}
          </div>
        )}
        {error && (
          <div style={{
            padding: '6px 14px',
            backgroundColor: 'rgba(239, 68, 68, 0.12)',
            border: '1px solid rgba(239, 68, 68, 0.3)',
            borderRadius: '6px',
            color: '#f87171',
            fontSize: '13px',
            fontWeight: '500',
            display: 'flex',
            alignItems: 'center',
            gap: '6px',
            animation: 'fadeIn 0.3s ease-in'
          }}>
            <span style={{
              fontSize: '14px',
              display: 'flex',
              alignItems: 'center'
            }}>✗</span>
            {error}
          </div>
        )}

        {/* Progress Indicator */}
        {isLoading && (
          <div style={{
            flex: 1,
            minWidth: '200px',
            display: 'flex',
            alignItems: 'center',
            gap: '12px'
          }}>
            <div style={{
              flex: 1,
              height: '8px',
              backgroundColor: 'rgba(99, 102, 241, 0.15)',
              borderRadius: '4px',
              overflow: 'hidden',
              border: '1px solid rgba(99, 102, 241, 0.3)'
            }}>
              <div style={{
                width: `${progress}%`,
                height: '100%',
                background: 'linear-gradient(90deg, #6366f1 0%, #8b5cf6 100%)',
                transition: 'width 0.05s linear',
                boxShadow: '0 0 10px rgba(99, 102, 241, 0.5)'
              }} />
            </div>
            <span style={{
              fontSize: '13px',
              color: '#94a3b8',
              fontWeight: '500',
              minWidth: '45px'
            }}>
              {Math.round(progress)}%
            </span>
          </div>
        )}
      </div>

      {/* Map Container */}
      <div style={{
        flex: 1,
        overflow: 'hidden',
        position: 'relative',
        backgroundColor: '#0a0e1a'
      }}>
        <iframe
          ref={iframeRef}
          key={mapKey}
          src={`/drone_missions_map.html?t=${mapKey}`}
          style={{
            width: '100%',
            height: '100%',
            border: 'none',
            margin: 0,
            padding: 0,
            display: 'block'
          }}
          title="Drone Missions Map"
          sandbox="allow-scripts allow-same-origin"
          loading="lazy"
        />
      </div>
      </div>

      {/* Drone Management Panel */}
      <DronePanel
        drones={drones}
        maxCapacity={STANDARD_BATTERY_CAPACITY}
        onAddDrone={handleAddDrone}
        onRemoveDrone={handleRemoveDrone}
        onUpdateCapacity={handleUpdateCapacity}
      />
    </div>
  );
};

export default DroneMissionsMap;
