
import sqlite3
import json
from datetime import datetime
import os

DATABASE_FILE = 'environmental_observations.db'

def init_database():
    """Initialize the database with all required tables"""
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    
    # Weather entries table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS weather_entries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            date TEXT NOT NULL,
            location TEXT NOT NULL,
            temperature REAL,
            humidity INTEGER,
            precipitation REAL,
            wind_speed REAL,
            conditions TEXT,
            notes TEXT
        )
    ''')
    
    # Plant entries table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS plant_entries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            date TEXT NOT NULL,
            preserve TEXT NOT NULL,
            species_name TEXT NOT NULL,
            common_name TEXT NOT NULL,
            location_details TEXT,
            abundance TEXT,
            flowering_status TEXT,
            habitat TEXT,
            notes TEXT
        )
    ''')
    
    # River entries table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS river_entries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            date TEXT NOT NULL,
            location TEXT NOT NULL,
            water_level TEXT,
            water_clarity TEXT,
            temperature REAL,
            flow_rate TEXT,
            wildlife_observed TEXT,
            pollution_indicators TEXT,
            notes TEXT
        )
    ''')
    
    # Lake entries table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS lake_entries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            date TEXT NOT NULL,
            lake_name TEXT NOT NULL,
            fishing_method TEXT,
            fish_species TEXT,
            fish_count INTEGER,
            fish_size_avg REAL,
            frogs_observed TEXT,
            turtles_observed TEXT,
            water_temperature REAL,
            water_clarity TEXT,
            notes TEXT
        )
    ''')
    
    # Animal entries table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS animal_entries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            date TEXT NOT NULL,
            location TEXT NOT NULL,
            species TEXT NOT NULL,
            common_name TEXT NOT NULL,
            number_observed INTEGER,
            behavior TEXT,
            habitat TEXT,
            time_of_day TEXT,
            weather_conditions TEXT,
            notes TEXT
        )
    ''')
    
    # Garbage can entries table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS garbage_can_entries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            date TEXT NOT NULL,
            location TEXT NOT NULL,
            garbage_can_type TEXT,
            fullness_level TEXT,
            ant_species TEXT,
            ant_colony_count INTEGER,
            ant_activity_level TEXT,
            weather_conditions TEXT,
            temperature REAL,
            time_of_day TEXT,
            notes TEXT
        )
    ''')
    
    # Sodium Trap / GUD entries table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS gud_entries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            date TEXT NOT NULL,
            site_type TEXT NOT NULL, -- 'Control' or 'Experimental'
            mask_a INTEGER, -- 1-5 scale
            vis_score INTEGER, -- 1-5 scale
            dist_to_road REAL, -- meters to River Road
            transit_active BOOLEAN, -- Pace Bus idling
            predator_cues_human_dog INTEGER,
            predator_cues_alarm_calls INTEGER,
            sodium_multiplier REAL, -- Lambda (λ)
            notes TEXT
        )
    ''')
    
    conn.commit()
    conn.close()

class DatabaseManager:
    def __init__(self):
        init_database()
    
    def get_connection(self):
        return sqlite3.connect(DATABASE_FILE)
    
    # Weather entries methods
    def add_weather_entry(self, data):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO weather_entries 
            (timestamp, date, location, temperature, humidity, precipitation, wind_speed, conditions, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            datetime.now().isoformat(),
            data.get('date', ''),
            data.get('location', ''),
            float(data.get('temperature', 0)) if data.get('temperature') else None,
            int(data.get('humidity', 0)) if data.get('humidity') else None,
            float(data.get('precipitation', 0)) if data.get('precipitation') else None,
            float(data.get('wind_speed', 0)) if data.get('wind_speed') else None,
            data.get('conditions', ''),
            data.get('notes', '')
        ))
        
        conn.commit()
        conn.close()
    
    def get_weather_entries(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM weather_entries ORDER BY timestamp DESC')
        rows = cursor.fetchall()
        
        entries = []
        for row in rows:
            entries.append({
                'id': row[0],
                'timestamp': row[1],
                'date': row[2],
                'location': row[3],
                'temperature': row[4],
                'humidity': row[5],
                'precipitation': row[6],
                'wind_speed': row[7],
                'conditions': row[8],
                'notes': row[9]
            })
        
        conn.close()
        return entries
    
    # Plant entries methods
    def add_plant_entry(self, data):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO plant_entries 
            (timestamp, date, preserve, species_name, common_name, location_details, abundance, flowering_status, habitat, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            datetime.now().isoformat(),
            data.get('date', ''),
            data.get('preserve', ''),
            data.get('species_name', ''),
            data.get('common_name', ''),
            data.get('location_details', ''),
            data.get('abundance', ''),
            data.get('flowering_status', ''),
            data.get('habitat', ''),
            data.get('notes', '')
        ))
        
        conn.commit()
        conn.close()
    
    def get_plant_entries(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM plant_entries ORDER BY timestamp DESC')
        rows = cursor.fetchall()
        
        entries = []
        for row in rows:
            entries.append({
                'id': row[0],
                'timestamp': row[1],
                'date': row[2],
                'preserve': row[3],
                'species_name': row[4],
                'common_name': row[5],
                'location_details': row[6],
                'abundance': row[7],
                'flowering_status': row[8],
                'habitat': row[9],
                'notes': row[10]
            })
        
        conn.close()
        return entries
    
    # River entries methods
    def add_river_entry(self, data):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO river_entries 
            (timestamp, date, location, water_level, water_clarity, temperature, flow_rate, wildlife_observed, pollution_indicators, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            datetime.now().isoformat(),
            data.get('date', ''),
            data.get('location', ''),
            data.get('water_level', ''),
            data.get('water_clarity', ''),
            float(data.get('temperature', 0)) if data.get('temperature') else None,
            data.get('flow_rate', ''),
            data.get('wildlife_observed', ''),
            data.get('pollution_indicators', ''),
            data.get('notes', '')
        ))
        
        conn.commit()
        conn.close()
    
    def get_river_entries(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM river_entries ORDER BY timestamp DESC')
        rows = cursor.fetchall()
        
        entries = []
        for row in rows:
            entries.append({
                'id': row[0],
                'timestamp': row[1],
                'date': row[2],
                'location': row[3],
                'water_level': row[4],
                'water_clarity': row[5],
                'temperature': row[6],
                'flow_rate': row[7],
                'wildlife_observed': row[8],
                'pollution_indicators': row[9],
                'notes': row[10]
            })
        
        conn.close()
        return entries
    
    # Lake entries methods
    def add_lake_entry(self, data):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO lake_entries 
            (timestamp, date, lake_name, fishing_method, fish_species, fish_count, fish_size_avg, frogs_observed, turtles_observed, water_temperature, water_clarity, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            datetime.now().isoformat(),
            data.get('date', ''),
            data.get('lake_name', ''),
            data.get('fishing_method', ''),
            data.get('fish_species', ''),
            int(data.get('fish_count', 0)) if data.get('fish_count') else None,
            float(data.get('fish_size_avg', 0)) if data.get('fish_size_avg') else None,
            data.get('frogs_observed', ''),
            data.get('turtles_observed', ''),
            float(data.get('water_temperature', 0)) if data.get('water_temperature') else None,
            data.get('water_clarity', ''),
            data.get('notes', '')
        ))
        
        conn.commit()
        conn.close()
    
    def get_lake_entries(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM lake_entries ORDER BY timestamp DESC')
        rows = cursor.fetchall()
        
        entries = []
        for row in rows:
            entries.append({
                'id': row[0],
                'timestamp': row[1],
                'date': row[2],
                'lake_name': row[3],
                'fishing_method': row[4],
                'fish_species': row[5],
                'fish_count': row[6],
                'fish_size_avg': row[7],
                'frogs_observed': row[8],
                'turtles_observed': row[9],
                'water_temperature': row[10],
                'water_clarity': row[11],
                'notes': row[12]
            })
        
        conn.close()
        return entries
    
    # Animal entries methods
    def add_animal_entry(self, data):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO animal_entries 
            (timestamp, date, location, species, common_name, number_observed, behavior, habitat, time_of_day, weather_conditions, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            datetime.now().isoformat(),
            data.get('date', ''),
            data.get('location', ''),
            data.get('species', ''),
            data.get('common_name', ''),
            int(data.get('number_observed', 1)) if data.get('number_observed') else 1,
            data.get('behavior', ''),
            data.get('habitat', ''),
            data.get('time_of_day', ''),
            data.get('weather_conditions', ''),
            data.get('notes', '')
        ))
        
        conn.commit()
        conn.close()
    
    def get_animal_entries(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM animal_entries ORDER BY timestamp DESC')
        rows = cursor.fetchall()
        
        entries = []
        for row in rows:
            entries.append({
                'id': row[0],
                'timestamp': row[1],
                'date': row[2],
                'location': row[3],
                'species': row[4],
                'common_name': row[5],
                'number_observed': row[6],
                'behavior': row[7],
                'habitat': row[8],
                'time_of_day': row[9],
                'weather_conditions': row[10],
                'notes': row[11]
            })
        
        conn.close()
        return entries
    
    def get_recent_entries(self, limit=10):
        """Get recent entries from all tables combined"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Get recent entries from each table with a type identifier
        queries = [
            "SELECT 'weather' as type, timestamp, date, location as title, notes FROM weather_entries",
            "SELECT 'plant' as type, timestamp, date, species_name as title, notes FROM plant_entries",
            "SELECT 'river' as type, timestamp, date, location as title, notes FROM river_entries",
            "SELECT 'lake' as type, timestamp, date, lake_name as title, notes FROM lake_entries",
            "SELECT 'animal' as type, timestamp, date, species as title, notes FROM animal_entries",
            "SELECT 'garbage_can' as type, timestamp, date, location as title, notes FROM garbage_can_entries"
        ]
        
        all_entries = []
        for query in queries:
            cursor.execute(query)
            rows = cursor.fetchall()
            for row in rows:
                all_entries.append({
                    'type': row[0],
                    'timestamp': row[1],
                    'date': row[2],
                    'title': row[3],
                    'notes': row[4]
                })
        
        # Sort by timestamp and return most recent
        all_entries.sort(key=lambda x: x['timestamp'], reverse=True)
        conn.close()
        
        return all_entries[:limit]
    
    # Garbage can entries methods
    def add_garbage_can_entry(self, data):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO garbage_can_entries 
            (timestamp, date, location, garbage_can_type, fullness_level, ant_species, ant_colony_count, ant_activity_level, weather_conditions, temperature, time_of_day, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            datetime.now().isoformat(),
            data.get('date', ''),
            data.get('location', ''),
            data.get('garbage_can_type', ''),
            data.get('fullness_level', ''),
            data.get('ant_species', ''),
            int(data.get('ant_colony_count', 0)) if data.get('ant_colony_count') else None,
            data.get('ant_activity_level', ''),
            data.get('weather_conditions', ''),
            float(data.get('temperature', 0)) if data.get('temperature') else None,
            data.get('time_of_day', ''),
            data.get('notes', '')
        ))
        
        conn.commit()
        conn.close()
    
    def get_garbage_can_entries(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM garbage_can_entries ORDER BY timestamp DESC')
        rows = cursor.fetchall()
        
        entries = []
        for row in rows:
            entries.append({
                'id': row[0],
                'timestamp': row[1],
                'date': row[2],
                'location': row[3],
                'garbage_can_type': row[4],
                'fullness_level': row[5],
                'ant_species': row[6],
                'ant_colony_count': row[7],
                'ant_activity_level': row[8],
                'weather_conditions': row[9],
                'temperature': row[10],
                'time_of_day': row[11],
                'notes': row[12]
            })
        
        conn.close()
        return entries

    def add_learning_resource(self, data):
        """Add a learning resource"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        timestamp = datetime.now().isoformat()
        date = data.get('date', datetime.now().strftime('%Y-%m-%d'))
        title = data.get('title', 'Untitled')
        category = data.get('category', '')
        description = data.get('description', '')
        url = data.get('url', '')
        notes = data.get('notes', '')
        
        cursor.execute('''
            INSERT INTO learning_resources (timestamp, date, title, category, description, url, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (timestamp, date, title, category, description, url, notes))
        
        conn.commit()
        conn.close()

    def get_learning_resources(self):
        """Get all learning resources"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM learning_resources ORDER BY timestamp DESC')
        rows = cursor.fetchall()
        
        resources = []
        for row in rows:
            resources.append({
                'id': row[0],
                'timestamp': row[1],
                'date': row[2],
                'title': row[3],
                'category': row[4],
                'description': row[5],
                'url': row[6],
                'notes': row[7]
            })
        
        conn.close()
        return resources

    def add_gud_entry(self, data):
        """Add a Giving-Up Density entry for BIOS 399"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        timestamp = datetime.now().isoformat()
        date = data.get('date', datetime.now().strftime('%Y-%m-%d'))
        site_type = data.get('site_type', 'Control')
        mask_a = int(data.get('mask_a', 1))
        vis_score = int(data.get('vis_score', 1))
        dist_to_road = float(data.get('dist_to_road', 0))
        transit_active = 1 if data.get('transit_active') == 'on' else 0
        p_cues_hd = int(data.get('predator_cues_human_dog', 0))
        p_cues_ac = int(data.get('predator_cues_alarm_calls', 0))
        
        # Sodium Multiplier (λ) calculation logic
        # High salt stress (low dist_to_road) increases λ
        # Simple model: λ = 1 + (100 / (dist_to_road + 10))
        sodium_multiplier = 1.0 + (100.0 / (dist_to_road + 10.0))
        
        cursor.execute('''
            INSERT INTO gud_entries (
                timestamp, date, site_type, mask_a, vis_score, 
                dist_to_road, transit_active, predator_cues_human_dog, 
                predator_cues_alarm_calls, sodium_multiplier, notes
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (timestamp, date, site_type, mask_a, vis_score, 
              dist_to_road, transit_active, p_cues_hd, p_cues_ac, sodium_multiplier, data.get('notes', '')))
        
        conn.commit()
        conn.close()

    def get_gud_entries(self):
        """Get all GUD entries"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM gud_entries ORDER BY timestamp DESC')
        rows = cursor.fetchall()
        entries = []
        for row in rows:
            entries.append({
                'id': row[0], 'timestamp': row[1], 'date': row[2],
                'site_type': row[3], 'mask_a': row[4], 'vis_score': row[5],
                'dist_to_road': row[6], 'transit_active': row[7],
                'predator_cues_hd': row[8], 'predator_cues_ac': row[9],
                'sodium_multiplier': row[10], 'notes': row[11]
            })
        conn.close()
        return entries

    def get_statistics(self):
        """Get count statistics for all entry types"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        stats = {}
        
        tables = ['weather_entries', 'plant_entries', 'river_entries', 'lake_entries', 'animal_entries', 'garbage_can_entries', 'learning_resources']
        for table in tables:
            cursor.execute(f'SELECT COUNT(*) FROM {table}')
            count = cursor.fetchone()[0]
            stats[f'total_{table}'] = count
        
        conn.close()
        return stats
