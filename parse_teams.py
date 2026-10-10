from bs4 import BeautifulSoup

with open('collegeteam.html', 'r', encoding='utf-8', errors='ignore') as f:
    soup = BeautifulSoup(f, 'html.parser')

tables = soup.find_all('table')
print(f"Found {len(tables)} tables.")

# Print the first table's headers and first row, or something useful
for i, table in enumerate(tables):
    print(f"--- Table {i} ---")
    headers = [th.text.strip() for th in table.find_all('th')]
    print("Headers:", headers)
    rows = table.find_all('tr')
    if len(rows) > 1:
        cells = [td.text.strip() for td in rows[1].find_all('td')]
        print("First Row:", cells)
    print()
    if i > 2: break
