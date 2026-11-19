import http.server
import socketserver
import json
import urllib.parse
import urllib.request
from datetime import datetime
import os
from database import DatabaseManager
from openai import OpenAI

# Initialize OpenAI client using Replit AI Integrations
# This internally uses Replit AI Integrations for OpenAI access, 
# does not require your own API key, and charges are billed to your credits.
client = OpenAI(
    base_url=os.environ.get("AI_INTEGRATIONS_OPENAI_BASE_URL"),
    api_key=os.environ.get("AI_INTEGRATIONS_OPENAI_API_KEY")
)

# Initialize database manager
db = DatabaseManager()

class EnvironmentalObservationHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # Normalize path by removing trailing slash
        path = self.path
        if path.endswith('/') and len(path) > 1:
            path = path[:-1]

        if path == '/' or path == '/index.html':
            self.serve_index()
        elif path == '/weather':
            self.serve_weather()
        elif path == '/plants':
            self.serve_plants()
        elif path == '/river':
            self.send_response(302)
            self.send_header('Location', '/lakes')
            self.end_headers()
            return
        elif path == '/lakes':
            self.serve_lakes()
        elif path == '/animals':
            self.serve_animals()
        elif path == '/garbage_cans':
            self.serve_garbage_cans()
        elif path == '/learning-center':
            self.serve_learning_center()
        elif path == '/we-convene-science':
            self.serve_we_convene_science()
        elif path == '/maps':
            self.serve_maps()
        elif path == '/statistics':
            self.serve_statistics()
        elif path == '/squirrel-model':
            self.send_response(302)
            self.send_header('Location', '/animals')
            self.end_headers()
            return
        elif path == '/sodium-trap':
            self.send_response(302)
            self.send_header('Location', '/animals')
            self.end_headers()
            return
        elif path == '/api/squirrel-data':
            self.serve_squirrel_data_api()
        elif path.startswith('/add'):
            self.serve_add_form()
        else:
            # Fallback for static files or other paths
            super().do_GET()

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        form_data = urllib.parse.parse_qs(post_data.decode('utf-8'))

        # Convert form data to regular dict
        data = {}
        for key, value in form_data.items():
            data[key] = value[0] if len(value) == 1 else value

        if self.path == '/add_weather':
            db.add_weather_entry(data)
        elif self.path == '/add_plant':
            db.add_plant_entry(data)
        elif self.path == '/add_river':
            db.add_river_entry(data)
        elif self.path == '/add_lake':
            db.add_lake_entry(data)
        elif self.path == '/add_animal':
            db.add_animal_entry(data)
        elif self.path == '/add_garbage_can':
            db.add_garbage_can_entry(data)
        elif self.path == '/add_learning_resource':
            db.add_learning_resource(data)
        elif self.path == '/add_gud_entry':
            db.add_gud_entry(data)

        # Redirect back to appropriate page
        self.send_response(302)
        category = self.path.replace('/add_', '')
        if category == 'weather':
            self.send_header('Location', '/weather')
        elif category == 'plant':
            self.send_header('Location', '/plants')
        elif category == 'river':
            self.send_header('Location', '/lakes')
        elif category == 'lake':
            self.send_header('Location', '/lakes')
        elif category == 'animal':
            self.send_header('Location', '/animals')
        elif category == 'garbage_can':
            self.send_header('Location', '/garbage_cans')
        elif category == 'learning_resource':
            self.send_header('Location', '/learning-center')
        elif category == 'gud_entry':
            self.send_header('Location', '/animals')
        else:
            self.send_header('Location', '/')
        self.end_headers()

    def serve_html(self, content):
        # Inject Google Dialogflow Messenger script and component before closing body tag
        messenger_html = """
    <script src="https://www.gstatic.com/dialogflow-console/fast/messenger/bootstrap.js?v=1"></script>
    <df-messenger
      intent="WELCOME"
      chat-title="ProfessorCULAPSED"
      agent-id="be7f1fc6-382e-490d-9b7e-0b7001fc9973"
      language-code="en"
    ></df-messenger>
    <!-- Default Statcounter code for CULAP Data Camp and Education Center
https://8ed879ce-2534-4bba-bf7d-23d8925989a5-00-ti7a1jcvn1hu.spock.replit.dev/
-->
<script type="text/javascript">
var sc_project=13209906; 
var sc_invisible=0; 
var sc_security="f2e4d088"; 
var scJsHost = "https://";
document.write("<sc"+"ript type='text/javascript' src='" +
scJsHost+
"statcounter.com/counter/counter.js'></"+"script>");
</script>
<noscript><div class="statcounter"><a title="Web Analytics"
href="https://statcounter.com/" target="_blank"><img
class="statcounter"
src="https://c.statcounter.com/13209906/0/f2e4d088/0/"
alt="Web Analytics"
referrerPolicy="no-referrer-when-downgrade"></a></div></noscript>
<!-- End of Statcounter Code -->
<a href="https://statcounter.com/p13209906/?guest=1">View My
Stats</a>
</body>
"""
        if "</body>" in content:
            content = content.replace("</body>", messenger_html)
        
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(content.encode('utf-8'))

    def serve_index(self):
        recent_entries = db.get_recent_entries(10)

        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>CULAP Data Camp and Education Center</title>
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <style>
                body {{ font-family: Arial, sans-serif; margin: 0; padding: 20px; background-color: #f5f5f5; }}
                .container {{ max-width: 1200px; margin: 0 auto; }}
                .header {{ background-color: #28a745; color: white; padding: 20px; border-radius: 8px; margin-bottom: 20px; }}
                .nav {{ display: flex; flex-wrap: wrap; gap: 10px; margin-bottom: 20px; }}
                .nav a {{ background-color: #007bff; color: white; padding: 10px 15px; text-decoration: none; border-radius: 5px; }}
                .nav a:hover {{ background-color: #0056b3; }}
                .card {{ background: white; padding: 20px; margin: 10px 0; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
                .grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; }}
                .add-btn {{ background-color: #28a745; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; display: inline-block; }}
                .add-btn:hover {{ background-color: #218838; }}
            </style>
        <link rel="stylesheet" href="https://unpkg.com/@algolia/sitesearch@latest/dist/search.min.css" />
    <script src="https://unpkg.com/@algolia/sitesearch@latest/dist/search.min.js"></script>
</head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🌿 CULAP Data Camp and Education Center</h1>
                    <p>Track and monitor environmental conditions, wildlife, and natural phenomena across Cook County, Illinois</p>
                </div>

                <div class="nav">
                    <a href="/">Home</a>
                    <a href="/weather">Weather</a>
                    <a href="/plants">Plants</a>
                    
                    <a href="/lakes">Lakes &amp; River</a>
                    <a href="/animals">Animals</a>
                    
                    <a href="/garbage_cans">Garbage Cans</a>
                    
                    <a href="/we-convene-science">We Convene Science</a>
                    <a href="/maps">Maps</a>
                    <a href="/statistics">Statistics</a>
                </div>
                <div id="search" style="margin-bottom: 20px;"></div>
                <script>
                  SiteSearch.init({{
                    container: "#search",
                    applicationId: "G1S1VRTBX5",
                    apiKey: "5d5d722782d6b620065a475f91221e18",
                    indexName: "test_schiller_woods_scenariosss",
                    attributes: {{
                      primaryText: "date",
                      secondaryText: undefined,
                      tertiaryText: undefined,
                      url: "",
                      image: undefined
                    }},
                    darkMode: false,
                  }});
                </script>

                <div class="grid">
                    <div class="card">
                        <h3>🌦️ Weather Tracking</h3>
                        <p>Record daily weather observations for Chicago and Cook County suburbs.</p>
                        <a href="/add_weather" class="add-btn">Add Weather Entry</a>
                    </div>

                    <div class="card">
                        <h3>🌸 Plant Identification</h3>
                        <p>Document plant species found in Cook County Forest Preserves.</p>
                        <a href="/add_plant" class="add-btn">Add Plant Observation</a>
                    </div>

                    <div class="card">
                        <h3>🌊 Chicago River</h3>
                        <p>Monitor Chicago River conditions and wildlife.</p>
                        <a href="/add_river" class="add-btn">Add River Observation</a>
                    </div>

                    <div class="card">
                        <h3>💧 Lake Surveys</h3>
                        <p>Conduct creel surveys and document aquatic life in Cook County lakes.</p>
                        <a href="/add_lake" class="add-btn">Add Lake Survey</a>
                    </div>

                    <div class="card">
                        <h3>🦌 Animal Observations</h3>
                        <p>Record wildlife sightings and animal behavior in Cook County.</p>
                        <a href="/add_animal" class="add-btn">Add Animal Observation</a>
                    </div>

                    <div class="card">
                        <h3>🗑️ Garbage Can Observations</h3>
                        <p>Record data about garbage cans, ant species, and colonies.</p>
                        <a href="/add_garbage_can" class="add-btn">Add Garbage Can Observation</a>
                    </div>
                </div>

                <div class="card">
                    <h3>Recent Entries</h3>
                    {self.format_recent_entries(recent_entries)}
                </div>
            </div>
        </body>
        </html>
        """
        self.serve_html(html)

    def serve_weather(self):
        entries = db.get_weather_entries()
        entries_html = ""
        for entry in entries:
            entries_html += f"""
            <div class="card">
                <h4>{entry.get('location', 'Unknown Location')}</h4>
                <p><strong>Date:</strong> {entry.get('date', 'N/A')}</p>
                <p><strong>Temperature:</strong> {entry.get('temperature', 'N/A')}°F</p>
                <p><strong>Humidity:</strong> {entry.get('humidity', 'N/A')}%</p>
                <p><strong>Precipitation:</strong> {entry.get('precipitation', 'N/A')}"</p>
                <p><strong>Wind Speed:</strong> {entry.get('wind_speed', 'N/A')} mph</p>
                <p><strong>Conditions:</strong> {entry.get('conditions', 'N/A')}</p>
                {f"<p><strong>Notes:</strong> {entry.get('notes', '')}</p>" if entry.get('notes') else ""}
            </div>
            """

        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Weather Observations - Chicago Environmental Observations</title>
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <style>
                body {{ font-family: Arial, sans-serif; margin: 0; padding: 20px; background-color: #f5f5f5; }}
                .container {{ max-width: 1200px; margin: 0 auto; }}
                .header {{ background-color: #28a745; color: white; padding: 20px; border-radius: 8px; margin-bottom: 20px; }}
                .nav {{ display: flex; flex-wrap: wrap; gap: 10px; margin-bottom: 20px; }}
                .nav a {{ background-color: #007bff; color: white; padding: 10px 15px; text-decoration: none; border-radius: 5px; }}
                .nav a:hover {{ background-color: #0056b3; }}
                .card {{ background: white; padding: 20px; margin: 10px 0; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
                .add-btn {{ background-color: #28a745; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; display: inline-block; margin-bottom: 20px; }}
                .add-btn:hover {{ background-color: #218838; }}
                .grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; }}
            </style>
        <link rel="stylesheet" href="https://unpkg.com/@algolia/sitesearch@latest/dist/search.min.css" />
    <script src="https://unpkg.com/@algolia/sitesearch@latest/dist/search.min.js"></script>
</head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🌦️ Weather Observations</h1>
                </div>

                <div class="nav">
                    <a href="/">Home</a>
                    <a href="/weather">Weather</a>
                    <a href="/plants">Plants</a>
                    
                    <a href="/lakes">Lakes &amp; River</a>
                    <a href="/animals">Animals</a>
                    
                    <a href="/garbage_cans">Garbage Cans</a>
                    
                    <a href="/we-convene-science">We Convene Science</a>
                    <a href="/maps">Maps</a>
                    <a href="/statistics">Statistics</a>
                </div>
                <div id="search" style="margin-bottom: 20px;"></div>
                <script>
                  SiteSearch.init({{
                    container: "#search",
                    applicationId: "G1S1VRTBX5",
                    apiKey: "5d5d722782d6b620065a475f91221e18",
                    indexName: "test_schiller_woods_scenariosss",
                    attributes: {{
                      primaryText: "date",
                      secondaryText: undefined,
                      tertiaryText: undefined,
                      url: "",
                      image: undefined
                    }},
                    darkMode: false,
                  }});
                </script>

                <a href="/add_weather" class="add-btn">Add New Weather Entry</a>

                <div class="grid">
                    {entries_html if entries_html else '<div class="card"><p>No weather entries yet. Add your first observation!</p></div>'}
                </div>
            </div>
        </body>
        </html>
        """
        self.serve_html(html)

    def serve_plants(self):
        entries = db.get_plant_entries()
        entries_html = ""
        for entry in entries:
            entries_html += f"""
            <div class="card">
                <h4>{entry.get('species_name', 'Unknown Species')}</h4>
                <p><strong>Common Name:</strong> {entry.get('common_name', 'N/A')}</p>
                <p><strong>Date:</strong> {entry.get('date', 'N/A')}</p>
                <p><strong>Preserve:</strong> {entry.get('preserve', 'N/A')}</p>
                <p><strong>Location Details:</strong> {entry.get('location_details', 'N/A')}</p>
                <p><strong>Abundance:</strong> {entry.get('abundance', 'N/A')}</p>
                <p><strong>Flowering Status:</strong> {entry.get('flowering_status', 'N/A')}</p>
                <p><strong>Habitat:</strong> {entry.get('habitat', 'N/A')}</p>
                {f"<p><strong>Notes:</strong> {entry.get('notes', '')}</p>" if entry.get('notes') else ""}
            </div>
            """

        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Plant Observations - Chicago Environmental Observations</title>
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <style>
                body {{ font-family: Arial, sans-serif; margin: 0; padding: 20px; background-color: #f5f5f5; }}
                .container {{ max-width: 1200px; margin: 0 auto; }}
                .header {{ background-color: #28a745; color: white; padding: 20px; border-radius: 8px; margin-bottom: 20px; }}
                .nav {{ display: flex; flex-wrap: wrap; gap: 10px; margin-bottom: 20px; }}
                .nav a {{ background-color: #007bff; color: white; padding: 10px 15px; text-decoration: none; border-radius: 5px; }}
                .nav a:hover {{ background-color: #0056b3; }}
                .card {{ background: white; padding: 20px; margin: 10px 0; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
                .add-btn {{ background-color: #28a745; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; display: inline-block; margin-bottom: 20px; }}
                .add-btn:hover {{ background-color: #218838; }}
                .grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; }}
            </style>
        <link rel="stylesheet" href="https://unpkg.com/@algolia/sitesearch@latest/dist/search.min.css" />
    <script src="https://unpkg.com/@algolia/sitesearch@latest/dist/search.min.js"></script>
</head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🌸 Plant Observations</h1>
                </div>

                <div class="nav">
                    <a href="/">Home</a>
                    <a href="/weather">Weather</a>
                    <a href="/plants">Plants</a>
                    
                    <a href="/lakes">Lakes &amp; River</a>
                    <a href="/animals">Animals</a>
                    
                    <a href="/garbage_cans">Garbage Cans</a>
                    
                    <a href="/we-convene-science">We Convene Science</a>
                    <a href="/maps">Maps</a>
                    <a href="/statistics">Statistics</a>
                </div>
                <div id="search" style="margin-bottom: 20px;"></div>
                <script>
                  SiteSearch.init({{
                    container: "#search",
                    applicationId: "G1S1VRTBX5",
                    apiKey: "5d5d722782d6b620065a475f91221e18",
                    indexName: "test_schiller_woods_scenariosss",
                    attributes: {{
                      primaryText: "date",
                      secondaryText: undefined,
                      tertiaryText: undefined,
                      url: "",
                      image: undefined
                    }},
                    darkMode: false,
                  }});
                </script>

                <a href="/add_plant" class="add-btn">Add New Plant Observation</a>

                <div class="grid">
                    {entries_html if entries_html else '<div class="card"><p>No plant entries yet. Add your first observation!</p></div>'}
                </div>
            </div>
        </body>
        </html>
        """
        self.serve_html(html)

    def serve_river(self):
        entries = db.get_river_entries()
        entries_html = ""
        for entry in entries:
            entries_html += f"""
            <div class="card">
                <h4>{entry.get('location', 'Unknown Location')}</h4>
                <p><strong>Date:</strong> {entry.get('date', 'N/A')}</p>
                <p><strong>Water Level:</strong> {entry.get('water_level', 'N/A')}</p>
                <p><strong>Water Clarity:</strong> {entry.get('water_clarity', 'N/A')}</p>
                <p><strong>Temperature:</strong> {entry.get('temperature', 'N/A')}°F</p>
                <p><strong>Flow Rate:</strong> {entry.get('flow_rate', 'N/A')}</p>
                <p><strong>Wildlife Observed:</strong> {entry.get('wildlife_observed', 'N/A')}</p>
                <p><strong>Pollution Indicators:</strong> {entry.get('pollution_indicators', 'N/A')}</p>
                {f"<p><strong>Notes:</strong> {entry.get('notes', '')}</p>" if entry.get('notes') else ""}
            </div>
            """

        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Chicago River Observations - Chicago Environmental Observations</title>
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <style>
                body {{ font-family: Arial, sans-serif; margin: 0; padding: 20px; background-color: #f5f5f5; }}
                .container {{ max-width: 1200px; margin: 0 auto; }}
                .header {{ background-color: #28a745; color: white; padding: 20px; border-radius: 8px; margin-bottom: 20px; }}
                .nav {{ display: flex; flex-wrap: wrap; gap: 10px; margin-bottom: 20px; }}
                .nav a {{ background-color: #007bff; color: white; padding: 10px 15px; text-decoration: none; border-radius: 5px; }}
                .nav a:hover {{ background-color: #0056b3; }}
                .card {{ background: white; padding: 20px; margin: 10px 0; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
                .add-btn {{ background-color: #28a745; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; display: inline-block; margin-bottom: 20px; }}
                .add-btn:hover {{ background-color: #218838; }}
                .grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; }}
            </style>
        <link rel="stylesheet" href="https://unpkg.com/@algolia/sitesearch@latest/dist/search.min.css" />
    <script src="https://unpkg.com/@algolia/sitesearch@latest/dist/search.min.js"></script>
</head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🌊 Chicago River Observations</h1>
                </div>

                <div class="nav">
                    <a href="/">Home</a>
                    <a href="/weather">Weather</a>
                    <a href="/plants">Plants</a>
                    
                    <a href="/lakes">Lakes &amp; River</a>
                    <a href="/animals">Animals</a>
                    
                    <a href="/garbage_cans">Garbage Cans</a>
                    
                    <a href="/we-convene-science">We Convene Science</a>
                    <a href="/maps">Maps</a>
                    <a href="/statistics">Statistics</a>
                </div>
                <div id="search" style="margin-bottom: 20px;"></div>
                <script>
                  SiteSearch.init({{
                    container: "#search",
                    applicationId: "G1S1VRTBX5",
                    apiKey: "5d5d722782d6b620065a475f91221e18",
                    indexName: "test_schiller_woods_scenariosss",
                    attributes: {{
                      primaryText: "date",
                      secondaryText: undefined,
                      tertiaryText: undefined,
                      url: "",
                      image: undefined
                    }},
                    darkMode: false,
                  }});
                </script>

                <a href="/add_river" class="add-btn">Add New River Observation</a>

                <div class="grid">
                    {entries_html if entries_html else '<div class="card"><p>No river entries yet. Add your first observation!</p></div>'}
                </div>
            </div>
        </body>
        </html>
        """
        self.serve_html(html)

    def serve_lakes(self):
        lake_entries = db.get_lake_entries()
        lake_entries_html = ""
        for entry in lake_entries:
            lake_entries_html += f"""
            <div class="card">
                <h4>{entry.get('lake_name', 'Unknown Lake')}</h4>
                <p><strong>Date:</strong> {entry.get('date', 'N/A')}</p>
                <p><strong>Fishing Method:</strong> {entry.get('fishing_method', 'N/A')}</p>
                <p><strong>Fish Species:</strong> {entry.get('fish_species', 'N/A')}</p>
                <p><strong>Fish Count:</strong> {entry.get('fish_count', 'N/A')}</p>
                <p><strong>Average Fish Size:</strong> {entry.get('fish_size_avg', 'N/A')}"</p>
                <p><strong>Frogs Observed:</strong> {entry.get('frogs_observed', 'N/A')}</p>
                <p><strong>Turtles Observed:</strong> {entry.get('turtles_observed', 'N/A')}</p>
                <p><strong>Water Temperature:</strong> {entry.get('water_temperature', 'N/A')}°F</p>
                <p><strong>Water Clarity:</strong> {entry.get('water_clarity', 'N/A')}</p>
                {f"<p><strong>Notes:</strong> {entry.get('notes', '')}</p>" if entry.get('notes') else ""}
            </div>
            """

        river_entries = db.get_river_entries()
        river_entries_html = ""
        for entry in river_entries:
            river_entries_html += f"""
            <div class="card">
                <h4>{entry.get('location', 'Unknown Location')}</h4>
                <p><strong>Date:</strong> {entry.get('date', 'N/A')}</p>
                <p><strong>Water Level:</strong> {entry.get('water_level', 'N/A')}</p>
                <p><strong>Water Clarity:</strong> {entry.get('water_clarity', 'N/A')}</p>
                <p><strong>Temperature:</strong> {entry.get('temperature', 'N/A')}°F</p>
                <p><strong>Flow Rate:</strong> {entry.get('flow_rate', 'N/A')}</p>
                <p><strong>Wildlife Observed:</strong> {entry.get('wildlife_observed', 'N/A')}</p>
                <p><strong>Pollution Indicators:</strong> {entry.get('pollution_indicators', 'N/A')}</p>
                {f"<p><strong>Notes:</strong> {entry.get('notes', '')}</p>" if entry.get('notes') else ""}
            </div>
            """

        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Lakes &amp; Chicago River - CULAP Data Camp and Education Center</title>
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <style>
                body {{ font-family: Arial, sans-serif; margin: 0; padding: 20px; background-color: #f5f5f5; }}
                .container {{ max-width: 1200px; margin: 0 auto; }}
                .header {{ background-color: #28a745; color: white; padding: 20px; border-radius: 8px; margin-bottom: 20px; }}
                .section-header {{ background-color: #0d6efd; color: white; padding: 15px 20px; border-radius: 8px; margin: 30px 0 15px 0; }}
                .nav {{ display: flex; flex-wrap: wrap; gap: 10px; margin-bottom: 20px; }}
                .nav a {{ background-color: #007bff; color: white; padding: 10px 15px; text-decoration: none; border-radius: 5px; }}
                .nav a:hover {{ background-color: #0056b3; }}
                .card {{ background: white; padding: 20px; margin: 10px 0; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
                .add-btn {{ background-color: #28a745; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; display: inline-block; margin-bottom: 20px; font-weight: bold; }}
                .add-btn:hover {{ background-color: #218838; }}
                .grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; }}
            </style>
        <link rel="stylesheet" href="https://unpkg.com/@algolia/sitesearch@latest/dist/search.min.css" />
    <script src="https://unpkg.com/@algolia/sitesearch@latest/dist/search.min.js"></script>
</head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>💧 Lakes &amp; Chicago River</h1>
                </div>
                <div class="nav">
                    <a href="/">Home</a>
                    <a href="/weather">Weather</a>
                    <a href="/plants">Plants</a>
                    <a href="/lakes">Lakes &amp; River</a>
                    <a href="/animals">Animals</a>
                    <a href="/garbage_cans">Garbage Cans</a>
                    <a href="/we-convene-science">We Convene Science</a>
                    <a href="/maps">Maps</a>
                    <a href="/statistics">Statistics</a>
                </div>
                <div id="search" style="margin-bottom: 20px;"></div>
                <script>
                  SiteSearch.init({{
                    container: "#search",
                    applicationId: "G1S1VRTBX5",
                    apiKey: "5d5d722782d6b620065a475f91221e18",
                    indexName: "test_schiller_woods_scenariosss",
                    attributes: {{
                      primaryText: "date",
                      secondaryText: undefined,
                      tertiaryText: undefined,
                      url: "",
                      image: undefined
                    }},
                    darkMode: false,
                  }});
                </script>

                <a href="/add_lake" class="add-btn">Add New Lake Survey</a>
                <div class="grid">
                    {lake_entries_html if lake_entries_html else '<div class="card"><p>No lake entries yet. Add your first survey!</p></div>'}
                </div>

                <div class="section-header">
                    <h2>🌊 Chicago River Observations</h2>
                </div>
                <a href="/add_river" class="add-btn">Add New River Observation</a>
                <div class="grid">
                    {river_entries_html if river_entries_html else '<div class="card"><p>No river entries yet. Add your first observation!</p></div>'}
                </div>
            </div>
        </body>
        </html>
        """
        self.serve_html(html)

    def serve_animals(self):
        entries = db.get_animal_entries()
        entries_html = ""
        for entry in entries:
            entries_html += f"""
            <div class="card">
                <h4>{entry.get('species', 'Unknown Species')}</h4>
                <p><strong>Common Name:</strong> {entry.get('common_name', 'N/A')}</p>
                <p><strong>Date:</strong> {entry.get('date', 'N/A')}</p>
                <p><strong>Location:</strong> {entry.get('location', 'N/A')}</p>
                <p><strong>Number Observed:</strong> {entry.get('number_observed', 'N/A')}</p>
                <p><strong>Behavior:</strong> {entry.get('behavior', 'N/A')}</p>
                <p><strong>Habitat:</strong> {entry.get('habitat', 'N/A')}</p>
                <p><strong>Time of Day:</strong> {entry.get('time_of_day', 'N/A')}</p>
                <p><strong>Weather Conditions:</strong> {entry.get('weather_conditions', 'N/A')}</p>
                {f"<p><strong>Notes:</strong> {entry.get('notes', '')}</p>" if entry.get('notes') else ""}
            </div>
            """

        # Squirrel AI model output
        try:
            response = client.responses.create(
                model="gpt-4o",
                prompt={
                    "id": "pmpt_697e4b151b2c8190a992e1146a2f2f410fb0045d5f65d9e8",
                    "version": "6"
                }
            )
            ai_content = str(response)
        except Exception as e:
            ai_content = f"Error generating squirrel model: {str(e)}"

        # GUD / Sodium Trap entries
        gud_entries = db.get_gud_entries()
        gud_entries_html = ""
        for entry in gud_entries:
            gud_entries_html += f"""
            <div class="card">
                <h4>{entry.get('site_type', 'N/A')} Site — {entry.get('date', 'N/A')}</h4>
                <p><strong>Sodium Multiplier (λ):</strong> {entry.get('sodium_multiplier', 1.0):.2f}</p>
                <p><strong>Acoustic Masking (1–5):</strong> {entry.get('mask_a', 'N/A')}</p>
                <p><strong>Visibility Score (1–5):</strong> {entry.get('vis_score', 'N/A')}</p>
                <p><strong>Dist. to River Road:</strong> {entry.get('dist_to_road', 'N/A')} m</p>
                <p><strong>Pace Bus Active:</strong> {"Yes" if entry.get('transit_active') else "No"}</p>
                <p><strong>Predator Cues:</strong> {entry.get('predator_cues_hd', 0)} (H/D), {entry.get('predator_cues_ac', 0)} (Alarm)</p>
                {f"<p><strong>Notes:</strong> {entry.get('notes', '')}</p>" if entry.get('notes') else ""}
            </div>
            """

        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Animals, Squirrel AI &amp; Sodium Trap - CULAP Data Camp and Education Center</title>
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <style>
                body {{ font-family: Arial, sans-serif; margin: 0; padding: 20px; background-color: #f5f5f5; }}
                .container {{ max-width: 1200px; margin: 0 auto; }}
                .header {{ background-color: #28a745; color: white; padding: 20px; border-radius: 8px; margin-bottom: 20px; }}
                .section-header {{ padding: 15px 20px; border-radius: 8px; margin: 30px 0 15px 0; }}
                .section-header-teal {{ background-color: #17a2b8; color: white; }}
                .section-header-yellow {{ background-color: #ffc107; color: #333; }}
                .nav {{ display: flex; flex-wrap: wrap; gap: 10px; margin-bottom: 20px; }}
                .nav a {{ background-color: #007bff; color: white; padding: 10px 15px; text-decoration: none; border-radius: 5px; }}
                .nav a:hover {{ background-color: #0056b3; }}
                .card {{ background: white; padding: 20px; margin: 10px 0; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
                .add-btn {{ color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; display: inline-block; margin-bottom: 20px; font-weight: bold; }}
                .add-btn-green {{ background-color: #28a745; }}
                .add-btn-green:hover {{ background-color: #218838; }}
                .add-btn-yellow {{ background-color: #ffc107; color: #333; }}
                .add-btn-yellow:hover {{ background-color: #e0a800; }}
                .grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; }}
                pre {{ background: #eee; padding: 15px; border-radius: 5px; overflow-x: auto; white-space: pre-wrap; }}
            </style>
        <link rel="stylesheet" href="https://unpkg.com/@algolia/sitesearch@latest/dist/search.min.css" />
    <script src="https://unpkg.com/@algolia/sitesearch@latest/dist/search.min.js"></script>
</head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🦌 Animal Observations</h1>
                </div>
                <div class="nav">
                    <a href="/">Home</a>
                    <a href="/weather">Weather</a>
                    <a href="/plants">Plants</a>
                    
                    <a href="/lakes">Lakes &amp; River</a>
                    <a href="/animals">Animals</a>
                    <a href="/garbage_cans">Garbage Cans</a>
                    <a href="/we-convene-science">We Convene Science</a>
                    <a href="/maps">Maps</a>
                    <a href="/statistics">Statistics</a>
                </div>
                <div id="search" style="margin-bottom: 20px;"></div>
                <script>
                  SiteSearch.init({{
                    container: "#search",
                    applicationId: "G1S1VRTBX5",
                    apiKey: "5d5d722782d6b620065a475f91221e18",
                    indexName: "test_schiller_woods_scenariosss",
                    attributes: {{
                      primaryText: "date",
                      secondaryText: undefined,
                      tertiaryText: undefined,
                      url: "",
                      image: undefined
                    }},
                    darkMode: false,
                  }});
                </script>

                <a href="/add_animal" class="add-btn add-btn-green">Add New Animal Observation</a>

                <div class="grid">
                    {entries_html if entries_html else '<div class="card"><p>No animal entries yet. Add your first observation!</p></div>'}
                </div>

                <div class="section-header section-header-teal">
                    <h2>🐿️ Squirrel AI Behavioral Model</h2>
                    <p>Powered by OpenAI Project Integration</p>
                </div>
                <div class="card">
                    <h3>🤖 AI Model Output</h3>
                    <p>Response from your customized OpenAI prompt (ID: pmpt_697e4...):</p>
                    <pre>{ai_content}</pre>
                </div>

                <div class="section-header section-header-yellow">
                    <h2>🐿️ Sodium Trap Project (BIOS 399)</h2>
                    <p>Modeling GUD curves and urban stressors at Schiller Woods — River Bend Picnic Area</p>
                </div>
                <a href="/add_gud_entry" class="add-btn add-btn-yellow">➕ Add GUD Observation</a>
                <div class="grid">
                    {gud_entries_html if gud_entries_html else '<div class="card"><p>No GUD entries yet. Add your first observation above!</p></div>'}
                </div>
            </div>
        </body>
        </html>
        """
        self.serve_html(html)

    def serve_garbage_cans(self):
        entries = db.get_garbage_can_entries()
        entries_html = ""
        for entry in entries:
            entries_html += f"""
            <div class="card">
                <h4>Garbage Can ID: {entry.get('garbage_can_id', 'Unknown ID')}</h4>
                <p><strong>Date:</strong> {entry.get('date', 'N/A')}</p>
                <p><strong>Location:</strong> {entry.get('location', 'N/A')}</p>
                <p><strong>Ant Species:</strong> {entry.get('ant_species', 'N/A')}</p>
                <p><strong>Colony Size:</strong> {entry.get('colony_size', 'N/A')}</p>
                <p><strong>Notes:</strong> {entry.get('notes', 'N/A')}</p>
            </div>
            """

        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Garbage Can Observations - Chicago Environmental Observations</title>
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <style>
                body {{ font-family: Arial, sans-serif; margin: 0; padding: 20px; background-color: #f5f5f5; }}
                .container {{ max-width: 1200px; margin: 0 auto; }}
                .header {{ background-color: #28a745; color: white; padding: 20px; border-radius: 8px; margin-bottom: 20px; }}
                .nav {{ display: flex; flex-wrap: wrap; gap: 10px; margin-bottom: 20px; }}
                .nav a {{ background-color: #007bff; color: white; padding: 10px 15px; text-decoration: none; border-radius: 5px; }}
                .nav a:hover {{ background-color: #0056b3; }}
                .card {{ background: white; padding: 20px; margin: 10px 0; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
                .add-btn {{ background-color: #28a745; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; display: inline-block; margin-bottom: 20px; }}
                .add-btn:hover {{ background-color: #218838; }}
                .grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; }}
            </style>
        <link rel="stylesheet" href="https://unpkg.com/@algolia/sitesearch@latest/dist/search.min.css" />
    <script src="https://unpkg.com/@algolia/sitesearch@latest/dist/search.min.js"></script>
</head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🗑️ Garbage Can Observations</h1>
                </div>

                <div class="nav">
                    <a href="/">Home</a>
                    <a href="/weather">Weather</a>
                    <a href="/plants">Plants</a>
                    
                    <a href="/lakes">Lakes &amp; River</a>
                    <a href="/animals">Animals</a>
                    
                    <a href="/garbage_cans">Garbage Cans</a>
                    
                    <a href="/we-convene-science">We Convene Science</a>
                    <a href="/maps">Maps</a>
                    <a href="/statistics">Statistics</a>
                </div>
                <div id="search" style="margin-bottom: 20px;"></div>
                <script>
                  SiteSearch.init({{
                    container: "#search",
                    applicationId: "G1S1VRTBX5",
                    apiKey: "5d5d722782d6b620065a475f91221e18",
                    indexName: "test_schiller_woods_scenariosss",
                    attributes: {{
                      primaryText: "date",
                      secondaryText: undefined,
                      tertiaryText: undefined,
                      url: "",
                      image: undefined
                    }},
                    darkMode: false,
                  }});
                </script>

                <a href="/add_garbage_can" class="add-btn">Add New Garbage Can Observation</a>

                <div class="grid">
                    {entries_html if entries_html else '<div class="card"><p>No garbage can entries yet. Add your first observation!</p></div>'}
                </div>
            </div>
        </body>
        </html>
        """
        self.serve_html(html)

    def serve_sodium_trap(self):
        entries = db.get_gud_entries()
        entries_html = ""
        for entry in entries:
            entries_html += f"""
            <div class="card">
                <h4>{entry.get('site_type', 'N/A')} Site - {entry.get('date', 'N/A')}</h4>
                <p><strong>Sodium Multiplier (λ):</strong> {entry.get('sodium_multiplier', 1.0):.2f}</p>
                <p><strong>Acoustic Masking (1-5):</strong> {entry.get('mask_a', 'N/A')}</p>
                <p><strong>Visibility Score (1-5):</strong> {entry.get('vis_score', 'N/A')}</p>
                <p><strong>Dist. to River Road:</strong> {entry.get('dist_to_road', 'N/A')}m</p>
                <p><strong>Pace Bus Active:</strong> {"Yes" if entry.get('transit_active') else "No"}</p>
                <p><strong>Predator Cues:</strong> {entry.get('predator_cues_hd', 0)} (H/D), {entry.get('predator_cues_ac', 0)} (Alarm)</p>
                {f"<p><strong>Notes:</strong> {entry.get('notes', '')}</p>" if entry.get('notes') else ""}
            </div>
            """

        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>The Sodium Trap Project - BIOS 399</title>
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <style>
                body {{ font-family: Arial, sans-serif; margin: 0; padding: 20px; background-color: #f5f5f5; }}
                .container {{ max-width: 1200px; margin: 0 auto; }}
                .header {{ background-color: #ffc107; color: #333; padding: 20px; border-radius: 8px; margin-bottom: 20px; }}
                .nav {{ display: flex; flex-wrap: wrap; gap: 10px; margin-bottom: 20px; }}
                .nav a {{ background-color: #007bff; color: white; padding: 10px 15px; text-decoration: none; border-radius: 5px; }}
                .card {{ background: white; padding: 20px; margin: 10px 0; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
                .add-btn {{ background-color: #ffc107; color: #333; padding: 10px 20px; text-decoration: none; border-radius: 5px; display: inline-block; margin-bottom: 20px; font-weight: bold; }}
                .grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; }}
            </style>
        <link rel="stylesheet" href="https://unpkg.com/@algolia/sitesearch@latest/dist/search.min.css" />
    <script src="https://unpkg.com/@algolia/sitesearch@latest/dist/search.min.js"></script>
</head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🐿️ The Sodium Trap Project (BIOS 399)</h1>
                    <p>Modeling GUD curves and urban stressors at Schiller Woods - River Bend Picnic Area</p>
                </div>
                <div class="nav">
                    <a href="/">Home</a>
                    <a href="/weather">Weather</a>
                    <a href="/plants">Plants</a>
                    
                    
                    <a href="/we-convene-science">We Convene Science</a>
                    <a href="/maps">Maps</a>
                </div>
                <a href="/add_gud_entry" class="add-btn">Add GUD Observation</a>
                <div class="grid">
                    {entries_html if entries_html else '<div class="card"><p>No GUD entries yet.</p></div>'}
                </div>
            </div>
        </body>
        </html>
        """
        self.serve_html(html)

    def serve_add_form(self):
        form_type = self.path.replace('/add_', '')
        if form_type == 'gud_entry':
            self.serve_gud_form()
            return
        elif form_type == 'weather':
            self.serve_weather_form()
        elif form_type == 'plant':
            self.serve_plant_form()
        elif form_type == 'river':
            self.serve_river_form()
        elif form_type == 'lake':
            self.serve_lake_form()
        elif form_type == 'animal':
            self.serve_animal_form()
        elif form_type == 'garbage_can':
            self.serve_garbage_can_form()
        elif form_type == 'learning_resource':
            self.serve_learning_resource_form()

    def serve_gud_form(self):
        html = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Add GUD Observation - Sodium Trap Project</title>
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <style>
                body { font-family: Arial, sans-serif; margin: 0; padding: 20px; background-color: #f5f5f5; }
                .container { max-width: 800px; margin: 0 auto; }
                .card { background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
                .form-group { margin-bottom: 15px; }
                label { display: block; margin-bottom: 5px; font-weight: bold; }
                input, select, textarea { width: 100%; padding: 8px; border: 1px solid #ddd; border-radius: 4px; box-sizing: border-box; }
                button { background-color: #ffc107; color: #333; padding: 12px 30px; border: none; border-radius: 5px; cursor: pointer; font-size: 16px; font-weight: bold; }
            </style>
        <link rel="stylesheet" href="https://unpkg.com/@algolia/sitesearch@latest/dist/search.min.css" />
    <script src="https://unpkg.com/@algolia/sitesearch@latest/dist/search.min.js"></script>
</head>
        <body>
            <div class="container">
                <div class="card">
                    <h2>Add GUD Observation</h2>
                    <form method="POST" action="/add_gud_entry">
                        <div class="form-group">
                            <label for="date">Date:</label>
                            <input type="date" id="date" name="date" required>
                        </div>
                        <div class="form-group">
                            <label for="site_type">Site Type:</label>
                            <select id="site_type" name="site_type" required>
                                <option value="Control">Robinson Homestead (Control)</option>
                                <option value="Experimental">River Bend Picnic Area (Experimental)</option>
                            </select>
                        </div>
                        <div class="form-group">
                            <label for="mask_a">Acoustic Masking (1-5):</label>
                            <input type="number" id="mask_a" name="mask_a" min="1" max="5" required>
                        </div>
                        <div class="form-group">
                            <label for="vis_score">Visibility Score (1-5):</label>
                            <input type="number" id="vis_score" name="vis_score" min="1" max="5" required>
                        </div>
                        <div class="form-group">
                            <label for="dist_to_road">Distance to River Road (meters):</label>
                            <input type="number" id="dist_to_road" name="dist_to_road" step="0.1" required>
                        </div>
                        <div class="form-group">
                            <label><input type="checkbox" name="transit_active"> Pace Bus Idling/Active</label>
                        </div>
                        <div class="form-group">
                            <label for="predator_cues_human_dog">Human/Dog Cues:</label>
                            <input type="number" id="predator_cues_human_dog" name="predator_cues_human_dog" value="0">
                        </div>
                        <div class="form-group">
                            <label for="predator_cues_alarm_calls">Alarm Call Cues:</label>
                            <input type="number" id="predator_cues_alarm_calls" name="predator_cues_alarm_calls" value="0">
                        </div>
                        <div class="form-group">
                            <label for="notes">Notes:</label>
                            <textarea id="notes" name="notes"></textarea>
                        </div>
                        <button type="submit">Submit Data</button>
                    </form>
                </div>
            </div>
        </body>
        </html>
        """
        self.serve_html(html)

    def serve_maps(self):
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Project Based Learning Maps - Chicago Environmental Observations</title>
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <style>
                body {{ font-family: Arial, sans-serif; margin: 0; padding: 20px; background-color: #f5f5f5; }}
                .container {{ max-width: 1200px; margin: 0 auto; }}
                .header {{ background-color: #6610f2; color: white; padding: 20px; border-radius: 8px; margin-bottom: 20px; }}
                .nav {{ display: flex; flex-wrap: wrap; gap: 10px; margin-bottom: 20px; }}
                .nav a {{ background-color: #007bff; color: white; padding: 10px 15px; text-decoration: none; border-radius: 5px; }}
                .nav a:hover {{ background-color: #0056b3; }}
                .card {{ background: white; padding: 20px; margin: 10px 0; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
                .map-placeholder {{ background-color: #e9ecef; border: 2px dashed #6c757d; height: 400px; border-radius: 8px; display: flex; align-items: center; justify-content: center; text-align: center; color: #6c757d; margin-bottom: 20px; }}
                .grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; }}
            </style>
        <link rel="stylesheet" href="https://unpkg.com/@algolia/sitesearch@latest/dist/search.min.css" />
    <script src="https://unpkg.com/@algolia/sitesearch@latest/dist/search.min.js"></script>
</head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🗺️ Project Based Learning Maps</h1>
                    <p>Spatial analysis and mapping resources for environmental research projects</p>
                </div>

                <div class="nav">
                    <a href="/">Home</a>
                    <a href="/weather">Weather</a>
                    <a href="/plants">Plants</a>
                    
                    <a href="/lakes">Lakes &amp; River</a>
                    <a href="/animals">Animals</a>
                    <a href="/garbage_cans">Garbage Cans</a>
                    <a href="/learning-center">Learning Center</a>
                    
                    <a href="/we-convene-science">We Convene Science</a>
                    <a href="/maps">Maps</a>
                    
                    <a href="/statistics">Statistics</a>
                </div>

                <div class="card">
                    <h3>Cook County Interactive Map</h3>
                    <p><strong>River Bend Site:</strong> [41.9515, -87.8430]</p>
                    <div class="map-placeholder">
                        <div>
                            <i style="font-size: 48px;">📍</i>
                            <p>Interactive Environmental Map Interface<br>Showing Observation Density Across Cook County</p>
                        </div>
                    </div>
                </div>

                <div class="grid">
                    <div class="card">
                        <h4>Forest Preserve Districts</h4>
                        <p>Detailed mapping of botanical observations across the Forest Preserves of Cook County.</p>
                        <a href="/plants" class="nav a" style="display:inline-block; margin-top:10px; padding: 5px 10px; background:#6610f2;">View Plant Data</a>
                    </div>
                    <div class="card">
                        <h4>Hydrological Mapping</h4>
                        <p>Chicago River and Lake survey locations with water quality indicators.</p>
                        <a href="/lakes" class="nav a" style="display:inline-block; margin-top:10px; padding: 5px 10px; background:#6610f2;">View River &amp; Lake Data</a>
                    </div>
                    <div class="card">
                        <h4>Urban Wildlife Corridors</h4>
                        <p>Mapping animal behaviors and sightings in urban and suburban environments.</p>
                        <a href="/animals" class="nav a" style="display:inline-block; margin-top:10px; padding: 5px 10px; background:#6610f2;">View Animal Data</a>
                    </div>
                </div>
            </div>
        </body>
        </html>
        """
        self.serve_html(html)

    def serve_squirrel_model(self):
        try:
            response = client.responses.create(
                model="gpt-4o",
                prompt={
                    "id": "pmpt_697e4b151b2c8190a992e1146a2f2f410fb0045d5f65d9e8",
                    "version": "6"
                }
            )
            ai_content = str(response)
        except Exception as e:
            ai_content = f"Error generating squirrel model: {str(e)}"

        # Fetch Sodium Trap / GUD entries to embed below AI output
        gud_entries = db.get_gud_entries()
        gud_entries_html = ""
        for entry in gud_entries:
            gud_entries_html += f"""
            <div class="card">
                <h4>{entry.get('site_type', 'N/A')} Site — {entry.get('date', 'N/A')}</h4>
                <p><strong>Sodium Multiplier (λ):</strong> {entry.get('sodium_multiplier', 1.0):.2f}</p>
                <p><strong>Acoustic Masking (1–5):</strong> {entry.get('mask_a', 'N/A')}</p>
                <p><strong>Visibility Score (1–5):</strong> {entry.get('vis_score', 'N/A')}</p>
                <p><strong>Dist. to River Road:</strong> {entry.get('dist_to_road', 'N/A')} m</p>
                <p><strong>Pace Bus Active:</strong> {"Yes" if entry.get('transit_active') else "No"}</p>
                <p><strong>Predator Cues:</strong> {entry.get('predator_cues_hd', 0)} (H/D), {entry.get('predator_cues_ac', 0)} (Alarm)</p>
                {f"<p><strong>Notes:</strong> {entry.get('notes', '')}</p>" if entry.get('notes') else ""}
            </div>
            """

        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Squirrel AI &amp; Sodium Trap - CULAP Data Camp and Education Center</title>
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <style>
                body {{ font-family: Arial, sans-serif; margin: 0; padding: 20px; background-color: #f5f5f5; }}
                .container {{ max-width: 1200px; margin: 0 auto; }}
                .header {{ background-color: #17a2b8; color: white; padding: 20px; border-radius: 8px; margin-bottom: 20px; }}
                .section-header {{ background-color: #ffc107; color: #333; padding: 15px 20px; border-radius: 8px; margin: 30px 0 15px 0; }}
                .nav {{ display: flex; flex-wrap: wrap; gap: 10px; margin-bottom: 20px; }}
                .nav a {{ background-color: #007bff; color: white; padding: 10px 15px; text-decoration: none; border-radius: 5px; }}
                .nav a:hover {{ background-color: #0056b3; }}
                .card {{ background: white; padding: 20px; margin: 10px 0; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
                .grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; }}
                .add-btn {{ background-color: #ffc107; color: #333; padding: 10px 20px; text-decoration: none; border-radius: 5px; display: inline-block; margin-bottom: 20px; font-weight: bold; }}
                .add-btn:hover {{ background-color: #e0a800; }}
                pre {{ background: #eee; padding: 15px; border-radius: 5px; overflow-x: auto; white-space: pre-wrap; }}
            </style>
        <link rel="stylesheet" href="https://unpkg.com/@algolia/sitesearch@latest/dist/search.min.css" />
    <script src="https://unpkg.com/@algolia/sitesearch@latest/dist/search.min.js"></script>
</head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🐿️ Squirrel AI Behavioral Model</h1>
                    <p>Powered by OpenAI Project Integration</p>
                </div>
                <div class="nav">
                    <a href="/">Home</a>
                    <a href="/weather">Weather</a>
                    <a href="/plants">Plants</a>
                    
                    <a href="/lakes">Lakes &amp; River</a>
                    <a href="/animals">Animals</a>
                    
                    <a href="/garbage_cans">Garbage Cans</a>
                    <a href="/we-convene-science">We Convene Science</a>
                    <a href="/maps">Maps</a>
                    <a href="/statistics">Statistics</a>
                </div>
                <div id="search" style="margin-bottom: 20px;"></div>
                <script>
                  SiteSearch.init({{
                    container: "#search",
                    applicationId: "G1S1VRTBX5",
                    apiKey: "5d5d722782d6b620065a475f91221e18",
                    indexName: "test_schiller_woods_scenariosss",
                    attributes: {{
                      primaryText: "date",
                      secondaryText: undefined,
                      tertiaryText: undefined,
                      url: "",
                      image: undefined
                    }},
                    darkMode: false,
                  }});
                </script>

                <div class="card">
                    <h3>🤖 AI Model Output</h3>
                    <p>Response from your customized OpenAI prompt (ID: pmpt_697e4...):</p>
                    <pre>{ai_content}</pre>
                </div>

                <div class="section-header">
                    <h2>🐿️ Sodium Trap Project (BIOS 399)</h2>
                    <p>Modeling GUD curves and urban stressors at Schiller Woods — River Bend Picnic Area</p>
                </div>

                <a href="/add_gud_entry" class="add-btn">➕ Add GUD Observation</a>

                <div class="grid">
                    {gud_entries_html if gud_entries_html else '<div class="card"><p>No GUD entries yet. Add your first observation above!</p></div>'}
                </div>
            </div>
        </body>
        </html>
        """
        self.serve_html(html)

    def serve_squirrel_data_api(self):
        try:
            entries = db.get_gud_entries()
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*') # Allow Colab to fetch
            self.end_headers()
            self.wfile.write(json.dumps(entries).encode())
        except Exception as e:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(json.dumps({"error": str(e)}).encode())

    def serve_statistics(self):
        stats = db.get_statistics()

        # Calculate temperature statistics if weather data exists
        weather_entries = db.get_weather_entries()
        temp_stats = ""
        if weather_entries:
            temps = []
            for entry in weather_entries:
                try:
                    temp = float(entry.get('temperature', 0))
                    if temp > 0:  # Only include valid temperatures
                        temps.append(temp)
                except (ValueError, TypeError):
                    continue

            if temps:
                avg_temp = sum(temps) / len(temps)
                min_temp = min(temps)
                max_temp = max(temps)
                temp_stats = f"""
                <p><strong>Average Temperature:</strong> {avg_temp:.1f}°F</p>
                <p><strong>Minimum Temperature:</strong> {min_temp}°F</p>
                <p><strong>Maximum Temperature:</strong> {max_temp}°F</p>
                """

        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Statistics - Chicago Environmental Observations</title>
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <style>
                body {{ font-family: Arial, sans-serif; margin: 0; padding: 20px; background-color: #f5f5f5; }}
                .container {{ max-width: 1200px; margin: 0 auto; }}
                .header {{ background-color: #28a745; color: white; padding: 20px; border-radius: 8px; margin-bottom: 20px; }}
                .nav {{ display: flex; flex-wrap: wrap; gap: 10px; margin-bottom: 20px; }}
                .nav a {{ background-color: #007bff; color: white; padding: 10px 15px; text-decoration: none; border-radius: 5px; }}
                .nav a:hover {{ background-color: #0056b3; }}
                .card {{ background: white; padding: 20px; margin: 10px 0; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
                .stat-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; }}
                .stat-card {{ text-align: center; padding: 20px; background: linear-gradient(135deg, #007bff, #0056b3); color: white; border-radius: 8px; }}
                .stat-number {{ font-size: 2em; font-weight: bold; }}
            </style>
        <link rel="stylesheet" href="https://unpkg.com/@algolia/sitesearch@latest/dist/search.min.css" />
    <script src="https://unpkg.com/@algolia/sitesearch@latest/dist/search.min.js"></script>
</head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>📊 Statistics</h1>
                </div>

                <div class="nav">
                    <a href="/">Home</a>
                    <a href="/weather">Weather</a>
                    <a href="/plants">Plants</a>
                    
                    <a href="/lakes">Lakes &amp; River</a>
                    <a href="/animals">Animals</a>
                    
                    <a href="/garbage_cans">Garbage Cans</a>
                    
                    <a href="/we-convene-science">We Convene Science</a>
                    <a href="/maps">Maps</a>
                    <a href="/statistics">Statistics</a>
                </div>
                <div id="search" style="margin-bottom: 20px;"></div>
                <script>
                  SiteSearch.init({{
                    container: "#search",
                    applicationId: "G1S1VRTBX5",
                    apiKey: "5d5d722782d6b620065a475f91221e18",
                    indexName: "test_schiller_woods_scenariosss",
                    attributes: {{
                      primaryText: "date",
                      secondaryText: undefined,
                      tertiaryText: undefined,
                      url: "",
                      image: undefined
                    }},
                    darkMode: false,
                  }});
                </script>

                <div class="stat-grid">
                    <div class="stat-card">
                        <div class="stat-number">{stats['total_weather_entries']}</div>
                        <div>Weather Entries</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-number">{stats['total_plant_entries']}</div>
                        <div>Plant Observations</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-number">{stats['total_river_entries']}</div>
                        <div>River Observations</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-number">{stats['total_lake_entries']}</div>
                        <div>Lake Surveys</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-number">{stats['total_animal_entries']}</div>
                        <div>Animal Observations</div>
                    </div>
                     <div class="stat-card">
                        <div class="stat-number">{stats['total_garbage_can_entries']}</div>
                        <div>Garbage Can Observations</div>
                    </div>
                </div>

                {f'<div class="card"><h3>Temperature Statistics</h3>{temp_stats}</div>' if temp_stats else ''}
            </div>
        </body>
        </html>
        """
        self.serve_html(html)

    def serve_weather_form(self):
        html = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Add Weather Entry - Chicago Environmental Observations</title>
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <style>
                body { font-family: Arial, sans-serif; margin: 0; padding: 20px; background-color: #f5f5f5; }
                .container { max-width: 800px; margin: 0 auto; }
                .header { background-color: #28a745; color: white; padding: 20px; border-radius: 8px; margin-bottom: 20px; }
                .nav { display: flex; flex-wrap: wrap; gap: 10px; margin-bottom: 20px; }
                .nav a { background-color: #007bff; color: white; padding: 10px 15px; text-decoration: none; border-radius: 5px; }
                .nav a:hover { background-color: #0056b3; }
                .card { background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
                .form-group { margin-bottom: 15px; }
                label { display: block; margin-bottom: 5px; font-weight: bold; }
                input, select, textarea { width: 100%; padding: 8px; border: 1px solid #ddd; border-radius: 4px; box-sizing: border-box; }
                textarea { height: 100px; resize: vertical; }
                button { background-color: #28a745; color: white; padding: 12px 30px; border: none; border-radius: 5px; cursor: pointer; font-size: 16px; }
                button:hover { background-color: #218838; }
                .back-btn { background-color: #6c757d; color: white; padding: 8px 15px; text-decoration: none; border-radius: 5px; display: inline-block; margin-bottom: 20px; }
                .back-btn:hover { background-color: #5a6268; }
            </style>
        <link rel="stylesheet" href="https://unpkg.com/@algolia/sitesearch@latest/dist/search.min.css" />
    <script src="https://unpkg.com/@algolia/sitesearch@latest/dist/search.min.js"></script>
</head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🌦️ Add Weather Entry</h1>
                </div>

                <div class="nav">
                    <a href="/">Home</a>
                    <a href="/weather">Weather</a>
                    <a href="/plants">Plants</a>
                    
                    <a href="/lakes">Lakes &amp; River</a>
                    <a href="/animals">Animals</a>
                    
                    <a href="/garbage_cans">Garbage Cans</a>
                    
                    <a href="/we-convene-science">We Convene Science</a>
                    <a href="/maps">Maps</a>
                    <a href="/statistics">Statistics</a>
                </div>
                <div id="search" style="margin-bottom: 20px;"></div>
                <script>
                  SiteSearch.init({{
                    container: "#search",
                    applicationId: "G1S1VRTBX5",
                    apiKey: "5d5d722782d6b620065a475f91221e18",
                    indexName: "test_schiller_woods_scenariosss",
                    attributes: {{
                      primaryText: "date",
                      secondaryText: undefined,
                      tertiaryText: undefined,
                      url: "",
                      image: undefined
                    }},
                    darkMode: false,
                  }});
                </script>

                <a href="/weather" class="back-btn">← Back to Weather</a>

                <div class="card">
                    <form method="POST" action="/add_weather">
                        <div class="form-group">
                            <label for="date">Date:</label>
                            <input type="date" id="date" name="date" required>
                        </div>

                        <div class="form-group">
                            <label for="location">Location:</label>
                            <input type="text" id="location" name="location" placeholder="e.g., Downtown Chicago, Evanston, etc." required>
                        </div>

                        <div class="form-group">
                            <label for="temperature">Temperature (°F):</label>
                            <input type="number" id="temperature" name="temperature" step="0.1" required>
                        </div>

                        <div class="form-group">
                            <label for="humidity">Humidity (%):</label>
                            <input type="number" id="humidity" name="humidity" min="0" max="100" required>
                        </div>

                        <div class="form-group">
                            <label for="precipitation">Precipitation (inches):</label>
                            <input type="number" id="precipitation" name="precipitation" step="0.01" min="0" required>
                        </div>

                        <div class="form-group">
                            <label for="wind_speed">Wind Speed (mph):</label>
                            <input type="number" id="wind_speed" name="wind_speed" step="0.1" min="0" required>
                        </div>

                        <div class="form-group">
                            <label for="conditions">Weather Conditions:</label>
                            <select id="conditions" name="conditions" required>
                                <option value="">Select conditions</option>
                                <option value="Sunny">Sunny</option>
                                <option value="Partly Cloudy">Partly Cloudy</option>
                                <option value="Cloudy">Cloudy</option>
                                <option value="Overcast">Overcast</option>
                                <option value="Light Rain">Light Rain</option>
                                <option value="Heavy Rain">Heavy Rain</option>
                                <option value="Snow">Snow</option>
                                <option value="Fog">Fog</option>
                                <option value="Thunderstorm">Thunderstorm</option>
                            </select>
                        </div>

                        <div class="form-group">
                            <label for="notes">Notes (optional):</label>
                            <textarea id="notes" name="notes" placeholder="Additional observations..."></textarea>
                        </div>

                        <button type="submit">Add Weather Entry</button>
                    </form>
                </div>
            </div>
        </body>
        </html>
        """
        self.serve_html(html)

    def serve_plant_form(self):
        html = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Add Plant Observation - Chicago Environmental Observations</title>
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <style>
                body { font-family: Arial, sans-serif; margin: 0; padding: 20px; background-color: #f5f5f5; }
                .container { max-width: 800px; margin: 0 auto; }
                .header { background-color: #28a745; color: white; padding: 20px; border-radius: 8px; margin-bottom: 20px; }
                .nav { display: flex; flex-wrap: wrap; gap: 10px; margin-bottom: 20px; }
                .nav a { background-color: #007bff; color: white; padding: 10px 15px; text-decoration: none; border-radius: 5px; }
                .nav a:hover { background-color: #0056b3; }
                .card { background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
                .form-group { margin-bottom: 15px; }
                label { display: block; margin-bottom: 5px; font-weight: bold; }
                input, select, textarea { width: 100%; padding: 8px; border: 1px solid #ddd; border-radius: 4px; box-sizing: border-box; }
                textarea { height: 100px; resize: vertical; }
                button { background-color: #28a745; color: white; padding: 12px 30px; border: none; border-radius: 5px; cursor: pointer; font-size: 16px; }
                button:hover { background-color: #218838; }
                .back-btn { background-color: #6c757d; color: white; padding: 8px 15px; text-decoration: none; border-radius: 5px; display: inline-block; margin-bottom: 20px; }
                .back-btn:hover { background-color: #5a6268; }
            </style>
        <link rel="stylesheet" href="https://unpkg.com/@algolia/sitesearch@latest/dist/search.min.css" />
    <script src="https://unpkg.com/@algolia/sitesearch@latest/dist/search.min.js"></script>
</head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🌸 Add Plant Observation</h1>
                </div>

                <div class="nav">
                    <a href="/">Home</a>
                    <a href="/weather">Weather</a>
                    <a href="/plants">Plants</a>
                    
                    <a href="/lakes">Lakes &amp; River</a>
                    <a href="/animals">Animals</a>
                     <a href="/garbage_cans">Garbage Cans</a>
                    <a href="/statistics">Statistics</a>
                </div>

                <a href="/plants" class="back-btn">← Back to Plants</a>

                <div class="card">
                    <form method="POST" action="/add_plant">
                        <div class="form-group">
                            <label for="date">Date:</label>
                            <input type="date" id="date" name="date" required>
                        </div>

                        <div class="form-group">
                            <label for="preserve">Forest Preserve:</label>
                            <input type="text" id="preserve" name="preserve" placeholder="e.g., Busse Woods, Waterfall Glen, etc." required>
                        </div>

                        <div class="form-group">
                            <label for="species_name">Species Name (Scientific):</label>
                            <input type="text" id="species_name" name="species_name" placeholder="e.g., Quercus alba" required>
                        </div>

                        <div class="form-group">
                            <label for="common_name">Common Name:</label>
                            <input type="text" id="common_name" name="common_name" placeholder="e.g., White Oak" required>
                        </div>

                        <div class="form-group">
                            <label for="location_details">Location Details:</label>
                            <input type="text" id="location_details" name="location_details" placeholder="Specific location within preserve" required>
                        </div>

                        <div class="form-group">
                            <label for="abundance">Abundance:</label>
                            <select id="abundance" name="abundance" required>
                                <option value="">Select abundance</option>
                                <option value="Rare">Rare (1-5 individuals)</option>
                                <option value="Uncommon">Uncommon (6-25 individuals)</option>
                                <option value="Common">Common (26-100 individuals)</option>
                                <option value="Abundant">Abundant (100+ individuals)</option>
                            </select>
                        </div>

                        <div class="form-group">
                            <label for="flowering_status">Flowering Status:</label>
                            <select id="flowering_status" name="flowering_status" required>
                                <option value="">Select status</option>
                                <option value="Not flowering">Not flowering</option>
                                <option value="Budding">Budding</option>
                                <option value="Flowering">Flowering</option>
                                <option value="Fruiting">Fruiting</option>
                                <option value="Seeding">Seeding</option>
                                <option value="Dormant">Dormant</option>
                            </select>
                        </div>

                        <div class="form-group">
                            <label for="habitat">Habitat:</label>
                            <input type="text" id="habitat" name="habitat" placeholder="e.g., Wetland, Prairie, Woodland" required>
                        </div>

                        <div class="form-group">
                            <label for="notes">Notes (optional):</label>
                            <textarea id="notes" name="notes" placeholder="Additional observations, condition notes, etc."></textarea>
                        </div>

                        <button type="submit">Add Plant Observation</button>
                    </form>
                </div>
            </div>
        </body>
        </html>
        """
        self.serve_html(html)

    def serve_river_form(self):
        html = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Add River Observation - Chicago Environmental Observations</title>
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <style>
                body { font-family: Arial, sans-serif; margin: 0; padding: 20px; background-color: #f5f5f5; }
                .container { max-width: 800px; margin: 0 auto; }
                .header { background-color: #28a745; color: white; padding: 20px; border-radius: 8px; margin-bottom: 20px; }
                .nav { display: flex; flex-wrap: wrap; gap: 10px; margin-bottom: 20px; }
                .nav a { background-color: #007bff; color: white; padding: 10px 15px; text-decoration: none; border-radius: 5px; }
                .nav a:hover { background-color: #0056b3; }
                .card { background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
                .form-group { margin-bottom: 15px; }
                label { display: block; margin-bottom: 5px; font-weight: bold; }
                input, select, textarea { width: 100%; padding: 8px; border: 1px solid #ddd; border-radius: 4px; box-sizing: border-box; }
                textarea { height: 100px; resize: vertical; }
                button { background-color: #28a745; color: white; padding: 12px 30px; border: none; border-radius: 5px; cursor: pointer; font-size: 16px; }
                button:hover { background-color: #218838; }
                .back-btn { background-color: #6c757d; color: white; padding: 8px 15px; text-decoration: none; border-radius: 5px; display: inline-block; margin-bottom: 20px; }
                .back-btn:hover { background-color: #5a6268; }
            </style>
        <link rel="stylesheet" href="https://unpkg.com/@algolia/sitesearch@latest/dist/search.min.css" />
    <script src="https://unpkg.com/@algolia/sitesearch@latest/dist/search.min.js"></script>
</head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🌊 Add River Observation</h1>
                </div>

                <div class="nav">
                    <a href="/">Home</a>
                    <a href="/weather">Weather</a>
                    <a href="/plants">Plants</a>
                    
                    <a href="/lakes">Lakes &amp; River</a>
                    <a href="/animals">Animals</a>
                     <a href="/garbage_cans">Garbage Cans</a>
                    <a href="/statistics">Statistics</a>
                </div>

                <a href="/lakes" class="back-btn">← Back to Lakes &amp; River</a>

                <div class="card">
                    <form method="POST" action="/add_river">
                        <div class="form-group">
                            <label for="date">Date:</label>
                            <input type="date" id="date" name="date" required>
                        </div>

                        <div class="form-group">
                            <label for="location">Location on Chicago River:</label>
                            <input type="text" id="location" name="location" placeholder="e.g., Navy Pier, Riverwalk, North Branch" required>
                        </div>

                        <div class="form-group">
                            <label for="water_level">Water Level:</label>
                            <select id="water_level" name="water_level" required>
                                <option value="">Select water level</option>
                                <option value="Very Low">Very Low</option>
                                <option value="Low">Low</option>
                                <option value="Normal">Normal</option>
                                <option value="High">High</option>
                                <option value="Very High">Very High</option>
                            </select>
                        </div>

                        <div class="form-group">
                            <label for="water_clarity">Water Clarity:</label>
                            <select id="water_clarity" name="water_clarity" required>
                                <option value="">Select clarity</option>
                                <option value="Clear">Clear</option>
                                <option value="Slightly Turbid">Slightly Turbid</option>
                                <option value="Turbid">Turbid</option>
                                <option value="Very Turbid">Very Turbid</option>
                                <option value="Muddy">Muddy</option>
                            </select>
                        </div>

                        <div class="form-group">
                            <label for="temperature">Water Temperature (°F, optional):</label>
                            <input type="number" id="temperature" name="temperature" step="0.1">
                        </div>

                        <div class="form-group">
                            <label for="flow_rate">Flow Rate:</label>
                            <select id="flow_rate" name="flow_rate" required>
                                <option value="">Select flow rate</option>
                                <option value="Very Slow">Very Slow</option>
                                <option value="Slow">Slow</option>
                                <option value="Moderate">Moderate</option>
                                <option value="Fast">Fast</option>
                                <option value="Very Fast">Very Fast</option>
                            </select>
                        </div>

                        <div class="form-group">
                            <label for="wildlife_observed">Wildlife Observed:</label>
                            <input type="text" id="wildlife_observed" name="wildlife_observed" placeholder="e.g., Mallards, Canada Geese, Fish jumping" required>
                        </div>

                        <div class="form-group">
                            <label for="pollution_indicators">Pollution Indicators:</label>
                            <input type="text" id="pollution_indicators" name="pollution_indicators" placeholder="e.g., Foam, Oil sheen, Debris, None observed" required>
                        </div>

                        <div class="form-group">
                            <label for="notes">Notes (optional):</label>
                            <textarea id="notes" name="notes" placeholder="Additional observations about water quality, wildlife behavior, etc."></textarea>
                        </div>

                        <button type="submit">Add River Observation</button>
                    </form>
                </div>
            </div>
        </body>
        </html>
        """
        self.serve_html(html)

    def serve_lake_form(self):
        html = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Add Lake Survey - Chicago Environmental Observations</title>
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <style>
                body { font-family: Arial, sans-serif; margin: 0; padding: 20px; background-color: #f5f5f5; }
                .container { max-width: 800px; margin: 0 auto; }
                .header { background-color: #28a745; color: white; padding: 20px; border-radius: 8px; margin-bottom: 20px; }
                .nav { display: flex; flex-wrap: wrap; gap: 10px; margin-bottom: 20px; }
                .nav a { background-color: #007bff; color: white; padding: 10px 15px; text-decoration: none; border-radius: 5px; }
                .nav a:hover { background-color: #0056b3; }
                .card { background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
                .form-group { margin-bottom: 15px; }
                label { display: block; margin-bottom: 5px; font-weight: bold; }
                input, select, textarea { width: 100%; padding: 8px; border: 1px solid #ddd; border-radius: 4px; box-sizing: border-box; }
                textarea { height: 100px; resize: vertical; }
                button { background-color: #28a745; color: white; padding: 12px 30px; border: none; border-radius: 5px; cursor: pointer; font-size: 16px; }
                button:hover { background-color: #218838; }
                .back-btn { background-color: #6c757d; color: white; padding: 8px 15px; text-decoration: none; border-radius: 5px; display: inline-block; margin-bottom: 20px; }
                .back-btn:hover { background-color: #5a6268; }
            </style>
        <link rel="stylesheet" href="https://unpkg.com/@algolia/sitesearch@latest/dist/search.min.css" />
    <script src="https://unpkg.com/@algolia/sitesearch@latest/dist/search.min.js"></script>
</head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>💧 Add Lake Survey</h1>
                </div>

                <div class="nav">
                    <a href="/">Home</a>
                    <a href="/weather">Weather</a>
                    <a href="/plants">Plants</a>
                    
                    <a href="/lakes">Lakes &amp; River</a>
                    <a href="/animals">Animals</a>
                     <a href="/garbage_cans">Garbage Cans</a>
                    <a href="/statistics">Statistics</a>
                </div>

                <a href="/lakes" class="back-btn">← Back to Lakes</a>

                <div class="card">
                    <form method="POST" action="/add_lake">
                        <div class="form-group">
                            <label for="date">Date:</label>
                            <input type="date" id="date" name="date" required>
                        </div>

                        <div class="form-group">
                            <label for="lake_name">Lake Name:</label>
                            <input type="text" id="lake_name" name="lake_name" placeholder="e.g., Busse Lake, Skokie Lagoons" required>
                        </div>

                        <div class="form-group">
                            <label for="fishing_method">Fishing Method:</label>
                            <select id="fishing_method" name="fishing_method" required>
                                <option value="">Select method</option>
                                <option value="Shore fishing">Shore fishing</option>
                                <option value="Boat fishing">Boat fishing</option>
                                <option value="Kayak fishing">Kayak fishing</option>
                                <option value="Wade fishing">Wade fishing</option>
                                <option value="Observation only">Observation only</option>
                            </select>
                        </div>

                        <div class="form-group">
                            <label for="fish_species">Fish Species Caught/Observed:</label>
                            <input type="text" id="fish_species" name="fish_species" placeholder="e.g., Largemouth Bass, Bluegill, Northern Pike" required>
                        </div>

                        <div class="form-group">
                            <label for="fish_count">Number of Fish Caught/Observed:</label>
                            <input type="number" id="fish_count" name="fish_count" min="0">
                        </div>

                        <div class="form-group">
                            <label for="fish_size_avg">Average Fish Size (inches, optional):</label>
                            <input type="number" id="fish_size_avg" name="fish_size_avg" step="0.1" min="0">
                        </div>

                        <div class="form-group">
                            <label for="frogs_observed">Frogs Observed:</label>
                            <input type="text" id="frogs_observed" name="frogs_observed" placeholder="e.g., American Bullfrogs, Green Frogs, None observed">
                        </div>

                        <div class="form-group">
                            <label for="turtles_observed">Turtles Observed:</label>
                            <input type="text" id="turtles_observed" name="turtles_observed" placeholder="e.g., Painted Turtles, Snapping Turtle, None observed">
                        </div>

                        <div class="form-group">
                            <label for="water_temperature">Water Temperature (°F, optional):</label>
                            <input type="number" id="water_temperature" name="water_temperature" step="0.1">
                        </div>

                        <div class="form-group">
                            <label for="water_clarity">Water Clarity:</label>
                            <select id="water_clarity" name="water_clarity" required>
                                <option value="">Select clarity</option>
                                <option value="Crystal Clear">Crystal Clear</option>
                                <option value="Clear">Clear</option>
                                <option value="Slightly Turbid">Slightly Turbid</option>
                                <option value="Turbid">Turbid</option>
                                <option value="Very Turbid">Very Turbid</option>
                                <option value="Muddy">Muddy</option>
                            </select>
                        </div>

                        <div class="form-group">
                            <label for="notes">Notes (optional):</label>
                            <textarea id="notes" name="notes" placeholder="Weather conditions, bait used, fishing success, aquatic vegetation, etc."></textarea>
                        </div>

                        <button type="submit">Add Lake Survey</button>
                    </form>
                </div>
            </div>
        </body>
        </html>
        """
        self.serve_html(html)

    def serve_animal_form(self):
        html = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Add Animal Observation - Chicago Environmental Observations</title>
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <style>
                body { font-family: Arial, sans-serif; margin: 0; padding: 20px; background-color: #f5f5f5; }
                .container { max-width: 800px; margin: 0 auto; }
                .header { background-color: #28a745; color: white; padding: 20px; border-radius: 8px; margin-bottom: 20px; }
                .nav { display: flex; flex-wrap: wrap; gap: 10px; margin-bottom: 20px; }
                .nav a { background-color: #007bff; color: white; padding: 10px 15px; text-decoration: none; border-radius: 5px; }
                .nav a:hover { background-color: #0056b3; }
                .card { background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
                .form-group { margin-bottom: 15px; }
                label { display: block; margin-bottom: 5px; font-weight: bold; }
                input, select, textarea { width: 100%; padding: 8px; border: 1px solid #ddd; border-radius: 4px; box-sizing: border-box; }
                textarea { height: 100px; resize: vertical; }
                button { background-color: #28a745; color: white; padding: 12px 30px; border: none; border-radius: 5px; cursor: pointer; font-size: 16px; }
                button:hover { background-color: #218838; }
                .back-btn { background-color: #6c757d; color: white; padding: 8px 15px; text-decoration: none; border-radius: 5px; display: inline-block; margin-bottom: 20px; }
                .back-btn:hover { background-color: #5a6268; }
            </style>
        <link rel="stylesheet" href="https://unpkg.com/@algolia/sitesearch@latest/dist/search.min.css" />
    <script src="https://unpkg.com/@algolia/sitesearch@latest/dist/search.min.js"></script>
</head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🦌 Add Animal Observation</h1>
                </div>

                <div class="nav">
                    <a href="/">Home</a>
                    <a href="/weather">Weather</a>
                    <a href="/plants">Plants</a>
                    
                    <a href="/lakes">Lakes &amp; River</a>
                    <a href="/animals">Animals</a>
                     <a href="/garbage_cans">Garbage Cans</a>
                    <a href="/statistics">Statistics</a>
                </div>

                <a href="/animals" class="back-btn">← Back to Animals</a>

                <div class="card">
                    <form method="POST" action="/add_animal">
                        <div class="form-group">
                            <label for="date">Date:</label>
                            <input type="date" id="date" name="date" required>
                        </div>

                        <div class="form-group">
                            <label for="location">Location:</label>
                            <input type="text" id="location" name="location" placeholder="e.g., Lincoln Park Zoo, Forest Preserve, Lakefront" required>
                        </div>

                        <div class="form-group">
                            <label for="species">Species (Scientific Name):</label>
                            <input type="text" id="species" name="species" placeholder="e.g., Odocoileus virginianus" required>
                        </div>

                        <div class="form-group">
                            <label for="common_name">Common Name:</label>
                            <input type="text" id="common_name" name="common_name" placeholder="e.g., White-tailed Deer" required>
                        </div>

                        <div class="form-group">
                            <label for="number_observed">Number Observed:</label>
                            <input type="number" id="number_observed" name="number_observed" min="1" value="1" required>
                        </div>

                        <div class="form-group">
                            <label for="behavior">Behavior:</label>
                            <input type="text" id="behavior" name="behavior" placeholder="e.g., Feeding, Nesting, Resting, Moving" required>
                        </div>

                        <div class="form-group">
                            <label for="habitat">Habitat:</label>
                            <select id="habitat" name="habitat" required>
                                <option value="">Select habitat</option>
                                <option value="Urban park">Urban park</option>
                                <option value="Forest">Forest</option>
                                <option value="Prairie">Prairie</option>
                                <option value="Wetland">Wetland</option>
                                <option value="Lakefront">Lakefront</option>
                                <option value="Residential area">Residential area</option>
                                <option value="Agricultural area">Agricultural area</option>
                                <option value="River/Stream">River/Stream</option>
                            </select>
                        </div>

                        <div class="form-group">
                            <label for="time_of_day">Time of Day:</label>
                            <select id="time_of_day" name="time_of_day" required>
                                <option value="">Select time</option>
                                <option value="Early Morning">Early Morning (5-8 AM)</option>
                                <option value="Morning">Morning (8-11 AM)</option>
                                <option value="Midday">Midday (11 AM-2 PM)</option>
                                <option value="Afternoon">Afternoon (2-5 PM)</option>
                                       <option value="Evening">Evening (5-8 PM)</option>
                                <option value="Dusk">Dusk (8-10 PM)</option>
                                <option value="Night">Night (10 PM-5 AM)</option>
                            </select>
                        </div>

                        <div class="form-group">
                            <label for="weather_conditions">Weather Conditions:</label>
                            <input type="text" id="weather_conditions" name="weather_conditions" placeholder="e.g., Sunny, 75°F, Light breeze" required>
                        </div>

                        <div class="form-group">
                            <label for="notes">Notes (optional):</label>
                            <textarea id="notes" name="notes" placeholder="Additional observations, age/sex if determinable, interaction with other animals, etc."></textarea>
                        </div>

                        <button type="submit">Add Animal Observation</button>
                    </form>
                </div>
            </div>
        </body>
        </html>
        """
        self.serve_html(html)

    def serve_garbage_can_form(self):
        html = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Add Garbage Can Observation - Chicago Environmental Observations</title>
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <style>
                body { font-family: Arial, sans-serif; margin: 0; padding: 20px; background-color: #f5f5f5; }
                .container { max-width: 800px; margin: 0 auto; }
                .header { background-color: #28a745; color: white; padding: 20px; border-radius: 8px; margin-bottom: 20px; }
                .nav { display: flex; flex-wrap: wrap; gap: 10px; margin-bottom: 20px; }
                .nav a { background-color: #007bff; color: white; padding: 10px 15px; text-decoration: none; border-radius: 5px; }
                .nav a:hover { background-color: #0056b3; }
                .card { background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
                .form-group { margin-bottom: 15px; }
                label { display: block; margin-bottom: 5px; font-weight: bold; }
                input, select, textarea { width: 100%; padding: 8px; border: 1px solid #ddd; border-radius: 4px; box-sizing: border-box; }
                textarea { height: 100px; resize: vertical; }
                button { background-color: #28a745; color: white; padding: 12px 30px; border: none; border-radius: 5px; cursor: pointer; font-size: 16px; }
                button:hover { background-color: #218838; }
                .back-btn { background-color: #6c757d; color: white; padding: 8px 15px; text-decoration: none; border-radius: 5px; display: inline-block; margin-bottom: 20px; }
                .back-btn:hover { background-color: #5a6268; }
            </style>
        <link rel="stylesheet" href="https://unpkg.com/@algolia/sitesearch@latest/dist/search.min.css" />
    <script src="https://unpkg.com/@algolia/sitesearch@latest/dist/search.min.js"></script>
</head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🗑️ Add Garbage Can Observation</h1>
                </div>

                <div class="nav">
                    <a href="/">Home</a>
                    <a href="/weather">Weather</a>
                    <a href="/plants">Plants</a>
                    
                    <a href="/lakes">Lakes &amp; River</a>
                    <a href="/animals">Animals</a>
                    
                    <a href="/garbage_cans">Garbage Cans</a>
                    
                    <a href="/we-convene-science">We Convene Science</a>
                    <a href="/maps">Maps</a>
                    <a href="/statistics">Statistics</a>
                </div>
                <div id="search" style="margin-bottom: 20px;"></div>
                <script>
                  SiteSearch.init({{
                    container: "#search",
                    applicationId: "G1S1VRTBX5",
                    apiKey: "5d5d722782d6b620065a475f91221e18",
                    indexName: "test_schiller_woods_scenariosss",
                    attributes: {{
                      primaryText: "date",
                      secondaryText: undefined,
                      tertiaryText: undefined,
                      url: "",
                      image: undefined
                    }},
                    darkMode: false,
                  }});
                </script>

                <a href="/garbage_cans" class="back-btn">← Back to Garbage Cans</a>

                <div class="card">
                    <form method="POST" action="/add_garbage_can">
                        <div class="form-group">
                            <label for="date">Date:</label>
                            <input type="date" id="date" name="date" required>
                        </div>

                        <div class="form-group">
                            <label for="location">Location:</label>
                            <input type="text" id="location" name="location" placeholder="e.g., Alley behind restaurant, Park near picnic tables" required>
                        </div>

                         <div class="form-group">
                            <label for="garbage_can_id">Garbage Can ID:</label>
                            <input type="text" id="garbage_can_id" name="garbage_can_id" placeholder="e.g., CAN-123, PARK-007" required>
                        </div>

                        <div class="form-group">
                            <label for="ant_species">Ant Species:</label>
                            <input type="text" id="ant_species" name="ant_species" placeholder="e.g., Lasius neoniger, Crematogaster lineolata" required>
                        </div>

                        <div class="form-group">
                            <label for="colony_size">Colony Size:</label>
                            <select id="colony_size" name="colony_size" required>
                                <option value="">Select size</option>
                                <option value="Small">Small (1-10 ants)</option>
                                <option value="Medium">Medium (11-50 ants)</option>
                                <option value="Large">Large (51-200 ants)</option>
                                <option value="Very Large">Very Large (200+ ants)</option>
                            </select>
                        </div>

                        <div class="form-group">
                            <label for="notes">Notes (optional):</label>
                            <textarea id="notes" name="notes" placeholder="Additional observations about ant behavior, food sources, etc."></textarea>
                        </div>

                        <button type="submit">Add Garbage Can Observation</button>
                    </form>
                </div>
            </div>
        </body>
        </html>
        """
        self.serve_html(html)

    def serve_learning_center(self):
        resources = db.get_learning_resources()
        resources_html = ""
        for resource in resources:
            resources_html += f"""
            <div class="card">
                <h4>{resource.get('title', 'Untitled Resource')}</h4>
                <p><strong>Category:</strong> {resource.get('category', 'N/A')}</p>
                <p><strong>Description:</strong> {resource.get('description', 'N/A')}</p>
                <p><strong>URL:</strong> <a href="{resource.get('url', '#')}" target="_blank">{resource.get('url', 'N/A')}</a></p>
                <p><strong>Added:</strong> {resource.get('date', 'N/A')}</p>
            </div>
            """

        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>We Convene Science Learning Resource Center</title>
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <style>
                body {{ font-family: Arial, sans-serif; margin: 0; padding: 20px; background-color: #f5f5f5; }}
                .container {{ max-width: 1200px; margin: 0 auto; }}
                .header {{ background-color: #0066cc; color: white; padding: 20px; border-radius: 8px; margin-bottom: 20px; }}
                .nav {{ display: flex; flex-wrap: wrap; gap: 10px; margin-bottom: 20px; }}
                .nav a {{ background-color: #007bff; color: white; padding: 10px 15px; text-decoration: none; border-radius: 5px; }}
                .nav a:hover {{ background-color: #0056b3; }}
                .card {{ background: white; padding: 20px; margin: 10px 0; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
                .add-btn {{ background-color: #0066cc; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; display: inline-block; margin-bottom: 20px; }}
                .add-btn:hover {{ background-color: #0052a3; }}
                .grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; }}
            </style>
        <link rel="stylesheet" href="https://unpkg.com/@algolia/sitesearch@latest/dist/search.min.css" />
    <script src="https://unpkg.com/@algolia/sitesearch@latest/dist/search.min.js"></script>
</head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>📚 We Convene Science Learning Resource Center</h1>
                    <p>Curated educational resources for environmental science learning and research</p>
                </div>

                <div class="nav">
                    <a href="/">Home</a>
                    <a href="/weather">Weather</a>
                    <a href="/plants">Plants</a>
                    
                    <a href="/lakes">Lakes &amp; River</a>
                    <a href="/animals">Animals</a>
                    <a href="/garbage_cans">Garbage Cans</a>
                    <a href="/learning-center">Learning Center</a>
                    
                    <a href="/we-convene-science">We Convene Science</a>
                    <a href="/maps">Maps</a>
                    
                    <a href="/statistics">Statistics</a>
                </div>

                <a href="/add_learning_resource" class="add-btn">Add New Learning Resource</a>

                <div class="grid">
                    {resources_html if resources_html else '<div class="card"><p>No learning resources yet. Add your first resource!</p></div>'}
                </div>
            </div>
        </body>
        </html>
        """
        self.serve_html(html)

    def serve_we_convene_science(self):
        # Fetch live AQI data from AirNow API for Chicago (ZIP 60601)
        airnow_key = os.environ.get("AIRNOW_API_KEY", "")
        aqi_cards_html = ""
        aqi_banner = ""
        if airnow_key:
            try:
                url = (
                    f"https://www.airnowapi.org/aq/observation/zipCode/current/"
                    f"?format=application/json&zipCode=60601&distance=25&API_KEY={airnow_key}"
                )
                with urllib.request.urlopen(url, timeout=5) as resp:
                    data = json.loads(resp.read().decode())
                if data:
                    for obs in data:
                        param = obs.get("ParameterName", "N/A")
                        aqi_val = obs.get("AQI", "N/A")
                        cat = obs.get("Category", {})
                        cat_name = cat.get("Name", "N/A")
                        cat_num = cat.get("Number", 1)
                        color_map = {1:"#00e400",2:"#ffff00",3:"#ff7e00",4:"#ff0000",5:"#8f3f97",6:"#7e0023"}
                        color = color_map.get(cat_num, "#aaa")
                        aqi_cards_html += f"""
                        <div class="aqi-card" style="border-left: 6px solid {color};">
                            <h4>{param}</h4>
                            <div class="aqi-number" style="color:{color};">{aqi_val}</div>
                            <div class="aqi-label">{cat_name}</div>
                        </div>
                        """
                    aqi_banner = f'<p class="aqi-note">Live data for Cook County, IL — updated hourly via AirNow API</p>'
                else:
                    aqi_cards_html = '<p>No current AQI observations returned for this area.</p>'
            except Exception as e:
                aqi_cards_html = f'<p>Could not fetch live AQI data: {str(e)}</p>'
        else:
            aqi_cards_html = """
            <div class="card" style="border-left:4px solid #ffc107;">
                <p><strong>⚠️ AirNow API key not configured.</strong> Add an <code>AIRNOW_API_KEY</code>
                environment variable to display live Cook County air quality data.
                Get a free key at <a href="https://docs.airnowapi.org/" target="_blank">docs.airnowapi.org</a>.</p>
            </div>
            """

        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>We Convene Science - CULAP Data Camp and Education Center</title>
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <style>
                body {{ font-family: Arial, sans-serif; margin: 0; padding: 20px; background-color: #f5f5f5; }}
                .container {{ max-width: 1200px; margin: 0 auto; }}
                .header {{ background: linear-gradient(135deg, #1a6b3c, #0d6efd); color: white; padding: 25px; border-radius: 8px; margin-bottom: 20px; }}
                .section-header {{ padding: 15px 20px; border-radius: 8px; margin: 30px 0 15px 0; color: white; }}
                .sh-green {{ background-color: #1a6b3c; }}
                .sh-blue {{ background-color: #0d6efd; }}
                .sh-orange {{ background-color: #e07b00; }}
                .sh-purple {{ background-color: #6f42c1; }}
                .nav {{ display: flex; flex-wrap: wrap; gap: 10px; margin-bottom: 20px; }}
                .nav a {{ background-color: #007bff; color: white; padding: 10px 15px; text-decoration: none; border-radius: 5px; }}
                .nav a:hover {{ background-color: #0056b3; }}
                .card {{ background: white; padding: 20px; margin: 10px 0; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
                .grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 20px; }}
                .aqi-grid {{ display: flex; flex-wrap: wrap; gap: 15px; margin-bottom: 10px; }}
                .aqi-card {{ background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); min-width: 160px; text-align: center; }}
                .aqi-number {{ font-size: 3em; font-weight: bold; }}
                .aqi-label {{ font-size: 0.9em; color: #555; margin-top: 4px; }}
                .aqi-note {{ font-size: 0.85em; color: #666; margin: 8px 0; }}
                .activity-tag {{ display: inline-block; background: #e8f4e8; color: #1a6b3c; padding: 3px 10px; border-radius: 12px; font-size: 0.85em; margin: 3px 2px; }}
                .lesson-step {{ background: #f8f9fa; border-left: 4px solid #1a6b3c; padding: 12px 15px; margin: 10px 0; border-radius: 0 6px 6px 0; }}
                .lesson-step h5 {{ margin: 0 0 5px 0; color: #1a6b3c; }}
                .materials-list {{ columns: 2; column-gap: 20px; }}
                .materials-list li {{ margin-bottom: 6px; }}
                .discussion-card {{ border-left: 4px solid #0d6efd; }}
                .project-card {{ border-left: 4px solid #6f42c1; }}
                .badge {{ display: inline-block; padding: 3px 10px; border-radius: 12px; font-size: 0.8em; font-weight: bold; margin-left: 8px; }}
                .badge-k5 {{ background: #cfe2ff; color: #0d6efd; }}
                .badge-ngss {{ background: #d1e7dd; color: #0a3622; }}
            </style>
        <link rel="stylesheet" href="https://unpkg.com/@algolia/sitesearch@latest/dist/search.min.css" />
        <script src="https://unpkg.com/@algolia/sitesearch@latest/dist/search.min.js"></script>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🌿 We Convene Science</h1>
                    <p>Outdoor activities, science discussions, lesson plans &amp; research projects for Cook County environmental education</p>
                </div>
                <div class="nav">
                    <a href="/">Home</a>
                    <a href="/weather">Weather</a>
                    <a href="/plants">Plants</a>
                    <a href="/lakes">Lakes &amp; River</a>
                    <a href="/animals">Animals</a>
                    <a href="/garbage_cans">Garbage Cans</a>
                    <a href="/we-convene-science">We Convene Science</a>
                    <a href="/maps">Maps</a>
                    <a href="/statistics">Statistics</a>
                </div>
                <div id="search" style="margin-bottom: 20px;"></div>
                <script>
                  SiteSearch.init({{
                    container: "#search",
                    applicationId: "G1S1VRTBX5",
                    apiKey: "5d5d722782d6b620065a475f91221e18",
                    indexName: "test_schiller_woods_scenariosss",
                    attributes: {{
                      primaryText: "date",
                      secondaryText: undefined,
                      tertiaryText: undefined,
                      url: "",
                      image: undefined
                    }},
                    darkMode: false,
                  }});
                </script>

                <!-- ── LIVE AIR QUALITY ── -->
                <div class="section-header sh-green">
                    <h2>🌬️ Live Air Quality — Cook County, IL</h2>
                    <p>Current AQI readings from the AirNow network</p>
                </div>
                <div class="aqi-grid">{aqi_cards_html}</div>
                {aqi_banner}
                <div class="card">
                    <h4>AQI Activity Guide</h4>
                    <table style="width:100%;border-collapse:collapse;font-size:0.9em;">
                        <tr style="background:#f0f0f0;"><th style="padding:8px;text-align:left;">AQI Range</th><th style="padding:8px;text-align:left;">Category</th><th style="padding:8px;text-align:left;">Outdoor Activity Recommendation</th></tr>
                        <tr><td style="padding:8px;border-bottom:1px solid #eee;"><span style="color:#00e400;font-weight:bold;">0–50</span></td><td style="padding:8px;border-bottom:1px solid #eee;">Good</td><td style="padding:8px;border-bottom:1px solid #eee;">✅ All outdoor activities recommended</td></tr>
                        <tr><td style="padding:8px;border-bottom:1px solid #eee;"><span style="color:#b8b800;font-weight:bold;">51–100</span></td><td style="padding:8px;border-bottom:1px solid #eee;">Moderate</td><td style="padding:8px;border-bottom:1px solid #eee;">✅ Most activities OK; sensitive groups take care</td></tr>
                        <tr><td style="padding:8px;border-bottom:1px solid #eee;"><span style="color:#ff7e00;font-weight:bold;">101–150</span></td><td style="padding:8px;border-bottom:1px solid #eee;">Unhealthy for Sensitive Groups</td><td style="padding:8px;border-bottom:1px solid #eee;">⚠️ Reduce prolonged outdoor exertion</td></tr>
                        <tr><td style="padding:8px;border-bottom:1px solid #eee;"><span style="color:#ff0000;font-weight:bold;">151–200</span></td><td style="padding:8px;border-bottom:1px solid #eee;">Unhealthy</td><td style="padding:8px;border-bottom:1px solid #eee;">⚠️ Move lessons indoors; limit outdoor time</td></tr>
                        <tr><td style="padding:8px;"><span style="color:#7e0023;font-weight:bold;">201+</span></td><td style="padding:8px;">Very Unhealthy / Hazardous</td><td style="padding:8px;">🚫 Cancel all outdoor activities</td></tr>
                    </table>
                </div>

                <!-- ── OUTDOOR ACTIVITIES ── -->
                <div class="section-header sh-green">
                    <h2>🏕️ Outdoor Activities</h2>
                </div>
                <div class="grid">
                    <div class="card">
                        <h4>🌫️ Air Particle Trapping Walk</h4>
                        <p>Students coat petroleum-jelly "wings" (see Bird's Eye View lesson below) and hang them at different outdoor sites — parking lot, tree canopy, ball field — then compare particle buildup after one week.</p>
                        <span class="activity-tag">Grades K–5</span>
                        <span class="activity-tag">Air Quality</span>
                        <span class="activity-tag">Schiller Woods</span>
                    </div>
                    <div class="card">
                        <h4>🌿 Forest Preserve Transect Survey</h4>
                        <p>Walk a measured transect at Schiller Woods or Robinson Homestead. Record plant species, soil cover, and canopy openings every 10 meters using the Plants tab to log findings in real time.</p>
                        <span class="activity-tag">Grades 3–12</span>
                        <span class="activity-tag">Botany</span>
                        <span class="activity-tag">BIOS 399</span>
                    </div>
                    <div class="card">
                        <h4>🐿️ Squirrel Giving-Up Density Observation</h4>
                        <p>Deploy foraging trays with known seed quantities at River Bend and Robinson Homestead. Record the GUD (amount left uneaten) as a proxy for perceived predation risk. Log data via the Animals tab.</p>
                        <span class="activity-tag">Grades 9–12</span>
                        <span class="activity-tag">Behavioral Ecology</span>
                        <span class="activity-tag">BIOS 399</span>
                    </div>
                    <div class="card">
                        <h4>💧 Creel Survey &amp; Shoreline Sweep</h4>
                        <p>Conduct a creel (fishing) survey at a Cook County lake, record fish species, count, and size. Pair with shoreline macro-invertebrate sampling as a water quality indicator.</p>
                        <span class="activity-tag">Grades 5–12</span>
                        <span class="activity-tag">Aquatic Biology</span>
                        <span class="activity-tag">Cook County</span>
                    </div>
                    <div class="card">
                        <h4>🗑️ Urban Ant Colony Census</h4>
                        <p>Survey garbage can stations for ant species diversity. Count colonies, estimate forager density, and record distance to nearest impervious surface as a urbanization proxy.</p>
                        <span class="activity-tag">Grades 4–12</span>
                        <span class="activity-tag">Entomology</span>
                        <span class="activity-tag">Urban Ecology</span>
                    </div>
                    <div class="card">
                        <h4>🌦️ Microclimate Mapping</h4>
                        <p>Use thermometers and weather instruments to compare temperature, humidity, and wind at forest interior vs. edge vs. parking lot. Discuss urban heat island effects using Weather tab data.</p>
                        <span class="activity-tag">Grades 3–12</span>
                        <span class="activity-tag">Meteorology</span>
                        <span class="activity-tag">Urban Heat</span>
                    </div>
                </div>

                <!-- ── DISCUSSIONS ── -->
                <div class="section-header sh-blue">
                    <h2>💬 Science Discussions</h2>
                </div>
                <div class="grid">
                    <div class="card discussion-card">
                        <h4>Why does road salt make squirrels take risks?</h4>
                        <p>Squirrels need sodium but face predation risk near roads. Discuss how the "ecology of fear" shapes animal behavior near urban stressors like River Road at Schiller Woods. What would the squirrels trade off?</p>
                        <span class="activity-tag">Behavioral Ecology</span>
                    </div>
                    <div class="card discussion-card">
                        <h4>Is the Chicago River healthy?</h4>
                        <p>Use river observation data from this app to discuss water quality indicators: clarity, temperature, and wildlife present. Compare with historical data on the reversal of the Chicago River. What species would indicate recovery?</p>
                        <span class="activity-tag">Water Quality</span>
                    </div>
                    <div class="card discussion-card">
                        <h4>What does "good" air actually mean?</h4>
                        <p>Look at today's AQI values above. Discuss PM2.5 vs. Ozone. Why do the smallest particles pose the greatest health risk? How does living near O'Hare flight paths affect air quality readings?</p>
                        <span class="activity-tag">Air Quality</span>
                        <span class="activity-tag">Public Health</span>
                    </div>
                    <div class="card discussion-card">
                        <h4>Forest preserve or parking lot — what difference does it make?</h4>
                        <p>Compare microclimate, noise level, species diversity, and air quality between a forested site and an urban site. What ecosystem services does the forest preserve provide that the parking lot does not?</p>
                        <span class="activity-tag">Ecosystem Services</span>
                    </div>
                </div>

                <!-- ── LESSON PLAN: BIRD'S EYE VIEW ── -->
                <div class="section-header sh-orange">
                    <h2>📋 Lesson Plan: Bird's Eye View</h2>
                    <p>
                        <span class="badge badge-k5">Grades K–5</span>
                        <span class="badge badge-ngss">NGSS ESS3.C</span>
                        &nbsp;Subject: Science &nbsp;|&nbsp; Time: 2 Class Periods (1 Week Apart)
                    </p>
                </div>
                <div class="card">
                    <h4>🎯 Student Objectives</h4>
                    <ul>
                        <li>Name examples of natural and man-made air pollution</li>
                        <li>Describe some ways that people pollute the air</li>
                        <li>Observe and compare air samples collected outdoors</li>
                        <li>Explain how air pollution may affect us in daily life</li>
                    </ul>
                </div>
                <div class="card">
                    <h4>🧰 Materials</h4>
                    <ul class="materials-list">
                        <li>Wire coat-hangers</li>
                        <li>Stockings (tan or white)</li>
                        <li>Scissors &amp; Stapler</li>
                        <li>Petroleum jelly</li>
                        <li>Cotton swabs</li>
                        <li>Magnifying glass</li>
                        <li>Tape or rubber bands</li>
                        <li>Butcher paper</li>
                    </ul>
                </div>
                <div class="card">
                    <h4>📖 Background</h4>
                    <p>People pollute the air in many ways — burning fuel in factories, power plants, cars, and trucks — but also simply by moving around. Particles stirred up by foot traffic or vehicle travel can include bacteria, pollen, animal dander, and microscopic organisms. The extremely small size of these particles makes them a respiratory risk because they can be inhaled deep into the lungs. Conditions from sore throats to asthma have been linked to air pollution. Plants also need clean air, sunlight, and water; foreign substances in the air can hinder their ability to take in essential nutrients.</p>
                </div>
                <div class="card">
                    <h4>🔨 Activity Steps — Building the Birds</h4>
                    <div class="lesson-step"><h5>Step 1</h5><p>Have students cut out the bird parts. Teachers may prepare coat-hangers ahead of time for younger grades.</p></div>
                    <div class="lesson-step"><h5>Step 2</h5><p>Ask each student to write their name on the back of the tail feathers.</p></div>
                    <div class="lesson-step"><h5>Step 3</h5><p>Students color the head and tail feathers. <strong>Do NOT color the wings</strong> — the wings must remain unstained to show particles clearly.</p></div>
                    <div class="lesson-step"><h5>Step 4</h5><p>Grasp a wire hanger by the handle. Pull and stretch the center bottom into a diamond shape.</p></div>
                    <div class="lesson-step"><h5>Step 5</h5><p>Pull the knee-high stocking onto the pointed diamond part and pull toward the handle until snug. Secure with staples, tape, or rubber bands.</p></div>
                    <div class="lesson-step"><h5>Step 6</h5><p>Staple the head, wings, and tail feathers to the bird frame.</p></div>
                    <div class="lesson-step"><h5>Step 7</h5><p>Using a cotton swab, spread a small amount of petroleum jelly on the wings only. <em>Wings only!</em></p></div>
                </div>
                <div class="card">
                    <h4>📍 Hanging &amp; Collecting the Birds</h4>
                    <div class="lesson-step"><h5>Hanging</h5><p>Hang birds at varied indoor and outdoor locations: playground, trees, breezeway, parking lot, school bus area, cafeteria, ball field. For Cook County research, use Schiller Woods sites. Make a chart of all locations. Collect birds before rain; return them after.</p></div>
                    <div class="lesson-step"><h5>After One Week</h5><p>Have students predict and chart which birds will be dirtiest. Collect and lay them on butcher paper.</p></div>
                    <div class="lesson-step"><h5>Comparison</h5><p>Students visually identify the most and least polluted birds. Use magnifying glasses to examine wings. Stress that the smallest particles are the most dangerous — and that particles invisible to the naked eye are still present. Discuss how dirty birds parallel dirty lungs, and what protective actions people can take.</p></div>
                </div>
                <div class="card">
                    <h4>💡 Discussion Prompts for This Lesson</h4>
                    <ul>
                        <li>Which locations produced the dirtiest birds? Why?</li>
                        <li>If the wings are "dirty," what does that tell us about our lungs?</li>
                        <li>What can we do to protect our lungs? (Examples: avoid burning trash/leaves, wear masks near sawdust, walk instead of drive, avoid playing near busy roads)</li>
                        <li>How do Cook County AQI readings above connect to what the birds collected?</li>
                    </ul>
                    <p><em>Adapted from the Air and Waste Management Association Environmental Resource Guide for Air Quality — EPA-456/F-24-006</em></p>
                </div>

                <!-- ── PROJECTS ── -->
                <div class="section-header sh-purple">
                    <h2>🔬 Research Projects</h2>
                </div>
                <div class="grid">
                    <div class="card project-card">
                        <h4>Project 1: GUD Curve Analysis</h4>
                        <p><strong>Question:</strong> Does proximity to River Road increase squirrel foraging risk-tolerance at Schiller Woods?</p>
                        <p><strong>Method:</strong> Deploy sodium-spiked seed trays at River Bend (Experimental) and Robinson Homestead (Control). Calculate Giving-Up Density (GUD) and Sodium Multiplier λ. Use the Animals tab to log observations.</p>
                        <span class="activity-tag">BIOS 399</span>
                        <span class="activity-tag">Behavioral Ecology</span>
                    </div>
                    <div class="card project-card">
                        <h4>Project 2: Particulate Deposition Mapping</h4>
                        <p><strong>Question:</strong> How does distance from O'Hare flight paths affect PM deposition across Cook County forest preserve sites?</p>
                        <p><strong>Method:</strong> Use the Bird's Eye View protocol at 5+ sites varying in distance from flight paths. Photograph wings and use ImageJ to quantify particle density.</p>
                        <span class="activity-tag">Air Quality</span>
                        <span class="activity-tag">Grades 6–12</span>
                    </div>
                    <div class="card project-card">
                        <h4>Project 3: Creel Survey &amp; Habitat Index</h4>
                        <p><strong>Question:</strong> Which Cook County lakes support the highest fish species diversity, and what habitat features predict that diversity?</p>
                        <p><strong>Method:</strong> Conduct standardized creel surveys at 3+ lakes. Record fish species, count, water clarity, and proximity to impervious surface. Log in Lakes &amp; River tab.</p>
                        <span class="activity-tag">Aquatic Biology</span>
                        <span class="activity-tag">Grades 7–12</span>
                    </div>
                    <div class="card project-card">
                        <h4>Project 4: Urban Ant Diversity Gradient</h4>
                        <p><strong>Question:</strong> Does ant species richness decrease with increasing urban intensity around garbage can stations?</p>
                        <p><strong>Method:</strong> Survey 10+ garbage can stations across a rural-to-urban gradient. Record species, colony size, and distance to nearest road. Log in Garbage Cans tab.</p>
                        <span class="activity-tag">Entomology</span>
                        <span class="activity-tag">Urban Ecology</span>
                    </div>
                </div>
            </div>
        </body>
        </html>
        """
        self.serve_html(html)

    def serve_learning_resource_form(self):
        html = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Add Learning Resource - Learning Center</title>
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <style>
                body { font-family: Arial, sans-serif; margin: 0; padding: 20px; background-color: #f5f5f5; }
                .container { max-width: 800px; margin: 0 auto; }
                .header { background-color: #0066cc; color: white; padding: 20px; border-radius: 8px; margin-bottom: 20px; }
                .nav { display: flex; flex-wrap: wrap; gap: 10px; margin-bottom: 20px; }
                .nav a { background-color: #007bff; color: white; padding: 10px 15px; text-decoration: none; border-radius: 5px; }
                .nav a:hover { background-color: #0056b3; }
                .card { background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
                .form-group { margin-bottom: 15px; }
                label { display: block; margin-bottom: 5px; font-weight: bold; }
                input, select, textarea { width: 100%; padding: 8px; border: 1px solid #ddd; border-radius: 4px; box-sizing: border-box; }
                textarea { height: 100px; resize: vertical; }
                button { background-color: #0066cc; color: white; padding: 12px 30px; border: none; border-radius: 5px; cursor: pointer; font-size: 16px; }
                button:hover { background-color: #0052a3; }
                .back-btn { background-color: #6c757d; color: white; padding: 8px 15px; text-decoration: none; border-radius: 5px; display: inline-block; margin-bottom: 20px; }
                .back-btn:hover { background-color: #5a6268; }
            </style>
        <link rel="stylesheet" href="https://unpkg.com/@algolia/sitesearch@latest/dist/search.min.css" />
    <script src="https://unpkg.com/@algolia/sitesearch@latest/dist/search.min.js"></script>
</head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>📚 Add Learning Resource</h1>
                </div>

                <div class="nav">
                    <a href="/">Home</a>
                    <a href="/learning-center">Learning Center</a>
                    <a href="/statistics">Statistics</a>
                </div>

                <a href="/learning-center" class="back-btn">← Back to Learning Center</a>

                <div class="card">
                    <form method="POST" action="/add_learning_resource">
                        <div class="form-group">
                            <label for="date">Date Added:</label>
                            <input type="date" id="date" name="date" required>
                        </div>

                        <div class="form-group">
                            <label for="title">Resource Title:</label>
                            <input type="text" id="title" name="title" placeholder="e.g., Environmental Science Basics" required>
                        </div>

                        <div class="form-group">
                            <label for="category">Category:</label>
                            <select id="category" name="category" required>
                                <option value="">Select category</option>
                                <option value="Article">Article</option>
                                <option value="Video">Video</option>
                                <option value="Dataset">Dataset</option>
                                <option value="Course">Course</option>
                                <option value="Research Paper">Research Paper</option>
                                <option value="Tool">Tool</option>
                                <option value="Other">Other</option>
                            </select>
                        </div>

                        <div class="form-group">
                            <label for="description">Description:</label>
                            <textarea id="description" name="description" placeholder="Brief description of the resource and its relevance" required></textarea>
                        </div>

                        <div class="form-group">
                            <label for="url">URL/Link:</label>
                            <input type="url" id="url" name="url" placeholder="https://example.com" required>
                        </div>

                        <div class="form-group">
                            <label for="notes">Notes (optional):</label>
                            <textarea id="notes" name="notes" placeholder="Additional observations or recommendations"></textarea>
                        </div>

                        <button type="submit">Add Learning Resource</button>
                    </form>
                </div>
            </div>
        </body>
        </html>
        """
        self.serve_html(html)

    def format_recent_entries(self, entries):
        if not entries:
            return "<p>No entries yet. Start by adding your first observation!</p>"

        html = ""
        for entry in entries:
            title = entry.get('title', 'Observation')
            date = entry.get('date', 'No date')
            entry_type = entry.get('type', 'unknown').title()
            notes = entry.get('notes', '')
            if notes and len(notes) > 100:
                notes = notes[:100] + "..."

            html += f"""
            <div style="border: 1px solid #ddd; padding: 10px; margin: 5px 0; border-radius: 5px;">
                <strong>{title}</strong> <span style="color: #666;">({entry_type})</span><br>
                <small style="color: #666;">{date}</small>
                {f"<p style='margin: 5px 0;'>{notes}</p>" if notes else ""}
            </div>
            """
        return html


if __name__ == '__main__':
    PORT = 5000
    # Add error handling for port in use
    try:
        socketserver.TCPServer.allow_reuse_address = True
        with socketserver.TCPServer(("0.0.0.0", PORT), EnvironmentalObservationHandler) as httpd:
            print(f"🌿 CULAP Data Camp and Education Center server running at http://0.0.0.0:{PORT}")
            print("Press Ctrl+C to stop the server")
            try:
                httpd.serve_forever()
            except KeyboardInterrupt:
                print("\nServer stopped.")
    except OSError as e:
        if e.errno == 98:
            print(f"Error: Port {PORT} is already in use. Please kill the process using it.")
            import sys
            sys.exit(1)
        else:
            raise e