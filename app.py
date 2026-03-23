"""
Shot Chart Web App
==================
Flask backend that serves the shot chart generator as a web app.

INSTALL:
  pip install flask requests pandas gunicorn

RUN LOCALLY:
  python app.py
  Open http://localhost:5000

DEPLOY TO RENDER:
  - Push to GitHub
  - Create new Web Service on Render
  - Build command: pip install -r requirements.txt
  - Start command: gunicorn app:app
"""

from flask import Flask, render_template, request, jsonify
import os
import json
import requests
import pandas as pd
from datetime import datetime, timedelta

app = Flask(__name__)

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
}

# ─────────────────────────────────────────────────────────────────────────────
# TEAM LOOKUP
# ─────────────────────────────────────────────────────────────────────────────

TEAM_LOOKUP = {
    'byu': (252, 'BYU Cougars'), 'brigham young': (252, 'BYU Cougars'),
    'houston': (248, 'Houston Cougars'),
    'kansas': (2305, 'Kansas Jayhawks'), 'ku': (2305, 'Kansas Jayhawks'),
    'kansas state': (2306, 'Kansas State Wildcats'), 'k-state': (2306, 'Kansas State Wildcats'),
    'iowa state': (66, 'Iowa State Cyclones'),
    'tcu': (2628, 'TCU Horned Frogs'),
    'texas tech': (2641, 'Texas Tech Red Raiders'),
    'baylor': (239, 'Baylor Bears'),
    'west virginia': (277, 'West Virginia Mountaineers'), 'wvu': (277, 'West Virginia Mountaineers'),
    'oklahoma state': (197, 'Oklahoma State Cowboys'),
    'ucf': (2116, 'UCF Knights'),
    'cincinnati': (2132, 'Cincinnati Bearcats'),
    'colorado': (38, 'Colorado Buffaloes'),
    'arizona state': (9, 'Arizona State Sun Devils'), 'asu': (9, 'Arizona State Sun Devils'),
    'arizona': (12, 'Arizona Wildcats'),
    'utah': (254, 'Utah Utes'),
    'duke': (150, 'Duke Blue Devils'),
    'north carolina': (153, 'North Carolina Tar Heels'), 'unc': (153, 'North Carolina Tar Heels'),
    'nc state': (152, 'NC State Wolfpack'),
    'virginia': (258, 'Virginia Cavaliers'), 'uva': (258, 'Virginia Cavaliers'),
    'virginia tech': (259, 'Virginia Tech Hokies'),
    'clemson': (228, 'Clemson Tigers'),
    'florida state': (52, 'Florida State Seminoles'), 'fsu': (52, 'Florida State Seminoles'),
    'miami': (2390, 'Miami Hurricanes'),
    'georgia tech': (59, 'Georgia Tech Yellow Jackets'),
    'wake forest': (154, 'Wake Forest Demon Deacons'),
    'pittsburgh': (221, 'Pittsburgh Panthers'), 'pitt': (221, 'Pittsburgh Panthers'),
    'syracuse': (183, 'Syracuse Orange'),
    'notre dame': (87, 'Notre Dame Fighting Irish'),
    'boston college': (103, 'Boston College Eagles'),
    'louisville': (97, 'Louisville Cardinals'),
    'cal': (25, 'California Golden Bears'), 'california': (25, 'California Golden Bears'),
    'stanford': (24, 'Stanford Cardinal'),
    'smu': (2567, 'SMU Mustangs'),
    'kentucky': (96, 'Kentucky Wildcats'), 'uk': (96, 'Kentucky Wildcats'),
    'tennessee': (2633, 'Tennessee Volunteers'),
    'auburn': (2, 'Auburn Tigers'),
    'alabama': (333, 'Alabama Crimson Tide'),
    'florida': (57, 'Florida Gators'),
    'georgia': (61, 'Georgia Bulldogs'),
    'lsu': (99, 'LSU Tigers'),
    'mississippi state': (344, 'Mississippi State Bulldogs'),
    'ole miss': (145, 'Ole Miss Rebels'),
    'arkansas': (8, 'Arkansas Razorbacks'),
    'texas a&m': (245, 'Texas A&M Aggies'),
    'south carolina': (2579, 'South Carolina Gamecocks'),
    'vanderbilt': (238, 'Vanderbilt Commodores'),
    'missouri': (142, 'Missouri Tigers'),
    'oklahoma': (201, 'Oklahoma Sooners'),
    'texas': (2641, 'Texas Longhorns'),
    'michigan': (130, 'Michigan Wolverines'),
    'michigan state': (127, 'Michigan State Spartans'), 'msu': (127, 'Michigan State Spartans'),
    'ohio state': (194, 'Ohio State Buckeyes'),
    'indiana': (84, 'Indiana Hoosiers'),
    'illinois': (356, 'Illinois Fighting Illini'),
    'purdue': (2509, 'Purdue Boilermakers'),
    'iowa': (2294, 'Iowa Hawkeyes'),
    'wisconsin': (275, 'Wisconsin Badgers'),
    'minnesota': (135, 'Minnesota Golden Gophers'),
    'nebraska': (158, 'Nebraska Cornhuskers'),
    'penn state': (213, 'Penn State Nittany Lions'),
    'maryland': (120, 'Maryland Terrapins'),
    'rutgers': (164, 'Rutgers Scarlet Knights'),
    'northwestern': (77, 'Northwestern Wildcats'),
    'oregon': (2483, 'Oregon Ducks'),
    'washington': (264, 'Washington Huskies'),
    'usc': (30, 'USC Trojans'),
    'ucla': (26, 'UCLA Bruins'),
    'gonzaga': (2250, 'Gonzaga Bulldogs'),
    'memphis': (235, 'Memphis Tigers'),
    'connecticut': (41, 'UConn Huskies'), 'uconn': (41, 'UConn Huskies'),
    'creighton': (156, 'Creighton Bluejays'),
    'marquette': (269, 'Marquette Golden Eagles'),
    'xavier': (2752, 'Xavier Musketeers'),
    'villanova': (222, 'Villanova Wildcats'),
    'st. johns': (2599, "St. John's Red Storm"), 'st johns': (2599, "St. John's Red Storm"),
    'providence': (2507, 'Providence Friars'),
    'seton hall': (2550, 'Seton Hall Pirates'),
    'butler': (2086, 'Butler Bulldogs'),
    'dayton': (2196, 'Dayton Flyers'),
    'san diego state': (21, 'San Diego State Aztecs'), 'sdsu': (21, 'San Diego State Aztecs'),
    'utah state': (328, 'Utah State Aggies'),
    'boise state': (68, 'Boise State Broncos'),
    'nevada': (2440, 'Nevada Wolf Pack'),
    'unlv': (2439, 'UNLV Rebels'),
    'colorado state': (36, 'Colorado State Rams'),
    'vcu': (2670, 'VCU Rams'),
    'davidson': (2168, 'Davidson Wildcats'),
    'wichita state': (2724, 'Wichita State Shockers'),
    'drake': (2181, 'Drake Bulldogs'),
    'murray state': (93, 'Murray State Racers'),
    'belmont': (2057, 'Belmont Bruins'),
    'liberty': (2335, 'Liberty Flames'),
    'vermont': (261, 'Vermont Catamounts'),
    'colgate': (2142, 'Colgate Raiders'),
    'oral roberts': (2393, 'Oral Roberts Golden Eagles'),
    'iona': (2363, 'Iona Gaels'),
    'furman': (231, 'Furman Paladins'),
    'george mason': (2244, 'George Mason Patriots'),
    'western kentucky': (98, 'Western Kentucky Hilltoppers'),
    'florida atlantic': (2226, 'Florida Atlantic Owls'), 'fau': (2226, 'Florida Atlantic Owls'),
    'charlotte': (2429, 'Charlotte 49ers'),
    'north texas': (249, 'North Texas Mean Green'),
    'app state': (2026, 'Appalachian State Mountaineers'),
    'james madison': (256, 'James Madison Dukes'), 'jmu': (256, 'James Madison Dukes'),
    'howard': (2309, 'Howard Bison'),
}

# ─────────────────────────────────────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────────────────────────────────────

def fuzzy_score(a, b):
    a, b = a.lower(), b.lower()
    if a == b: return 1.0
    if a in b or b in a: return 0.9
    matches = sum(1 for c in a if c in b)
    return matches / max(len(a), len(b))


def find_team_id(team_name):
    search = team_name.strip().lower()
    entries = [([key], str(tid), display) for key, (tid, display) in TEAM_LOOKUP.items()]

    for keys, tid, display in entries:
        if search in keys or search == display.lower():
            return int(tid), display
    for keys, tid, display in entries:
        if any(search in k or k in search for k in keys) or search in display.lower():
            return int(tid), display

    scored = []
    for keys, tid, display in entries:
        score = max(fuzzy_score(search, k) for k in keys)
        score = max(score, fuzzy_score(search, display.lower()))
        scored.append((score, tid, display))
    scored.sort(key=lambda x: x[0], reverse=True)
    top = [(int(tid), display) for score, tid, display in scored if score >= 0.4][:5]
    if top:
        return top[0]  # return best fuzzy match

    return None, None


def get_all_teams():
    seen = set()
    teams = []
    for key, (tid, display) in TEAM_LOOKUP.items():
        if display not in seen:
            seen.add(display)
            teams.append({'id': tid, 'name': display})
    return sorted(teams, key=lambda x: x['name'])


def fetch_schedule(team_id):
    all_games = []
    seen_ids  = set()
    start     = datetime(2025, 11, 1)
    end       = datetime(2026, 4, 7)
    current   = start

    while current <= end:
        date_param = current.strftime('%Y%m%d')
        try:
            resp = requests.get(
                "https://site.web.api.espn.com/apis/site/v2/sports/basketball/mens-college-basketball/scoreboard",
                headers=HEADERS,
                params={'dates': date_param, 'limit': 300, 'groups': 50},
                timeout=8
            )
            if resp.status_code == 200:
                for event in resp.json().get('events', []):
                    comps      = event.get('competitions', [{}])[0]
                    comp_teams = comps.get('competitors', [])
                    team_ids   = [str(c.get('team', {}).get('id', '')) for c in comp_teams]
                    if str(team_id) not in team_ids:
                        continue
                    eid   = event.get('id', '')
                    ename = event.get('name', '')
                    edate = event.get('date', '')[:10]
                    if not eid or eid in seen_ids:
                        continue
                    try:
                        dt = datetime.strptime(edate, '%Y-%m-%d')
                    except:
                        continue
                    opp_name  = ''
                    home_away = 'vs'
                    score_str = ''
                    opp_score = ''
                    winner    = None
                    for c in comp_teams:
                        cid = str(c.get('team', {}).get('id', ''))
                        if cid == str(team_id):
                            home_away = 'vs' if c.get('homeAway') == 'home' else '@'
                            score_str = str(c.get('score', ''))
                            winner    = c.get('winner')
                        else:
                            opp_name  = c.get('team', {}).get('displayName', '')
                            opp_score = str(c.get('score', ''))
                    status = comps.get('status', {}).get('type', {}).get('description', '')
                    result = ''
                    if status == 'Final' and score_str and opp_score:
                        result = ('W' if winner else 'L') + ' ' + score_str + '-' + opp_score
                    all_games.append({
                        'id':       eid,
                        'date':     dt.strftime('%m/%d/%Y'),
                        'name':     ename,
                        'opponent': opp_name,
                        'homeAway': home_away,
                        'result':   result,
                        'status':   status,
                    })
                    seen_ids.add(eid)
        except:
            pass
        current += timedelta(days=1)

    return sorted(all_games, key=lambda x: x['date'])


def pull_game_data(game_id, primary_team_name):
    url  = "https://site.web.api.espn.com/apis/site/v2/sports/basketball/mens-college-basketball/summary?event=" + str(game_id)
    resp = requests.get(url, headers=HEADERS, timeout=15)
    resp.raise_for_status()
    data = resp.json()

    header      = data['header']['competitions'][0]
    competitors = header['competitors']
    game_date   = header['date'][:10]
    date_fmt    = pd.to_datetime(game_date).strftime('%-m/%-d/%Y')
    search      = primary_team_name.strip().lower()

    def team_matches(comp, s):
        t = comp['team']
        return any(s in t.get(f, '').lower() for f in ['displayName','abbreviation','location','shortDisplayName'])

    primary_comp = next((c for c in competitors if team_matches(c, search)), competitors[0])
    opp_comp     = next((c for c in competitors if not team_matches(c, search)), competitors[1])
    primary_name = primary_comp['team']['location']
    opp_name     = opp_comp['team']['location']

    rows = []
    for team_block in data['boxscore']['players']:
        is_primary  = team_matches({'team': team_block['team']}, search)
        stats_block = team_block['statistics'][0]
        keys        = stats_block['keys']
        for athlete in stats_block['athletes']:
            if athlete.get('didNotPlay'):
                continue
            s   = athlete['stats']
            row = {
                'is_primary': is_primary,
                'name':       athlete['athlete']['displayName'],
                'athlete_id': str(athlete['athlete'].get('id', '')),
                'starter':    athlete.get('starter', False),
            }
            for i, key in enumerate(keys):
                row[key] = s[i] if i < len(s) else None
            rows.append(row)
    boxscore = pd.DataFrame(rows)

    shots_list = []
    for play in data.get('plays', []):
        if not play.get('shootingPlay'):
            continue
        if 'free throw' in play.get('text', '').lower():
            continue
        raw_x = play.get('coordinate', {}).get('x')
        raw_y = play.get('coordinate', {}).get('y')
        if raw_x is None or raw_y is None:
            continue
        participants = play.get('participants', [])
        athlete_id   = str(participants[0].get('athlete', {}).get('id', '')) if participants else ''
        shots_list.append({
            'player':     play.get('text', '').split(' makes')[0].split(' misses')[0].strip(),
            'athlete_id': athlete_id,
            'is_primary': None,
            'made':       play.get('scoringPlay', False),
            'shot_x':     (25 - raw_x) * 10,
            'shot_y':     raw_y * 10,
        })

    shots = pd.DataFrame(shots_list)
    if not shots.empty:
        id_map = {str(r['athlete_id']): (r['name'], r['is_primary'])
                  for _, r in boxscore.iterrows() if r['athlete_id'] and str(r['athlete_id']) != 'nan'}
        def resolve(r):
            aid = r.get('athlete_id', '')
            if aid and aid in id_map:
                return pd.Series({'player': id_map[aid][0], 'is_primary': id_map[aid][1]})
            return pd.Series({'player': r['player'], 'is_primary': None})
        resolved       = shots.apply(resolve, axis=1)
        shots['player']     = resolved['player']
        shots['is_primary'] = resolved['is_primary']

    return shots, date_fmt, primary_name, opp_name, boxscore


def classify_shot(loc_x, loc_y):
    corner_3 = (loc_y < 90) and (abs(loc_x) >= 191)
    arc_3    = (loc_y / 267)**2 + (loc_x / 194)**2 > 1
    if corner_3 or arc_3:
        if loc_y < 90 and loc_x >= 0:  return 'right_corner_3'
        elif loc_y < 90 and loc_x < 0: return 'left_corner_3'
        elif loc_x > 69:               return 'right_wing_3'
        elif loc_x < -69:              return 'left_wing_3'
        else:                          return 'top_of_key_3'
    else:
        if abs(loc_x) < 69 and loc_y < 163:  return 'paint'
        elif abs(loc_x) < 69:                 return 'mid_range_top'
        elif loc_x > 0 and loc_y >= 129:      return 'right_elbow'
        elif loc_x < 0 and loc_y >= 129:      return 'left_elbow'
        elif loc_x > 0:                       return 'mid_range_right'
        else:                                 return 'mid_range_left'


ALL_ZONES   = ['paint','mid_range_top','mid_range_right','mid_range_left',
               'right_elbow','left_elbow','right_corner_3','left_corner_3',
               'right_wing_3','left_wing_3','top_of_key_3']

def tally_zones(shots, player_name):
    result = {z: {'fga': 0, 'fgm': 0} for z in ALL_ZONES}
    if shots.empty or 'zone' not in shots.columns:
        return result
    df = shots[shots['player'].str.lower() == player_name.lower()]
    if df.empty:
        parts = player_name.lower().split()
        df = shots[shots['player'].str.lower().apply(lambda n: all(p in n for p in parts))]
    for _, row in df.iterrows():
        z = row['zone']
        if z in result:
            result[z]['fga'] += 1
            result[z]['fgm'] += int(row['made'])
    return result


def tally_from_boxscore(boxscore, player_name):
    df = boxscore[boxscore['name'].str.lower() == player_name.lower()]
    if df.empty:
        parts = player_name.lower().split()
        df = boxscore[boxscore['name'].str.lower().apply(lambda n: all(p in n for p in parts))]
    if df.empty:
        return {'fga': 0, 'fgm': 0, 'fga2': 0, 'fgm2': 0, 'fga3': 0, 'fgm3': 0}
    FG  = 'fieldGoalsMade-fieldGoalsAttempted'
    TPT = 'threePointFieldGoalsMade-threePointFieldGoalsAttempted'
    def made(val):
        try: return int(str(val).split('-')[0])
        except: return 0
    def att(val):
        try:
            p = str(val).split('-')
            return int(p[1]) if len(p) > 1 else 0
        except: return 0
    fgm  = sum(made(v) for v in df[FG].tolist())
    fga  = sum(att(v)  for v in df[FG].tolist())
    fgm3 = sum(made(v) for v in df[TPT].tolist())
    fga3 = sum(att(v)  for v in df[TPT].tolist())
    return {'fga': fga, 'fgm': fgm, 'fga2': fga-fga3, 'fgm2': fgm-fgm3, 'fga3': fga3, 'fgm3': fgm3}


def get_minutes(boxscore, player_name):
    df = boxscore[boxscore['name'].str.lower() == player_name.lower()]
    if df.empty:
        parts = player_name.lower().split()
        df = boxscore[boxscore['name'].str.lower().apply(lambda n: all(p in n for p in parts))]
    if df.empty: return 0
    for col in ['minutes', 'min']:
        if col in df.columns:
            try:
                val = str(df[col].iloc[0])
                if ':' in val:
                    p = val.split(':')
                    return int(p[0]) * 60 + int(p[1])
                return int(float(val)) * 60
            except: continue
    return 0


# ─────────────────────────────────────────────────────────────────────────────
# SVG BUILDER
# ─────────────────────────────────────────────────────────────────────────────

def fg_color(pct):
    if pct is None: return None
    if pct <= 20:   return "#ef4444"
    if pct <= 40:   return "#f97316"
    if pct <= 60:   return "#eab308"
    if pct <= 80:   return "#84cc16"
    return "#22c55e"

def fmt(fgm, fga):
    if fga == 0: return "-/-", "--%", None
    pct = round(fgm / fga * 100)
    return f"{fgm}/{fga}", f"{pct}%", pct

def pct_str(fgm, fga):
    return f"{round(fgm/fga*100)}%" if fga else "--%"

def time_str(secs):
    return f"{secs//60}m {secs%60:02d}s"

ZONE_FILLS = {
    'right_corner_3':  '<rect x="10" y="10" width="152" height="85" fill="{c}" opacity="0.65"/>',
    'left_corner_3':   '<rect x="10" y="645" width="152" height="85" fill="{c}" opacity="0.65"/>',
    'right_wing_3':    '<path d="M 162 10 L 520 10 L 520 270 L 371 270 A 280 280 0 0 0 162 95 Z" fill="{c}" opacity="0.65"/>',
    'left_wing_3':     '<path d="M 162 645 A 280 280 0 0 0 371 470 L 520 470 L 520 730 L 162 730 Z" fill="{c}" opacity="0.65"/>',
    'top_of_key_3':    '<path d="M 371 270 L 520 270 L 520 470 L 371 470 A 280 280 0 0 0 371 270 Z" fill="{c}" opacity="0.65"/>',
    'right_elbow':     '<path d="M 162 95 A 280 280 0 0 1 371 270 L 198 270 L 198 95 Z" fill="{c}" opacity="0.65"/>',
    'left_elbow':      '<path d="M 371 470 A 280 280 0 0 1 162 645 L 198 645 L 198 470 Z" fill="{c}" opacity="0.65"/>',
    'mid_range_right': '<rect x="10" y="95" width="188" height="175" fill="{c}" opacity="0.65"/>',
    'mid_range_left':  '<rect x="10" y="470" width="188" height="175" fill="{c}" opacity="0.65"/>',
    'mid_range_top':   '<path d="M 198 270 L 371 270 A 280 280 0 0 1 371 470 L 198 470 Z" fill="{c}" opacity="0.65"/>',
    'paint':           '<rect x="10" y="270" width="188" height="200" fill="{c}" opacity="0.65"/>',
}

COURT = """  <path d="M 670 300 A 70 70 0 0 1 670 440" fill="none" stroke="#2a2a2a" stroke-width="2.5"/>
  <rect x="10" y="270" width="188" height="200" fill="none" stroke="#2a2a2a" stroke-width="2"/>
  <path d="M 198 270 A 120 100 0 0 1 198 470" fill="none" stroke="#2a2a2a" stroke-width="2"/>
  <circle cx="27" cy="370" r="17" fill="none" stroke="#cc4400" stroke-width="3"/>
  <line x1="12" y1="342" x2="12" y2="398" stroke="#2a2a2a" stroke-width="6" stroke-linecap="round"/>
  <line x1="10" y1="95" x2="162" y2="95" stroke="#2a2a2a" stroke-width="2.5"/>
  <line x1="10" y1="645" x2="162" y2="645" stroke="#2a2a2a" stroke-width="2.5"/>
  <path d="M 162 95 A 280 280 0 0 1 162 645" fill="none" stroke="#2a2a2a" stroke-width="4"/>
  <line x1="10" y1="95" x2="162" y2="95" stroke="#aaaaaa" stroke-width="1.5" stroke-dasharray="6 4"/>
  <line x1="10" y1="645" x2="162" y2="645" stroke="#aaaaaa" stroke-width="1.5" stroke-dasharray="6 4"/>
  <rect x="10" y="270" width="188" height="200" fill="none" stroke="#aaaaaa" stroke-width="1.5" stroke-dasharray="6 4"/>
  <path d="M 198 270 A 120 100 0 0 1 198 470" fill="none" stroke="#aaaaaa" stroke-width="1.5" stroke-dasharray="6 4"/>
  <line x1="162" y1="10" x2="162" y2="95" stroke="#aaaaaa" stroke-width="1.5" stroke-dasharray="6 4"/>
  <line x1="162" y1="645" x2="162" y2="730" stroke="#aaaaaa" stroke-width="1.5" stroke-dasharray="6 4"/>
  <line x1="198" y1="105" x2="198" y2="270" stroke="#aaaaaa" stroke-width="1.5" stroke-dasharray="6 4"/>
  <line x1="198" y1="470" x2="198" y2="635" stroke="#aaaaaa" stroke-width="1.5" stroke-dasharray="6 4"/>
  <line x1="198" y1="270" x2="371" y2="270" stroke="#aaaaaa" stroke-width="1.5" stroke-dasharray="6 4"/>
  <line x1="198" y1="470" x2="371" y2="470" stroke="#aaaaaa" stroke-width="1.5" stroke-dasharray="6 4"/>
  <path d="M 371 270 A 280 280 0 0 1 371 470" fill="none" stroke="#aaaaaa" stroke-width="1.5" stroke-dasharray="6 4"/>
  <line x1="371" y1="270" x2="520" y2="270" stroke="#aaaaaa" stroke-width="1.5" stroke-dasharray="6 4"/>
  <line x1="371" y1="470" x2="520" y2="470" stroke="#aaaaaa" stroke-width="1.5" stroke-dasharray="6 4"/>
  <path d="M 162 95 A 280 280 0 0 1 371 270" fill="none" stroke="#aaaaaa" stroke-width="1.5" stroke-dasharray="6 4"/>
  <path d="M 371 470 A 280 280 0 0 1 162 645" fill="none" stroke="#aaaaaa" stroke-width="1.5" stroke-dasharray="6 4"/>
  <line x1="520" y1="10" x2="520" y2="730" stroke="#aaaaaa" stroke-width="1.5" stroke-dasharray="6 4"/>"""

LEGEND = """  <rect x="528" y="16" width="136" height="164" rx="5" fill="white" opacity="0.80"/>
  <text x="596" y="34" text-anchor="middle" font-size="11" font-weight="700" fill="#111" font-family="sans-serif">FG% Scale</text>
  <rect x="538" y="42" width="16" height="16" rx="2" fill="#ef4444"/>
  <text x="560" y="54" font-size="10" fill="#111" font-family="sans-serif">0–20%</text>
  <rect x="538" y="64" width="16" height="16" rx="2" fill="#f97316"/>
  <text x="560" y="76" font-size="10" fill="#111" font-family="sans-serif">21–40%</text>
  <rect x="538" y="86" width="16" height="16" rx="2" fill="#eab308"/>
  <text x="560" y="98" font-size="10" fill="#111" font-family="sans-serif">41–60%</text>
  <rect x="538" y="108" width="16" height="16" rx="2" fill="#84cc16"/>
  <text x="560" y="120" font-size="10" fill="#111" font-family="sans-serif">61–80%</text>
  <rect x="538" y="130" width="16" height="16" rx="2" fill="#22c55e"/>
  <text x="560" y="142" font-size="10" fill="#111" font-family="sans-serif">81–100%</text>
  <rect x="538" y="152" width="16" height="16" rx="2" fill="#f0ead8" stroke="#aaa" stroke-width="1"/>
  <text x="560" y="164" font-size="10" fill="#111" font-family="sans-serif">No attempts</text>"""

LABEL_DEFS = [
    ('right_corner_3',  45,  30,  84, 16, 60,  76,  "#EEEDFE","#534AB7","#3C3489","right corner 3"),
    ('left_corner_3',   45,  676, 82, 16, 706, 722, "#EEEDFE","#534AB7","#3C3489","left corner 3"),
    ('right_wing_3',   300,  118, 74, 16, 150, 166, "#EEEDFE","#534AB7","#3C3489","right wing 3"),
    ('left_wing_3',    300,  590, 72, 16, 622, 638, "#EEEDFE","#534AB7","#3C3489","left wing 3"),
    ('top_of_key_3',   406,  355, 88, 16, 387, 403, "#EEEDFE","#534AB7","#3C3489","top of key 3"),
    ('right_elbow',    220,  198, 76, 16, 230, 246, "#E1F5EE","#1D9E75","#085041","right elbow"),
    ('left_elbow',     220,  512, 68, 16, 544, 560, "#E1F5EE","#1D9E75","#085041","left elbow"),
    ('mid_range_right', 55,  165, 90, 16, 197, 213, "#E1F5EE","#1D9E75","#085041","mid-range right"),
    ('mid_range_left',  55,  548, 90, 16, 580, 596, "#E1F5EE","#1D9E75","#085041","mid-range left"),
    ('mid_range_top',  230,  355,114, 16, 387, 403, "#E1F5EE","#1D9E75","#085041","mid-range top"),
    ('paint',           80,  355, 46, 16, 387, 403, "#FAECE7","#993C1D","#712B13","paint"),
]

def build_svg(title, title_color, zones, box, team_label, last, secs):
    fills  = ""
    for zone, tmpl in ZONE_FILLS.items():
        v = zones.get(zone, {'fga': 0, 'fgm': 0})
        if v['fga'] > 0:
            _, _, pct = fmt(v['fgm'], v['fga'])
            fills += "  " + tmpl.replace("{c}", fg_color(pct)) + "\n"

    labels = ""
    for (zone, rx, ry, rw, rh, ty1, ty2, fill, stroke, tcol, label) in LABEL_DEFS:
        v  = zones.get(zone, {'fga': 0, 'fgm': 0})
        ma, pc, _ = fmt(v['fgm'], v['fga'])
        cx = rx + rw // 2
        labels += f"""
  <rect x="{rx}" y="{ry}" width="{rw}" height="{rh}" rx="3" fill="{fill}" stroke="{stroke}" stroke-width="1"/>
  <text x="{cx}" y="{ry+12}" text-anchor="middle" font-size="10" fill="{tcol}" font-family="sans-serif" font-weight="500">{label}</text>
  <text x="{cx}" y="{ty1}" text-anchor="middle" font-size="13" font-weight="700" fill="#111" font-family="sans-serif">{ma}</text>
  <text x="{cx}" y="{ty2}" text-anchor="middle" font-size="13" font-weight="700" fill="#111" font-family="sans-serif">{pc}</text>"""

    fga2=box['fga2']; fgm2=box['fgm2']; fga3=box['fga3']; fgm3=box['fgm3']
    tfga=box['fga'];  tfgm=box['fgm'];  ts=time_str(secs); b=254

    sidebar = f"""  <rect x="528" y="192" width="136" height="50" rx="5" fill="white" opacity="0.80"/>
  <text x="596" y="210" text-anchor="middle" font-size="11" font-weight="700" fill="#111" font-family="sans-serif">{team_label} Player:</text>
  <text x="596" y="230" text-anchor="middle" font-size="11" fill="#333" font-family="sans-serif">{last}</text>
  <rect x="528" y="254" width="136" height="204" rx="5" fill="white" opacity="0.80"/>
  <text x="596" y="272" text-anchor="middle" font-size="11" font-weight="700" fill="#111" font-family="sans-serif">Player Stats</text>
  <line x1="535" y1="{b+23}" x2="657" y2="{b+23}" stroke="#ccc" stroke-width="1"/>
  <text x="535" y="{b+38}" font-size="10" fill="#555" font-family="sans-serif">Time on court:</text>
  <text x="657" y="{b+38}" text-anchor="end" font-size="10" font-weight="700" fill="#111" font-family="sans-serif">{ts}</text>
  <text x="535" y="{b+54}" font-size="10" fill="#555" font-family="sans-serif">Total FGAs:</text>
  <text x="657" y="{b+54}" text-anchor="end" font-size="10" font-weight="700" fill="#111" font-family="sans-serif">{tfga}</text>
  <text x="535" y="{b+70}" font-size="10" fill="#555" font-family="sans-serif">Total FGMs:</text>
  <text x="657" y="{b+70}" text-anchor="end" font-size="10" font-weight="700" fill="#111" font-family="sans-serif">{tfgm}</text>
  <text x="535" y="{b+86}" font-size="10" fill="#555" font-family="sans-serif">Total FG%:</text>
  <text x="657" y="{b+86}" text-anchor="end" font-size="10" font-weight="700" fill="#111" font-family="sans-serif">{pct_str(tfgm,tfga)}</text>
  <line x1="535" y1="{b+94}" x2="657" y2="{b+94}" stroke="#eee" stroke-width="1"/>
  <text x="535" y="{b+108}" font-size="10" fill="#555" font-family="sans-serif">Total 2FGAs:</text>
  <text x="657" y="{b+108}" text-anchor="end" font-size="10" font-weight="700" fill="#111" font-family="sans-serif">{fga2}</text>
  <text x="535" y="{b+124}" font-size="10" fill="#555" font-family="sans-serif">Total 2FGMs:</text>
  <text x="657" y="{b+124}" text-anchor="end" font-size="10" font-weight="700" fill="#111" font-family="sans-serif">{fgm2}</text>
  <text x="535" y="{b+140}" font-size="10" fill="#555" font-family="sans-serif">Total 2FG%:</text>
  <text x="657" y="{b+140}" text-anchor="end" font-size="10" font-weight="700" fill="#111" font-family="sans-serif">{pct_str(fgm2,fga2)}</text>
  <line x1="535" y1="{b+148}" x2="657" y2="{b+148}" stroke="#eee" stroke-width="1"/>
  <text x="535" y="{b+162}" font-size="10" fill="#555" font-family="sans-serif">Total 3FGAs:</text>
  <text x="657" y="{b+162}" text-anchor="end" font-size="10" font-weight="700" fill="#111" font-family="sans-serif">{fga3}</text>
  <text x="535" y="{b+178}" font-size="10" fill="#555" font-family="sans-serif">Total 3FGMs:</text>
  <text x="657" y="{b+178}" text-anchor="end" font-size="10" font-weight="700" fill="#111" font-family="sans-serif">{fgm3}</text>
  <text x="535" y="{b+194}" font-size="10" fill="#555" font-family="sans-serif">Total 3FG%:</text>
  <text x="657" y="{b+194}" text-anchor="end" font-size="10" font-weight="700" fill="#111" font-family="sans-serif">{pct_str(fgm3,fga3)}</text>"""

    return f"""<svg width="100%" viewBox="10 -50 660 780" xmlns="http://www.w3.org/2000/svg">
  <rect x="10" y="10" width="660" height="720" rx="6" fill="#f0ead8" stroke="#2a2a2a" stroke-width="2.5"/>
{fills}
{COURT}
  <text x="340" y="-22" text-anchor="middle" font-size="16" font-weight="700" fill="{title_color}" font-family="sans-serif">{title}</text>
{labels}
{LEGEND}
{sidebar}
</svg>"""


# ─────────────────────────────────────────────────────────────────────────────
# ROUTES
# ─────────────────────────────────────────────────────────────────────────────

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/teams')
def api_teams():
    return jsonify(get_all_teams())


@app.route('/api/search_team')
def api_search_team():
    query = request.args.get('q', '').strip()
    if not query:
        return jsonify({'error': 'No query provided'}), 400
    team_id, display = find_team_id(query)
    if not team_id:
        return jsonify({'error': f"Team '{query}' not found"}), 404
    return jsonify({'id': team_id, 'name': display})


@app.route('/api/schedule/<int:team_id>')
def api_schedule(team_id):
    games = fetch_schedule(team_id)
    return jsonify(games)


@app.route('/api/players/<game_id>')
def api_players(game_id):
    team_name = request.args.get('team', '')
    try:
        shots, date, primary_name, opp_name, boxscore = pull_game_data(game_id, team_name)
        players = []
        for _, r in boxscore[boxscore['is_primary'] == True].iterrows():
            players.append({'name': r['name'], 'starter': bool(r['starter']), 'team': primary_name, 'is_primary': True})
        for _, r in boxscore[boxscore['is_primary'] == False].iterrows():
            players.append({'name': r['name'], 'starter': bool(r['starter']), 'team': opp_name, 'is_primary': False})
        return jsonify({
            'players':      players,
            'primaryTeam':  primary_name,
            'oppTeam':      opp_name,
            'date':         date,
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/chart/<game_id>/<path:player_name>')
def api_chart(game_id, player_name):
    team_name = request.args.get('team', '')
    try:
        shots, date, primary_name, opp_name, boxscore = pull_game_data(game_id, team_name)
        if not shots.empty and 'shot_x' in shots.columns:
            shots['zone'] = shots.apply(lambda r: classify_shot(r['shot_x'], r['shot_y']), axis=1)

        player_row = boxscore[boxscore['name'].str.lower() == player_name.lower()]
        if player_row.empty:
            parts = player_name.lower().split()
            player_row = boxscore[boxscore['name'].str.lower().apply(lambda n: all(p in n for p in parts))]
        if player_row.empty:
            return jsonify({'error': f"Player '{player_name}' not found"}), 404

        full_name   = player_row.iloc[0]['name']
        is_primary  = player_row.iloc[0]['is_primary']
        last        = full_name.split()[-1]
        team_label  = primary_name if is_primary else opp_name
        opp_label   = opp_name if is_primary else primary_name
        title_color = "#002E5D" if is_primary else "#CC0000"

        zones = tally_zones(shots, full_name)
        box   = tally_from_boxscore(boxscore, full_name)
        secs  = get_minutes(boxscore, full_name)
        title = f"{full_name} Shot Chart against {opp_label} on {date}"

        svg = build_svg(title, title_color, zones, box, team_label, last, secs)
        return jsonify({'svg': svg, 'title': title, 'filename': f"{last} Shot Chart against {opp_label} on {date.replace('/', '-')}.svg"})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, port=5000)
