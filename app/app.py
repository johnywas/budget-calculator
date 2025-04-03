import os
from flask import Flask, render_template, request, redirect, url_for, flash
import pandas as pd
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # For flash messages
app.config['UPLOAD_FOLDER'] = '/tmp/uploads'
app.config['ALLOWED_EXTENSIONS'] = {'xls', 'xlsx'}

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Check if files were uploaded
        if 'files' not in request.files:
            flash('No files selected')
            return redirect(request.url)
        
        files = request.files.getlist('files')
        
        # Check if any files were selected
        if not files or files[0].filename == '':
            flash('No files selected')
            return redirect(request.url)
        
        total_sum = 0
        processed_files = []
        
        for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
                
                try:
                    # Read Excel file
                    df = pd.read_excel(filepath)
                    
                    # Check if there are at least 4 columns
                    if len(df.columns) < 4:
                        flash(f'File {filename} does not have enough columns')
                        continue
                    
                    # Group by 'Establecimiento/concepto' and sum the 'Importe' column
                    grouped = df.groupby('Establecimiento/concepto').agg({'Importe': 'sum'}).reset_index()
                    grouped = grouped.sort_values(by='Importe', ascending=False)  # Sort by total cost
                    
                    total_sum = grouped['Importe'].sum()  # Total costs
                    
                    processed_files.append({
                        'name': filename,
                        'grouped_data': grouped.to_dict(orient='records'),  # Convert to dict for rendering
                        'total_sum': total_sum
                    })
                    
                except Exception as e:
                    flash(f'Error processing {filename}: {str(e)}')
                
                # Clean up uploaded file
                os.remove(filepath)
            else:
                flash(f'Invalid file: {file.filename}')
        
        if processed_files:
            return render_template('result.html', 
                                  total_sum=total_sum, 
                                  files=processed_files)
    
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
