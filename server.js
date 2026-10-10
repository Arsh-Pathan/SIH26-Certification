const express = require('express');
const nunjucks = require('nunjucks');
const fs = require('fs');
const path = require('path');
const csv = require('csv-parser');

const app = express();
const port = process.env.PORT || 5000;

// Configure Nunjucks
const env = nunjucks.configure('templates', {
    autoescape: true,
    express: app
});
app.set('view engine', 'html');

// Add url_for equivalent
env.addGlobal('url_for', function(endpoint, kwargs) {
    if (endpoint === 'static') {
        return '/static/' + kwargs.filename;
    }
    return '/';
});

// Serve static files
app.use('/static', express.static(path.join(__dirname, 'static')));

// Load CSV data
let df = [];
fs.createReadStream('SIH_Teams_Members.csv')
  .pipe(csv())
  .on('data', (row) => {
      // Ensure row has required fields
      if (row['Team ID'] && row['Team Name']) {
          df.push(row);
      }
  })
  .on('end', () => {
      console.log('CSV file successfully processed');
  });

app.get('/', (req, res) => {
    res.render('index.html');
});

app.get('/search', (req, res) => {
    let query = req.query.query;
    if (!query || !query.trim()) {
        return res.render('index.html', { error: "Please enter a Team ID or Team Name." });
    }
    
    query = query.trim().toLowerCase();
    
    // Search matches
    let matches = df.filter(row => {
        let tid = String(row['Team ID']).toLowerCase();
        let tname = String(row['Team Name']).toLowerCase();
        return tid === query || tname.includes(query);
    });
    
    if (matches.length === 0) {
        return res.render('index.html', { error: "No team found with that ID or Name." });
    }
    
    // Helper function for title case
    const toTitleCase = (str) => {
        return str.replace(/\w\S*/g, (txt) => txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase());
    };
    
    // Group by Team ID
    let teamsMap = {};
    matches.forEach(row => {
        let tid = String(row['Team ID']);
        if (!teamsMap[tid]) {
            teamsMap[tid] = {
                id: tid,
                name: row['Team Name'],
                members: []
            };
        }
        teamsMap[tid].members.push({
            name: row['Member Name'],
            // Pre-format the role for the template (replaces python's .replace('_', ' ').title())
            role: row['Role'],
            formatted_role: toTitleCase((row['Role'] || '').replace(/_/g, ' '))
        });
    });
    
    res.render('results.html', { teams: Object.values(teamsMap), query: req.query.query });
});

app.get('/download/:team_id/:member_name', (req, res) => {
    let teamId = req.params.team_id;
    let memberName = req.params.member_name;
    
    let teamRow = df.find(row => String(row['Team ID']) === teamId);
    if (!teamRow) {
        return res.status(404).send('Team not found');
    }
    
    let teamName = teamRow['Team Name'];
    
    // Construct filename exactly as in the Python generation script
    // safe_name = re.sub(r'[^a-zA-Z0-9_\- ]', "", member_name).strip()
    let safeName = memberName.replace(/[^a-zA-Z0-9_\- ]/g, '').trim();
    let safeTeam = teamName.replace(/[^a-zA-Z0-9_\- ]/g, '').trim();
    
    let filename = `${safeTeam}_${safeName}.png`;
    let filepath = path.join(__dirname, 'Certificates', filename);
    
    if (!fs.existsSync(filepath)) {
        return res.status(404).send('Certificate file not found.');
    }
    
    res.download(filepath, filename);
});

app.listen(port, () => {
    console.log(`App listening at http://localhost:${port}`);
});
