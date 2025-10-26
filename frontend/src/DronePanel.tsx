import React from 'react';

export interface Drone {
  id: number;
  batteryCapacity: number;
}

interface DronePanelProps {
  drones: Drone[];
  maxCapacity: number;
  onAddDrone: () => void;
  onRemoveDrone: (id: number) => void;
  onUpdateCapacity: (id: number, capacity: number) => void;
}

const DronePanel: React.FC<DronePanelProps> = ({
  drones,
  maxCapacity,
  onAddDrone,
  onRemoveDrone,
  onUpdateCapacity
}) => {
  const canAddDrone = drones.length < 30;
  const canRemoveDrone = drones.length > 1;

  return (
    <div style={{
      width: '320px',
      height: '100%',
      backgroundColor: '#0f1420',
      borderLeft: '1px solid rgba(99, 102, 241, 0.2)',
      display: 'flex',
      flexDirection: 'column',
      overflow: 'hidden'
    }}>
      {/* Header */}
      <div style={{
        padding: '16px 20px',
        background: 'linear-gradient(135deg, #1a1f35 0%, #141824 100%)',
        borderBottom: '1px solid rgba(99, 102, 241, 0.2)',
        flexShrink: 0
      }}>
        <h2 style={{
          margin: 0,
          fontSize: '18px',
          fontWeight: '700',
          background: 'linear-gradient(135deg, #818cf8 0%, #c084fc 100%)',
          WebkitBackgroundClip: 'text',
          WebkitTextFillColor: 'transparent',
          backgroundClip: 'text',
          display: 'flex',
          alignItems: 'center',
          gap: '8px'
        }}>
          Drone Fleet Manager
        </h2>
        <p style={{
          margin: '6px 0 0 0',
          fontSize: '12px',
          color: '#94a3b8'
        }}>
          Total Drones: {drones.length} / 30
        </p>
      </div>

      {/* Drone List */}
      <div style={{
        flex: 1,
        overflowY: 'auto',
        padding: '12px'
      }}>
        {drones.map((drone, index) => (
          <div
            key={drone.id}
            style={{
              marginBottom: '12px',
              padding: '14px',
              background: 'linear-gradient(135deg, #1a1f35 0%, #141824 100%)',
              borderRadius: '8px',
              border: '1px solid rgba(99, 102, 241, 0.2)',
              boxShadow: '0 2px 8px rgba(0, 0, 0, 0.2)'
            }}
          >
            <div style={{
              display: 'flex',
              justifyContent: 'space-between',
              alignItems: 'center',
              marginBottom: '10px'
            }}>
              <span style={{
                fontSize: '14px',
                fontWeight: '600',
                color: '#e2e8f0'
              }}>
                Drone #{index + 1}
              </span>
              <button
                onClick={() => onRemoveDrone(drone.id)}
                disabled={!canRemoveDrone}
                style={{
                  padding: '4px 10px',
                  fontSize: '12px',
                  fontWeight: '600',
                  color: canRemoveDrone ? '#f87171' : '#4b5563',
                  backgroundColor: canRemoveDrone ? 'rgba(239, 68, 68, 0.12)' : 'rgba(75, 85, 99, 0.12)',
                  border: `1px solid ${canRemoveDrone ? 'rgba(239, 68, 68, 0.3)' : 'rgba(75, 85, 99, 0.3)'}`,
                  borderRadius: '4px',
                  cursor: canRemoveDrone ? 'pointer' : 'not-allowed',
                  transition: 'all 0.2s'
                }}
                onMouseEnter={(e) => {
                  if (canRemoveDrone) {
                    e.currentTarget.style.backgroundColor = 'rgba(239, 68, 68, 0.2)';
                  }
                }}
                onMouseLeave={(e) => {
                  if (canRemoveDrone) {
                    e.currentTarget.style.backgroundColor = 'rgba(239, 68, 68, 0.12)';
                  }
                }}
              >
                Remove
              </button>
            </div>

            <div style={{ marginBottom: '8px' }}>
              <label style={{
                display: 'block',
                fontSize: '12px',
                color: '#94a3b8',
                marginBottom: '6px'
              }}>
                Battery Capacity (ft)
              </label>
              <input
                type="number"
                min={0}
                max={maxCapacity}
                value={drone.batteryCapacity}
                onChange={(e) => {
                  const value = Math.max(0, Math.min(maxCapacity, parseInt(e.target.value) || 0));
                  onUpdateCapacity(drone.id, value);
                }}
                style={{
                  width: '100%',
                  padding: '8px 12px',
                  fontSize: '14px',
                  backgroundColor: '#0a0e1a',
                  border: '1px solid rgba(99, 102, 241, 0.3)',
                  borderRadius: '6px',
                  color: '#e2e8f0',
                  outline: 'none'
                }}
                onFocus={(e) => {
                  e.currentTarget.style.border = '1px solid rgba(99, 102, 241, 0.6)';
                  e.currentTarget.style.boxShadow = '0 0 0 3px rgba(99, 102, 241, 0.1)';
                }}
                onBlur={(e) => {
                  e.currentTarget.style.border = '1px solid rgba(99, 102, 241, 0.3)';
                  e.currentTarget.style.boxShadow = 'none';
                }}
              />
            </div>

            <div style={{
              marginTop: '8px',
              height: '6px',
              backgroundColor: 'rgba(99, 102, 241, 0.15)',
              borderRadius: '3px',
              overflow: 'hidden'
            }}>
              <div style={{
                width: `${(drone.batteryCapacity / maxCapacity) * 100}%`,
                height: '100%',
                background: 'linear-gradient(90deg, #10b981 0%, #34d399 100%)',
                transition: 'width 0.3s ease'
              }} />
            </div>
            <div style={{
              marginTop: '4px',
              fontSize: '11px',
              color: '#94a3b8',
              textAlign: 'right'
            }}>
              {((drone.batteryCapacity / maxCapacity) * 100).toFixed(1)}% capacity
            </div>
          </div>
        ))}
      </div>

      {/* Add Drone Button */}
      <div style={{
        padding: '12px',
        borderTop: '1px solid rgba(99, 102, 241, 0.2)',
        background: 'linear-gradient(135deg, #1a1f35 0%, #0f1420 100%)',
        flexShrink: 0
      }}>
        <button
          onClick={onAddDrone}
          disabled={!canAddDrone}
          style={{
            width: '100%',
            padding: '12px',
            fontSize: '14px',
            fontWeight: '600',
            color: 'white',
            background: canAddDrone
              ? 'linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%)'
              : 'linear-gradient(135deg, #374151 0%, #1f2937 100%)',
            border: 'none',
            borderRadius: '6px',
            cursor: canAddDrone ? 'pointer' : 'not-allowed',
            transition: 'all 0.3s',
            boxShadow: canAddDrone
              ? '0 4px 12px rgba(99, 102, 241, 0.3)'
              : 'none'
          }}
          onMouseEnter={(e) => {
            if (canAddDrone) {
              e.currentTarget.style.transform = 'translateY(-2px)';
              e.currentTarget.style.boxShadow = '0 6px 20px rgba(99, 102, 241, 0.4)';
            }
          }}
          onMouseLeave={(e) => {
            if (canAddDrone) {
              e.currentTarget.style.transform = 'translateY(0)';
              e.currentTarget.style.boxShadow = '0 4px 12px rgba(99, 102, 241, 0.3)';
            }
          }}
        >
          {canAddDrone ? '+ Add Drone' : 'Maximum Drones Reached (30)'}
        </button>
      </div>
    </div>
  );
};

export default DronePanel;
