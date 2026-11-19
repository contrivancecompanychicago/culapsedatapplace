# CULAP Data Camp and Education Center

A community and education-focused environmental observation app for recording weather, plants, wildlife, river and lake conditions, garbage-can/ant observations, and learning resources in Cook County, Illinois. The project also includes a Caldwell Preserves weekly wildlife survey workflow for analyzing Google Forms responses in Google Colab.

## Project status

- **Python project name:** `culapsedatapplace`
- **Version:** `0.0.0`
- **Python:** `>=3.11,<3.12`
- **License:** Apache-2.0
- The package metadata is in [`CULAPS-Data-Camp-and-Education-Center/pyproject.toml`](CULAPS-Data-Camp-and-Education-Center/pyproject.toml).

## What's included

- **Observation web app:** `CULAPS-Data-Camp-and-Education-Center/main.py` runs a Python `http.server` application. It renders pages and handles routes for weather, plants, animals, lakes/rivers, learning resources, maps, statistics, and the GUD/Sodium Trap study.
- **SQLite storage:** `database.py` defines tables and `DatabaseManager` operations for environmental observations, including GUD records.
- **Caldwell survey Colab notebook:** [`Caldwell_Preserves_Weekly_Wildlife_Colab.ipynb`](CULAPS-Data-Camp-and-Education-Center/attached_assets/Caldwell_Preserves_Weekly_Wildlife_Colab.ipynb) reads the linked survey response spreadsheet, inspects headers and missing data, provides exploratory summaries, and exports a CSV with sensitive columns excluded by default.
- **Research/education materials:** notebooks, PDFs, JSON/CSV data, and HTML templates are under `CULAPS-Data-Camp-and-Education-Center/attached_assets/`, `templates/`, and the application directory.

## Caldwell Preserves survey and Google Colab

The weekly survey is intended to collect one response per observation station visit. It captures station and visit details, weather and soundscape, air quality, human activity, species observations, focal-animal behavior, habitat, water chemistry, photographs, and notes.

1. Collect responses with the Google Form and link its responses to the Google Sheet. The app does not submit answers to the Google Form; the notebook reads the response spreadsheet.
2. Open the [Caldwell survey notebook in Colab](https://colab.research.google.com/github/contrivancecompanychicago/culapsedatapplace/blob/main/CULAPS-Data-Camp-and-Education-Center/attached_assets/Caldwell_Preserves_Weekly_Wildlife_Colab.ipynb).
3. Sign in with a Google account that has at least Viewer access to the response spreadsheet. Run the notebook cells and authorize Google access when prompted.
4. The notebook uses the configured spreadsheet ID `1ZqHQrlQWlGlUuywvK58DdK7PyVaBtmNFtFuehj13NeY` and selects the first worksheet by default. Set `WORKSHEET_NAME` in the notebook if the form responses are on a different tab.
5. Review the detected column names and data before analysis. The notebook creates `caldwell_preserves_wildlife_observations.csv`; use the optional Colab download cell to download it.

The notebook authenticates through Colab and Google Sheets API, rather than making the sheet public or embedding credentials. Keep access to the spreadsheet and exports limited to authorized collaborators. Email, observer name, GPS coordinates, and photo-related columns are excluded from the notebook's default CSV export; inspect the headers and sharing settings before sharing any output.

## Run the observation web app

From the repository root:

```bash
cd CULAPS-Data-Camp-and-Education-Center
poetry install
poetry run python main.py
```

The server listens on port `5000`; open `http://localhost:5000`. The app creates/uses `environmental_observations.db` in its working directory.

### Optional integrations

- `AI_INTEGRATIONS_OPENAI_BASE_URL` and `AI_INTEGRATIONS_OPENAI_API_KEY` configure the OpenAI-compatible Replit integration used by the squirrel model.
- `AIRNOW_API_KEY` enables live AirNow data on the We Convene Science page.

Do not commit real API credentials. Configure them as environment secrets in the runtime environment.

## Development notes

- Dependency and package metadata are maintained in `CULAPS-Data-Camp-and-Education-Center/pyproject.toml`; Poetry lock data is in `poetry.lock` in the same directory.
- Although Flask is listed as a dependency, the current server entry point uses Python's built-in `http.server`.
- Most web page HTML is rendered inline in `main.py`; `templates/` also contains standalone HTML files.
- The Google Colab workflow is for reading and analyzing submitted Google Form responses. It is separate from the SQLite-backed observation web app.

## Author and license

Authored by Eric Hilary Smith (<erichilarysmithsr@gmail.com>). Distributed under the [Apache License 2.0](LICENSE).
