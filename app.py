import os
from dotenv import load_dotenv
from app import app

# config/startup
if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=os.environ.get('PORT'),
            debug=True)