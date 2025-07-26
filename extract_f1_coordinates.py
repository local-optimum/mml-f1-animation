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

def get_f1_driver_abbreviation(driver_name):
    """Convert driver name to F1-style 3-letter abbreviation."""
    # F1 driver abbreviations mapping
    driver_abbreviations = {
        'Max Verstappen': 'VER',
        'Lewis Hamilton': 'HAM',
        'Lando Norris': 'NOR',
        'Oscar Piastri': 'PIA',
        'Nico Hulkenberg': 'HUL',
        'Pierre Gasly': 'GAS',
        'Lance Stroll': 'STR',
        'Alexander Albon': 'ALB',
        'Fernando Alonso': 'ALO',
        'George Russell': 'RUS',
        'Oliver Bearman': 'BEA',
        'Carlos Sainz': 'SAI',
        'Esteban Ocon': 'OCO',
        'Charles Leclerc': 'LEC',
        'Yuki Tsunoda': 'TSU',
        'Kimi Antonelli': 'ANT',
        'Isack Hadjar': 'HAD',
        'Gabriel Bortoleto': 'BOR',
        'Liam Lawson': 'LAW',
        'Franco Colapinto': 'COL'
    }
    
    return driver_abbreviations.get(driver_name, driver_name[:3].upper())

def extract_driver_coordinates(driver_number, session):
    """Extract coordinates for a specific driver from the session."""
    try:
        # Get position data for the driver
        driver_data = session.pos_data[driver_number]
        
        if driver_data is None or driver_data.empty:
            print(f"No position data found for driver {driver_number}")
            return {
                'coordinates': [],
                'driver_number': driver_number,
                'driver_name': f"Driver {driver_number}",
                'driver_abbreviation': f"DRV{driver_number}",
                'team_name': "Unknown",
                'team_color': "#cccccc"
            }
        
        print(f"Found {len(driver_data)} position records for driver {driver_number}")
        
        # Get driver info
        driver_info = session.get_driver(driver_number)
        full_name = f"{driver_info.FirstName} {driver_info.LastName}"
        driver_abbreviation = get_f1_driver_abbreviation(full_name)
        
        # Downsample to 1 position per second using the Date column
        driver_data['second'] = pd.to_datetime(driver_data['Date']).dt.floor('s')
        downsampled = driver_data.groupby('second').first().reset_index()
        
        # Extract coordinates and scale by 1/100
        coordinates = []
        for _, row in downsampled.iterrows():
            # Check if we have valid position data
            if pd.notna(row['X']) and pd.notna(row['Y']) and pd.notna(row['Z']):
                x, y, z = float(row['X']) / 100, float(row['Y']) / 100, float(row['Z']) / 100
                # Filter out (0,0,0) coordinates which indicate no movement
                if x != 0 or y != 0 or z != 0:
                    coord = {
                        'x': x,
                        'y': z,  # Swap Y and Z - F1 Z becomes MML Y (up)
                        'z': y   # F1 Y becomes MML Z (forward/backward)
                    }
                    coordinates.append(coord)
        
        print(f"Extracted {len(coordinates)} non-zero coordinates for driver {driver_number}")
        
        return {
            'coordinates': coordinates,
            'driver_number': driver_number,
            'driver_name': full_name,
            'driver_abbreviation': driver_abbreviation,
            'team_name': driver_info.TeamName,
            'team_color': get_team_color(driver_info.TeamName)
        }
        
    except Exception as e:
        print(f"Error extracting data for driver {driver_number}: {e}")
        return {
            'coordinates': [],
            'driver_number': driver_number,
            'driver_name': f"Driver {driver_number}",
            'driver_abbreviation': f"DRV{driver_number}",
            'team_name': "Unknown",
            'team_color': "#cccccc"
        }

def get_team_color(team_name):
    """Get the primary color for each F1 team."""
    team_colors = {
        'Red Bull Racing': '#3671C6',      # Red Bull Blue
        'Ferrari': '#F91536',              # Ferrari Red
        'McLaren': '#FF8700',              # McLaren Orange
        'Mercedes': '#6CD3BF',             # Mercedes Teal
        'Aston Martin': '#358C75',         # Aston Martin Green
        'Alpine': '#2293D1',               # Alpine Blue
        'Williams': '#37BEDD',             # Williams Blue
        'Visa Cash App RB': '#5E8FAA',     # RB Blue
        'Stake F1 Team Kick Sauber': '#52E252',  # Sauber Green
        'Haas F1 Team': '#B6BABD',         # Haas Gray
        'Force India': '#F596C8',          # Force India Pink (historical)
        'Toro Rosso': '#469BFF',           # Toro Rosso Blue (historical)
        'Racing Point': '#F596C8',         # Racing Point Pink (historical)
        'Alfa Romeo': '#C92D4B',           # Alfa Romeo Red (historical)
        'AlphaTauri': '#5E8FAA',           # AlphaTauri Blue (historical)
    }
    
    return team_colors.get(team_name, '#cccccc')  # Default gray for unknown teams

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
    
    # Get all available drivers from the session
    all_drivers = list(session.pos_data.keys())
    print(f"Found {len(all_drivers)} drivers in the race: {all_drivers}")
    
    # Extract coordinates for all drivers
    all_coordinates = []
    
    for driver in all_drivers:
        print(f"\nExtracting data for driver {driver}...")
        coords = extract_driver_coordinates(driver, session)
        all_coordinates.append(coords)
    
    # Find the minimum length to ensure all arrays have the same number of coordinates
    min_length = min(len(coords['coordinates']) for coords in all_coordinates if coords['coordinates'])
    
    if min_length == 0:
        print("No valid coordinate data found!")
        return
    
    # Truncate all arrays to the minimum length
    for i in range(len(all_coordinates)):
        all_coordinates[i]['coordinates'] = all_coordinates[i]['coordinates'][:min_length]
    
    print(f"\nFinal coordinate arrays: {min_length} positions each for {len(all_drivers)} drivers")
    
    # Generate the JavaScript file
    js_content = f"""// F1 coordinate data for ALL drivers from Silverstone race
// Coordinates scaled by 1/100 and filtered to remove stationary positions
// Time steps are 1/30th of a second apart (30x speed replay)

// Driver information array - accessible globally
const driverInfo = [
"""
    
    # Add driver information for each driver
    for i, driver_data in enumerate(all_coordinates):
        js_content += f"  // Driver {driver_data['driver_number']} info\n"
        js_content += f"  {{\n"
        js_content += f"    driver_number: {driver_data['driver_number']},\n"
        js_content += f"    driver_name: \"{driver_data['driver_name']}\",\n"
        js_content += f"    driver_abbreviation: \"{driver_data['driver_abbreviation']}\",\n"
        js_content += f"    team_name: \"{driver_data['team_name']}\",\n"
        js_content += f"    team_color: \"{driver_data['team_color']}\"\n"
        js_content += f"  }},\n\n"
    
    js_content += f"""];

// Cube coordinates array - accessible globally
const cubeCoordinates = [
"""
    
    # Add coordinates for each driver
    for i, driver_data in enumerate(all_coordinates):
        js_content += f"  // Cube {i+1} coordinates (driver {driver_data['driver_number']}) - F1 telemetry data\n"
        js_content += f"  {json.dumps(driver_data['coordinates'], indent=2)},\n\n"
    
    js_content += f"""];

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
    print(f"All {len(all_drivers)} drivers mapped to cubes:")
    for i, driver_data in enumerate(all_coordinates):
        print(f"  - Cube {i+1}: Driver {driver_data['driver_number']} ({driver_data['driver_name']}) - Team: {driver_data['team_name']} (Color: {driver_data['team_color']})")

if __name__ == "__main__":
    main() 