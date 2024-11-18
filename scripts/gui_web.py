from flask import Flask, render_template, request, redirect, flash, url_for
from werkzeug.utils import secure_filename
import os
from datetime import datetime
import logging
from send_emails import send_emails  # Assuming you have a send_emails.py script to handle email sending

# Base directory setup
BASE_DIR = r'F:/codes/cloud master/'
app = Flask(__name__, template_folder=os.path.join(BASE_DIR, 'templates'))
app.secret_key = 'superseceretkey'  # To use flash

log_file = os.path.join(BASE_DIR, 'logs', 'spy_pixel.log')
logging.basicConfig(
    filename=log_file, level=logging.INFO,
    format='%(asctime)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

# Directories for storing files
data_dir = os.path.join(BASE_DIR, 'data')
template_dir = os.path.join(BASE_DIR, 'templates')

# Ensure the folders exist
os.makedirs(data_dir, exist_ok=True)
os.makedirs(template_dir, exist_ok=True)

# Allowed file types
ALLOWED_EXTENSIONS = {'xlsx', 'html'}

def allowed_file(filename):
    """Check if the file has an allowed extension."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Route for the home page
@app.route('/')
def index():
    """Display the home page with the list of uploaded files."""
    excel_files = os.listdir(data_dir)
    template_files = os.listdir(template_dir)
    return render_template('index.html', excel_files=excel_files, template_files=template_files)

# Route to handle Excel file upload
@app.route('/upload_excel', methods=['POST'])
def upload_excel():
    """Handle the upload of Excel files."""
    if 'excelFile' not in request.files:
        flash('No file part', 'error')
        return redirect(url_for('index'))

    file = request.files['excelFile']
    if file.filename == '':
        flash('No selected Excel file', 'error')
        return redirect(url_for('index'))

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(data_dir, filename))
        flash(f'Excel file "{filename}" uploaded successfully!', 'success')
    
    return redirect(url_for('index'))

# Route to handle Template file upload
@app.route('/upload_template', methods=['POST'])
def upload_template():
    """Handle the upload of HTML template files."""
    if 'templateFile' not in request.files:
        flash('No file part', 'error')
        return redirect(url_for('index'))

    file = request.files['templateFile']
    if file.filename == '':
        flash('No selected template file', 'error')
        return redirect(url_for('index'))

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(template_dir, filename))
        flash(f'Template file "{filename}" uploaded successfully!', 'success')
    
    return redirect(url_for('index'))

# Route to handle sending emails
@app.route('/send_emails', methods=['POST'])
def send_emails_action():
    """Handle the process of sending emails using selected files."""
    excel_file = request.form.get('selected_excel')
    template_file = request.form.get('selected_template')

    if not excel_file or not template_file:
        flash('Please select both an Excel file and a Template file.', 'error')
        return redirect(url_for('index'))

    try:
        # Full paths to the selected files
        excel_file_path = os.path.join(data_dir, excel_file)
        template_file_path = os.path.join(template_dir, template_file)

        # Call the function to send emails
        send_emails(excel_file_path, template_file_path)
        flash('Emails sent successfully!', 'success')
    except Exception as e:
        flash(f'Error sending emails: {e}', 'error')

    return redirect(url_for('index'))

@app.route('/pixel/<email>')
def pixel(email):
    # Log the access to the pixel
    logging.info(f"Email opened by: {email} at {datetime.now()} from {request.remote_addr} using {request.user_agent}\n")
    
    # Redirect to the actual pixel image URL
    return redirect("http://ailetechnology.net/public/spy-pixel.png")


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000)