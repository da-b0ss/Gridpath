# Comprehensive Frontend Documentation

## Table of Contents
1. [Overview](#overview)
2. [Directory Structure](#directory-structure)
3. [Folder Hierarchy & File Organization](#folder-hierarchy--file-organization)
4. [File Types](#file-types)
5. [Key Files & Their Purposes](#key-files--their-purposes)
6. [Dependencies & Imports](#dependencies--imports)
7. [Configuration Setup](#configuration-setup)
8. [Special Patterns & Architecture](#special-patterns--architecture)
9. [Build Tooling Summary](#build-tooling-summary)
10. [Development Workflow](#development-workflow)
11. [Integration Points](#integration-points)
12. [Key Metrics](#key-metrics)

---

## Overview

This is a **modern, type-safe React 19 application** using **Vite** as the build tool. It features a **dark-themed dashboard** for managing drone missions with real-time visualization, fleet management capabilities, and backend API integration.

**Key Statistics:**
- **Source Code**: 747 lines of TypeScript/TSX
- **Components**: 3 main React components
- **Dependencies**: 41 npm packages (2 runtime, 5 dev)
- **Total Size**: 78MB (mostly node_modules)
- **Public Assets**: 4.9MB Plotly visualization

---

## Directory Structure

```
frontend/
├── public/
│   └── drone_missions_map.html          # 4.9MB Plotly visualization (embedded via iframe)
├── src/
│   ├── App.tsx                          # 75 lines - Main app component
│   ├── DroneMissionsMap.tsx             # 316 lines - Map component with drone management
│   ├── DronePanel.tsx                   # 238 lines - Drone fleet management UI
│   ├── index.tsx                        # 117 lines - App entry point with global styles
│   └── vite-env.d.ts                    # 1 line - Vite type definitions
├── index.html                           # HTML template with root div and script
├── package.json                         # Project metadata and dependencies
├── package-lock.json                    # Locked dependency versions
├── tsconfig.json                        # TypeScript compiler options
├── tsconfig.node.json                   # TypeScript config for Vite
├── vite.config.ts                       # Vite bundler configuration
├── README.md                            # Usage documentation
├── INTEGRATION_SUMMARY.md               # Integration notes
└── node_modules/                        # 41 dependencies installed
```

---

## Folder Hierarchy & File Organization

### Root Level Files (Configuration & Documentation)

| File | Purpose | Type |
|------|---------|------|
| `package.json` | Project metadata, scripts, dependencies | Config |
| `tsconfig.json` | TypeScript compiler options | Config |
| `tsconfig.node.json` | TypeScript config for Vite | Config |
| `vite.config.ts` | Vite bundler configuration | Config |
| `index.html` | Main HTML template | HTML |
| `README.md` | User documentation | Markdown |
| `INTEGRATION_SUMMARY.md` | Integration notes | Markdown |

### `/src` Directory (Source Code)

TypeScript React components using TSX syntax (747 total lines):

| File | Lines | Purpose |
|------|-------|---------|
| `index.tsx` | 117 | Entry point with global dark theme styling |
| `App.tsx` | 75 | Main application component with header |
| `DroneMissionsMap.tsx` | 316 | Map visualization with API integration and progress tracking |
| `DronePanel.tsx` | 238 | Drone fleet management sidebar |
| `vite-env.d.ts` | 1 | Vite type definition file |

### `/public` Directory (Static Assets)

| File | Size | Purpose |
|------|------|---------|
| `drone_missions_map.html` | 4.9MB | Complete Plotly visualization with MapLibre GL JS embedded |

---

## File Types

**Source Code Files:**
- `.tsx` - React TypeScript components (4 files)
- `.ts` - TypeScript files (1 config file: vite.config.ts, 1 type def)

**Configuration Files:**
- `.json` - package.json, tsconfig.json, tsconfig.node.json, package-lock.json
- `.ts` - vite.config.ts (ESM module configuration)

**Documentation:**
- `.md` - README.md, INTEGRATION_SUMMARY.md

**HTML & Templates:**
- `.html` - index.html (main template), drone_missions_map.html (Plotly viz)

**Dependencies:**
- `node_modules/` - 41 npm packages installed

---

## Key Files & Their Purposes

### A. Entry Points

#### `index.html`

```
Location: /home/ahern/KnightHacks/The-Seeker/frontend/index.html
Lines: 18
Purpose: Main HTML template
```

**Key Elements:**
- Root `div` with id="root" for React mounting
- Links to Vite module script
- Meta tags for viewport and theme color
- Title: "Drone Missions Map"

#### `src/index.tsx`

```
Location: /home/ahern/KnightHacks/The-Seeker/frontend/src/index.tsx
Lines: 117
Purpose: React application entry point with global styling
```

**Key Features:**
- Imports React 19 and ReactDOM
- Mounts App component to #root DOM element
- Injects global CSS styling via `document.createElement('style')`

**Global Styling Includes:**
- Dark theme (background: #0a0e1a, text: #e2e8f0)
- Custom scrollbar (gradient purple)
- Animations: fadeIn, pulse, slideIn, glow
- Focus & selection styling
- 100vh fullscreen layout

### B. Component Files

#### `src/App.tsx`

```
Location: /home/ahern/KnightHacks/The-Seeker/frontend/src/App.tsx
Lines: 75
Purpose: Root application component
```

**Structure:**
- Renders a 100vh container with flexbox layout
- **Header section:**
  - Dark gradient background (linear-gradient(135deg, #1a1f35 0%, #0f1420 100%))
  - Title: "🚁 Drone Missions Visualization"
  - Subtitle: "Real-time mission tracking and flight zone visualization"
  - Decorative top border with indigo gradient
  - Icon with glow effect
- **Main content area:**
  - Renders DroneMissionsMap component (full width/height)

#### `src/DroneMissionsMap.tsx`

```
Location: /home/ahern/KnightHacks/The-Seeker/frontend/src/DroneMissionsMap.tsx
Lines: 316
Purpose: Main drone missions map component with fleet management
```

**Props Interface:**
```typescript
interface DroneMissionsMapProps {
  width?: string | number;           // Default: '100%'
  height?: string | number;          // Default: '100vh'
  apiUrl?: string;                   // Default: 'http://localhost:5000'
}
```

**Key Features:**

1. **Drone Fleet Management:**
   - Maintain array of drones with battery capacity
   - Add drones (max 30)
   - Remove drones (min 1)
   - Update battery capacity per drone
   - Default drone: `{ id: 1, batteryCapacity: 37725 }`

2. **State Management:**
   - `drones[]` - Array of drone objects
   - `isLoading` - Loading state during API calls
   - `error` - Error message display
   - `message` - Success message display
   - `progress` - Progress bar percentage (0-100%)
   - `mapKey` - Force iframe refresh

3. **API Integration:**
   - Endpoint: `POST /api/run-pipeline` (at apiUrl)
   - Sends: `{ fleet_capacities: [battery_values] }`
   - 30-second timeout (SEARCH_TIME_LIMIT_SECONDS)
   - Animated progress bar matching timeout duration

4. **UI Layout (Flexbox row):**
   - **Left section (flex: 1):**
     - Control panel with buttons and status messages
     - Iframe displaying drone_missions_map.html
   - **Right section (320px):**
     - DronePanel component for fleet management

5. **Constants:**
   - `SEARCH_TIME_LIMIT_SECONDS = 30` (matches backend routing.py)
   - `STANDARD_BATTERY_CAPACITY = 37725` (matches backend config.py)

6. **Handlers:**
   - `handleAddDrone()` - Create new drone
   - `handleRemoveDrone(id)` - Delete drone by id
   - `handleUpdateCapacity(id, capacity)` - Update battery value
   - `refreshDisplay()` - Trigger API call and iframe refresh

#### `src/DronePanel.tsx`

```
Location: /home/ahern/KnightHacks/The-Seeker/frontend/src/DronePanel.tsx
Lines: 238
Purpose: Drone fleet management sidebar
```

**Exports:**
- `DronePanel` component (default export)
- `Drone` interface: `{ id: number; batteryCapacity: number }`

**Props Interface:**
```typescript
interface DronePanelProps {
  drones: Drone[];
  maxCapacity: number;
  onAddDrone: () => void;
  onRemoveDrone: (id: number) => void;
  onUpdateCapacity: (id: number, capacity: number) => void;
}
```

**UI Layout (320px wide sidebar):**

1. **Header section (fixed):**
   - Title: "Drone Fleet Manager"
   - Subtitle: "Total Drones: X / 30"
   - Gradient background

2. **Scrollable drone list:**
   - Card for each drone with:
     - Drone name (Drone #1, #2, etc.)
     - Remove button (disabled if only 1 drone)
     - Battery capacity input field (0 to maxCapacity)
     - Green capacity bar with percentage
     - Percentage display (X.X% capacity)

3. **Add Drone button (fixed bottom):**
   - Gradient purple button
   - Disabled when 30 drones reached
   - Shows "Maximum Drones Reached (30)" when full

**Styling:**
- 320px fixed width
- Dark theme matching main app
- Indigo/purple gradient accents
- Green battery indicator bars
- Hover effects on buttons
- Border left separator (indigo)

### C. Configuration Files

#### `package.json`

```
Location: /home/ahern/KnightHacks/The-Seeker/frontend/package.json
Type: ESM module
Name: drone-missions-map
Version: 1.0.0
```

**Scripts:**
```json
{
  "start": "vite",                    // Start dev server
  "dev": "vite",                      // Same as start
  "build": "tsc && vite build",       // TypeScript check + Vite build
  "preview": "vite preview"           // Preview production build
}
```

**Runtime Dependencies:**
- `react`: ^19.2.0
- `react-dom`: ^19.2.0

**Dev Dependencies:**
- `@types/react`: ^18.2.0 - React type definitions
- `@types/react-dom`: ^18.2.0 - ReactDOM type definitions
- `@vitejs/plugin-react`: ^4.2.0 - Vite React plugin with JSX
- `typescript`: ^5.3.0 - TypeScript compiler
- `vite`: ^5.0.0 - Build tool & dev server

#### `tsconfig.json`

**Compiler Options:**
```json
{
  "compilerOptions": {
    "target": "ES2020",              // Modern JavaScript output
    "lib": ["ES2020", "DOM", "DOM.Iterable"],  // Include DOM APIs
    "module": "ESNext",              // ES modules
    "jsx": "react-jsx",              // React 17+ JSX transform
    "moduleResolution": "bundler",   // Vite/Rollup resolution

    // Strict Mode
    "strict": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noFallthroughCasesInSwitch": true,

    // Other Settings
    "skipLibCheck": true,
    "isolatedModules": true,
    "noEmit": true,
    "resolveJsonModule": true,
    "allowImportingTsExtensions": true
  },
  "include": ["src"],
  "references": [{"path": "./tsconfig.node.json"}]
}
```

#### `vite.config.ts`

```typescript
// Location: /home/ahern/KnightHacks/The-Seeker/frontend/vite.config.ts
// Lines: 15

import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],              // Vite React plugin

  server: {
    port: 3000,                    // Dev server port
    open: true                     // Auto-open browser
  },

  build: {
    outDir: 'dist',               // Output directory
    sourcemap: true               // Generate source maps
  }
})
```

#### `tsconfig.node.json`

```
Location: /home/ahern/KnightHacks/The-Seeker/frontend/tsconfig.node.json
Lines: 10
Purpose: TypeScript config for Vite configuration files
```

**Options:**
- `composite: true` - Part of monorepo setup
- `skipLibCheck: true` - Skip type checking
- `module: ESNext`
- `moduleResolution: bundler`
- `allowSyntheticDefaultImports: true`
- Include: `["vite.config.ts"]`

#### `src/vite-env.d.ts`

```
Location: /home/ahern/KnightHacks/The-Seeker/frontend/src/vite-env.d.ts
Lines: 1

Content:
/// <reference types="vite/client" />
```

**Purpose:** TypeScript type definitions for Vite client-side imports

**Enables:** Vite-specific features like `import.meta.hot`

### D. Public Assets

#### `public/drone_missions_map.html`

```
Location: /home/ahern/KnightHacks/The-Seeker/frontend/public/drone_missions_map.html
Size: 4.9MB
Type: Self-contained Plotly visualization
```

**Contents:**
- Embedded Plotly.js v3.1.1 library (complete, minified)
- MapLibre GL JS library
- Flight zone polygon coordinates (GeoJSON)
- Mission location data with clustering
- Interactive map with:
  - Zoom, pan, hover controls
  - Flight zone overlay
  - Mission markers
  - Clustering on zoom
  - Satellite/terrain/vector base maps

**Embedded in App as:**
```jsx
<iframe
  src="/drone_missions_map.html"
  style={{ width: '100%', height: '100%', border: 'none' }}
  title="Drone Missions Map"
  sandbox="allow-scripts allow-same-origin"
  loading="lazy"
/>
```

---

## Dependencies & Imports

### npm Dependencies (41 packages total)

**Runtime Dependencies:**
- `react` v19.2.0 - UI library
- `react-dom` v19.2.0 - React DOM rendering

**Dev Dependencies:**
- `@types/react` v18.2.0 - React type definitions
- `@types/react-dom` v18.2.0 - ReactDOM type definitions
- `@vitejs/plugin-react` v4.2.0 - Vite React integration
- `typescript` v5.3.0 - TypeScript compiler
- `vite` v5.0.0 - Build tool/dev server

**Transitive Dependencies (30+ additional):**
- Babel ecosystem (@babel/*)
- PostCSS for CSS processing
- Rollup for bundling
- Source map utilities
- Browser compatibility libraries (browserslist, caniuse-lite)

### Import Statements in Components

**src/index.tsx:**
```typescript
import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';
```

**src/App.tsx:**
```typescript
import React from 'react';
import DroneMissionsMap from './DroneMissionsMap';
```

**src/DroneMissionsMap.tsx:**
```typescript
import React, { useEffect, useRef, useState } from 'react';
import DronePanel, { Drone } from './DronePanel';
```

**src/DronePanel.tsx:**
```typescript
import React from 'react';
// Exports: Drone interface
```

### No External UI Libraries

- No Material-UI, Tailwind, Bootstrap, etc.
- All styling done with inline React style objects
- Custom CSS animations in global styles
- Dark theme colors hardcoded in components

---

## Configuration Setup

### Development Workflow

**Starting Development:**
```bash
npm run dev  # Starts Vite at http://localhost:3000
```

**Building for Production:**
```bash
npm run build  # TypeScript check + Vite build → dist/
```

**Preview Build:**
```bash
npm run preview  # Preview dist/ locally
```

### TypeScript Configuration

- **Target**: ES2020 (modern browsers)
- **Strict Mode**: Fully enabled
- **Module System**: ESNext (ES modules)
- **JSX Transform**: React 17+ auto-import (no React import needed in files)

### Build Output

- **Format**: ESM (JavaScript modules)
- **Output Directory**: `dist/`
- **Source Maps**: Enabled for debugging
- **Code Splitting**: Handled by Vite

### Vite Specific Features

- **Fast Refresh**: Hot Module Replacement on save
- **Plugin System**: @vitejs/plugin-react for React JSX support
- **Esbuild**: Rust-based TypeScript transpiler (faster than Babel)

---

## Special Patterns & Architecture

### A. Component Architecture Pattern

**Container/Presentational Split:**

```
App.tsx (Container)
  └─ DroneMissionsMap.tsx (Container + Presentational)
      ├─ Control Panel (Presentational)
      ├─ Iframe with Plotly (Visualization)
      └─ DronePanel.tsx (Presentational)
```

### B. State Management Pattern

**Local Component State (No Redux/Context):**
```typescript
// DroneMissionsMap.tsx
const [drones, setDrones] = useState<Drone[]>([...])
const [isLoading, setIsLoading] = useState(false)
const [error, setError] = useState<string | null>(null)
const [message, setMessage] = useState<string | null>(null)
const [progress, setProgress] = useState(0)
const [mapKey, setMapKey] = useState(Date.now())
```

**Lift State Up Pattern:**
- Parent (DroneMissionsMap) manages drone fleet state
- Handlers passed as props to DronePanel
- Single source of truth for drone data

### C. API Integration Pattern

**Fetch-based HTTP Requests:**
```typescript
const refreshDisplay = async () => {
  try {
    const response = await fetch(`${apiUrl}/api/run-pipeline`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ fleet_capacities: fleetCapacities })
    });
    const data = await response.json();
    // Handle response...
  } catch (err) {
    // Handle error...
  }
};
```

**Features:**
- Configurable API URL (default: http://localhost:5000)
- JSON request/response handling
- Error and success messaging
- Progress tracking with timeout

### D. Styling Pattern

**Inline Style Objects (No CSS Files):**
```typescript
style={{
  width: '100vw',
  height: '100vh',
  backgroundColor: '#0a0e1a',
  display: 'flex',
  flexDirection: 'column',
  // ... more properties
}}
```

**Global Styles via Injection:**
```typescript
const styleSheet = document.createElement('style');
styleSheet.textContent = `
  /* CSS string with animations, colors, scrollbars */
`;
document.head.appendChild(styleSheet);
```

**Design System Colors:**
- **Background**: #0a0e1a (very dark blue)
- **Secondary BG**: #0f1420, #1a1f35, #141824
- **Primary Accent**: #6366f1 (indigo)
- **Secondary Accent**: #8b5cf6 (violet)
- **Highlight**: #818cf8 (light indigo)
- **Text**: #e2e8f0 (light gray)
- **Muted Text**: #94a3b8 (slate gray)
- **Success**: #10b981, #34d399 (green)
- **Error**: #ef4444, #f87171 (red)

### E. Iframe Integration Pattern

**Isolated HTML Visualization:**
```typescript
<iframe
  ref={iframeRef}
  key={mapKey}
  src={`/drone_missions_map.html?t=${mapKey}`}
  style={{ width: '100%', height: '100%', border: 'none' }}
  title="Drone Missions Map"
  sandbox="allow-scripts allow-same-origin"
  loading="lazy"
/>
```

**Force Refresh Strategy:**
- Change `key` prop to remount iframe
- Update `mapKey` state on API success
- Adds timestamp query param to bypass cache

**Sandbox Attributes:**
- `allow-scripts` - Execute JavaScript in iframe
- `allow-same-origin` - Access same-origin resources
- Prevents access to parent window

### F. Type Safety Pattern

**TypeScript Interfaces:**
```typescript
interface DroneMissionsMapProps {
  width?: string | number;
  height?: string | number;
  apiUrl?: string;
}

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
```

**Type Annotations:**
- All props typed with interfaces
- All event handlers typed: `(e: React.ChangeEvent<HTMLInputElement>) => void`
- State variables typed: `useState<Drone[]>`, `useState<string | null>`

### G. Browser Event Handling Pattern

**Controlled Inputs:**
```typescript
<input
  type="number"
  value={drone.batteryCapacity}
  onChange={(e) => {
    const value = Math.max(0, Math.min(maxCapacity, parseInt(e.target.value) || 0));
    onUpdateCapacity(drone.id, value);
  }}
  onFocus={(e) => { /* visual feedback */ }}
  onBlur={(e) => { /* reset styling */ }}
/>
```

**Interactive Button States:**
```typescript
<button
  onClick={handleClick}
  disabled={isLoading}
  onMouseEnter={(e) => { /* hover effect */ }}
  onMouseLeave={(e) => { /* reset effect */ }}
>
  {isLoading ? 'Loading...' : 'Button Text'}
</button>
```

### H. Animation Pattern

**CSS Animations (Injected Global Styles):**
```css
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(-10px); }
  to { opacity: 1; transform: translateY(0); }
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.6; }
}

@keyframes slideIn {
  from { transform: translateX(-100%); opacity: 0; }
  to { transform: translateX(0); opacity: 1; }
}

@keyframes glow {
  0%, 100% { box-shadow: 0 0 5px rgba(99, 102, 241, 0.3); }
  50% { box-shadow: 0 0 20px rgba(99, 102, 241, 0.6); }
}
```

**Applied via inline style:**
```typescript
style={{ animation: 'fadeIn 0.3s ease-in' }}
style={{ animation: 'pulse 2s infinite' }} // For loading states
```

### I. Progress Tracking Pattern

**Time-Based Progress Animation:**
```typescript
useEffect(() => {
  if (isLoading) {
    const startTime = Date.now();
    const duration = SEARCH_TIME_LIMIT_SECONDS * 1000; // 30 seconds

    const interval = setInterval(() => {
      const elapsed = Date.now() - startTime;
      const newProgress = Math.min((elapsed / duration) * 100, 100);
      setProgress(newProgress);

      if (newProgress >= 100) clearInterval(interval);
    }, 50); // Update every 50ms for smooth animation

    return () => clearInterval(interval);
  }
}, [isLoading]);
```

**Renders Progress Bar:**
```typescript
<div style={{ width: `${progress}%`, height: '100%' }} />
<span>{Math.round(progress)}%</span>
```

### J. Constraints & Limits

**Fleet Constraints:**
```typescript
const canAddDrone = drones.length < 30;      // Max 30 drones
const canRemoveDrone = drones.length > 1;    // Min 1 drone
```

**Battery Constraints:**
```typescript
const value = Math.max(0, Math.min(maxCapacity, parseInt(e.target.value) || 0));
// Ensures: 0 <= value <= 37725
```

**API Constraints:**
```typescript
SEARCH_TIME_LIMIT_SECONDS = 30;              // Must match backend
STANDARD_BATTERY_CAPACITY = 37725;           // Must match backend config.py
```

---

## Build Tooling Summary

| Tool | Version | Purpose |
|------|---------|---------|
| Vite | ^5.0.0 | Dev server, bundler, HMR |
| TypeScript | ^5.3.0 | Type checking, transpilation |
| Esbuild | (via Vite) | Fast JS/TS transpiler |
| Rollup | (via Vite) | Module bundler |
| Babel | (transitive) | JSX plugin ecosystem |
| PostCSS | (transitive) | CSS processing |
| React | ^19.2.0 | UI library |
| React-DOM | ^19.2.0 | DOM rendering |

---

## Development Workflow

**Local Development:**
1. `npm install` - Install dependencies
2. `npm run dev` - Start Vite dev server on port 3000
3. Browser opens automatically with HMR enabled
4. Edit TSX files → browser reloads instantly

**Type Checking:**
- TypeScript compiler runs on save in IDE
- Build command: `npm run build` also runs `tsc` first

**Production Build:**
1. `npm run build` - Creates optimized dist/
2. Files are minified, chunked, and source-mapped
3. Ready for deployment to static host

---

## Integration Points

**Backend Connection:**
- API URL: `http://localhost:5000` (configurable)
- Endpoint: `POST /api/run-pipeline`
- Payload: `{ fleet_capacities: [battery_values] }`
- Response: `{ success: boolean, message?: string }`

**Public Visualization:**
- HTML file served from `public/` directory
- Embedded in iframe for isolation
- Can be updated without rebuilding React app
- Must be named `drone_missions_map.html`

**Global Styling:**
- Injected via `<style>` tag in index.tsx
- Affects entire page including iframe borders
- 117-line global stylesheet

---

## Key Metrics

| Metric | Value |
|--------|-------|
| Total Source Lines | 747 |
| Total Components | 3 (App, DroneMissionsMap, DronePanel) |
| TypeScript Files | 5 (.tsx + .ts + .d.ts) |
| Configuration Files | 5 (vite, tsconfig, package.json, etc) |
| Documentation Files | 2 (README, INTEGRATION_SUMMARY) |
| npm Dependencies | 41 total |
| Runtime Dependencies | 2 (React, ReactDOM) |
| Dev Dependencies | 5 (types, vite, typescript, plugin) |
| Frontend Directory Size | 78MB (mostly node_modules) |
| Plotly Visualization | 4.9MB single HTML file |
| Dev Server Port | 3000 |
| API Backend Port | 5000 |
| Maximum Drones | 30 |
| Default Battery Capacity | 37,725 (units) |
| API Timeout | 30 seconds |

---

## Summary

The frontend is a **modern, type-safe React 19 application** using **Vite** as the build tool. It features a **dark-themed dashboard** for managing drone missions with:

1. **Real-time Visualization** - Plotly maps embedded in iframe
2. **Fleet Management** - Add/remove drones, adjust battery capacities
3. **API Integration** - Send fleet config to backend for computation
4. **Progress Tracking** - Animated progress bar with 30-second timeout
5. **No External UI Libraries** - All custom styling with inline objects
6. **Full TypeScript** - Strict mode enabled for type safety
7. **Performance Optimized** - Vite for fast dev/build, lazy-loaded iframe

All components use **functional components with hooks**, **controlled inputs**, and **prop-based communication** following modern React best practices.
