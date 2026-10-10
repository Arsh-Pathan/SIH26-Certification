import os
import pandas as pd
import re
from flask import Flask, render_template, request, send_from_directory, abort

app = Flask(__name__)

# Load data
df = pd.read_csv('SIH_Teams_Members.csv')
# Convert team ID to string for robust matching
df['Team ID'] = df['Team ID'].astype(str)
# Remove nan or empty rows
df = df.dropna(subset=['Team ID', 'Team Name'])

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query', '').strip()
    if not query:
        return render_template('index.html', error="Please enter a Team ID or Team Name.")
    
    # Search by Team ID or Team Name (case-insensitive)
    matches = df[(df['Team ID'] == query) | (df['Team Name'].str.contains(query, case=False, na=False))]
    
    if matches.empty:
        return render_template('index.html', error="No team found with that ID or Name.")
    
    # We might have multiple teams matched if searched by a partial name, 
    # but let's group by Team ID
    teams = {}
    for _, row in matches.iterrows():
        tid = row['Team ID']
        if tid not in teams:
            teams[tid] = {
                'id': tid,
                'name': row['Team Name'],
                'members': []
            }
        teams[tid]['members'].append({
            'name': row['Member Name'],
            'role': row['Role']
        })
        
    return render_template('results.html', teams=teams.values(), query=query)

@app.route('/download/<team_id>/<member_name>')
def download(team_id, member_name):
    # Find the team
    team_rows = df[df['Team ID'] == team_id]
    if team_rows.empty:
        abort(404)
    team_name = team_rows.iloc[0]['Team Name']
    
    # Construct filename exactly as in the generation script
    safe_name = re.sub(r'[^a-zA-Z0-9_\- ]', "", member_name).strip()
    safe_team = re.sub(r'[^a-zA-Z0-9_\- ]', "", team_name).strip()
    filename = f"{safe_team}_{safe_name}.png"
    
    certs_dir = os.path.join(app.root_path, 'Certificates')
    
    if not os.path.exists(os.path.join(certs_dir, filename)):
        abort(404, description="Certificate file not found.")
        
    return send_from_directory(certs_dir, filename, as_attachment=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
