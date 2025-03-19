from flask import Flask, request, jsonify
import pandas as pd
import os

app = Flask(__name__)

# Load CSV file with error handling
csv_file = "scraped_data.csv"

if not os.path.exists(csv_file):
    df = pd.DataFrame(columns=["Title", "URL"])  # Create an empty DataFrame
else:
    try:
        df = pd.read_csv(csv_file, encoding="ISO-8859-1") 
    except Exception as e:
        print(f"Error loading CSV: {e}")
        df = pd.DataFrame(columns=["Title", "URL"])  # Fallback empty DataFrame

@app.route('/')  # ✅ Default route to prevent 404
def home():
    return "Flask app is running! Use /search?query=your_keyword to search."

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query', '').lower()

    if "Title" not in df.columns:
        return jsonify({'error': 'CSV does not contain a "Title" column'})

    results = df[df['Title'].astype(str).str.lower().str.contains(query, na=False)]

    if results.empty:
        return jsonify({'message': 'No matching articles found'})

    return jsonify(results.to_dict(orient='records'))

if __name__ == '__main__':
    app.run(debug=True)
