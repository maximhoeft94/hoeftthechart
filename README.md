# Shot Chart Generator — Web App

## Run Locally

```bash
# Install dependencies
pip install flask requests pandas gunicorn

# Run
python app.py

# Open browser
http://localhost:5000
```

## Deploy to Render (free, public URL)

1. Create a GitHub account at github.com
2. Create a new repository called `shotchart`
3. Upload all files in this folder to the repo
4. Go to render.com and sign up (free)
5. Click "New Web Service"
6. Connect your GitHub repo
7. Set these settings:
   - Build Command: `pip install -r requirements.txt`
   - Start Command:  `gunicorn app:app`
8. Click "Deploy" — done!

Render gives you a public URL like: https://shotchart.onrender.com

## File Structure
```
shotchart_web/
├── app.py              ← Flask backend (all logic)
├── requirements.txt    ← Python dependencies
├── Procfile            ← Render/Heroku start command
├── README.md
└── templates/
    └── index.html      ← Frontend UI
```

## How It Works
1. User types a team name → app searches team lookup table
2. User selects a game → app scans ESPN scoreboard day by day
3. User selects a player → app fetches ESPN game summary
4. App generates SVG shot chart and displays it in the browser
5. User can download the SVG
