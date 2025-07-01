# run.py
# ----------------------------------------------------------------
# Entry point for the Flask application
# Uses the application factory pattern to initialize and run the app
# ----------------------------------------------------------------

from app import create_app
from app.config.logger_loader import app_logger

# Create the Flask app using factory method
app = create_app()

if __name__ == '__main__':
    app_logger.info("Starting Flask server...")
    app.run(host='0.0.0.0', port=5000, debug=True)
