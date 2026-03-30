from dotenv import load_dotenv
load_dotenv()

from app import create_app

app = create_app()

if __name__ == "__main__":
    # Disable threading for simple synchronous execution
    app.run(debug=True, threaded=False, use_reloader=True)
