from dotenv import load_dotenv

load_dotenv()

from app import create_app

app = create_app()


if __name__ == "__main__":
    # Keep behavior aligned with run.py for local development.
    app.run(debug=True, threaded=False, use_reloader=True)
