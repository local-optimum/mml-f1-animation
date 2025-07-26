#!/usr/bin/env python3
"""
Extract F1 coordinate data for drivers 4, 81, and 27 from 2025 Silverstone race.
Scales coordinates by 1/1000 and downsamples to 1 position per second.
"""

import fastf1
import fastf1.plotting
import pandas as pd
import numpy as np
from datetime import datetime
import json

# Enable cache for faster subsequent runs
fastf1.Cache.enable_cache('cache')

def extract_driver_coordinates(driver_number, session):
    """Extract coordinates for a specific driver from the session."""
    try:
        # Get position data directly from session
        position_data = session.pos_data
        
        if position_data is None:
            print(f"No position data found for driver {driver_number}")
            return []
        
        # Position data is a dictionary with driver numbers as keys
        driver_key = str(driver_number)
        if driver_key not in position_data:
            print(f"No position data found for driver {driver_number}")
            return []
        
        driver_data = position_data[driver_key]
        
        if driver_data.empty:
            print(f"No position data found for driver {driver_number}")
            return []
        
        print(f"Found {len(driver_data)} position records for driver {driver_number}")
        
        # Sort by timestamp
        driver_data = driver_data.sort_values('Time')
        
        # Downsample to 1 position per second
        driver_data['second'] = driver_data['Time'].dt.floor('s')
        downsampled = driver_data.groupby('second').first().reset_index()
        
        # Extract coordinates and scale by 1/1000
        coordinates = []
        for _, row in downsampled.iterrows():
            # Check if we have valid position data
            if pd.notna(row['X']) and pd.notna(row['Y']) and pd.notna(row['Z']):
                x, y, z = float(row['X']) / 1000, float(row['Y']) / 1000, float(row['Z']) / 1000
                # Filter out (0,0,0) coordinates which indicate no movement
                if x != 0 or y != 0 or z != 0:
                    coord = {
                        'x': x,
                        'y': z,  # Swap Y and Z - F1 Z becomes MML Y (up)
                        'z': y   # F1 Y becomes MML Z (forward/backward)
                    }
                    coordinates.append(coord)
        
        print(f"Extracted {len(coordinates)} non-zero coordinates for driver {driver_number}")
        return coordinates
        
    except Exception as e:
        print(f"Error extracting data for driver {driver_number}: {e}")
        return []

def main():
    """Main function to extract F1 coordinates and generate the JS file."""
    
    # Load the 2025 Silverstone race session
    print("Loading 2025 Silverstone race session...")
    try:
        session = fastf1.get_session(2025, 'British Grand Prix', 'R')
        session.load()
        print("Session loaded successfully!")
    except Exception as e:
        print(f"Error loading session: {e}")
        print("Note: 2025 data might not be available yet. Trying 2024...")
        try:
            session = fastf1.get_session(2024, 'British Grand Prix', 'R')
            session.load()
            print("2024 session loaded successfully!")
        except Exception as e2:
            print(f"Error loading 2024 session: {e2}")
            return
    
    # Extract coordinates for drivers 4, 81, and 27
    drivers = [4, 81, 27]
    all_coordinates = []
    
    for driver in drivers:
        print(f"\nExtracting data for driver {driver}...")
        coords = extract_driver_coordinates(driver, session)
        all_coordinates.append(coords)
    
    # Find the minimum length to ensure all arrays have the same number of coordinates
    min_length = min(len(coords) for coords in all_coordinates if coords)
    
    if min_length == 0:
        print("No valid coordinate data found!")
        return
    
    # Truncate all arrays to the minimum length
    for i in range(len(all_coordinates)):
        all_coordinates[i] = all_coordinates[i][:min_length]
    
    print(f"\nFinal coordinate arrays: {min_length} positions each")
    
    # Generate the JavaScript file
    js_content = f"""// F1 coordinate data for drivers 4, 81, and 27 from Silverstone race
// Coordinates scaled by 1/1000 and filtered to remove stationary positions
// Time steps are 1/60th of a second apart (60x speed replay)

// Cube coordinates array - accessible globally
const cubeCoordinates = [
  // Cube 1 coordinates (driver 4) - F1 telemetry data
  {json.dumps(all_coordinates[0], indent=2)},
  
  // Cube 2 coordinates (driver 81) - F1 telemetry data  
  {json.dumps(all_coordinates[1], indent=2)},
  
  // Cube 3 coordinates (driver 27) - F1 telemetry data
  {json.dumps(all_coordinates[2], indent=2)}
];

// Configuration for the coordinate system - accessible globally
const coordinateConfig = {{
  timeStepDuration: 33.33, // 1/30th of a second per step in milliseconds (30x speed)
  totalTimeSteps: cubeCoordinates[0].length,
  updateInterval: 50, // Update frequency in milliseconds (20 times per second)
}};

// Helper function to get coordinates for a specific time step
function getCoordinatesAtTimeStep(timeStep) {{
  return cubeCoordinates.map(cubeCoords => cubeCoords[timeStep]);
}}

// Helper function to get the current time step based on document time
function getCurrentTimeStep(currentTime) {{
  return Math.floor(currentTime / coordinateConfig.timeStepDuration) % coordinateConfig.totalTimeSteps;
}}
"""
    
    # Write to f1-coordinates.js file
    with open('assets/f1-coordinates.js', 'w') as f:
        f.write(js_content)
    
    print(f"\n✅ Generated assets/f1-coordinates.js with {min_length} coordinate positions")
    print("Drivers mapped:")
    print("  - Cube 1 (red): Driver 4")
    print("  - Cube 2 (teal): Driver 81") 
    print("  - Cube 3 (blue): Driver 27")

if __name__ == "__main__":
    main() 