import sys
import os
# Add the site-packages directory to Python path
site_packages = os.path.join(os.path.dirname(__file__), 'newenv/lib/python3.11/site-packages')
sys.path.append(site_packages)

import uvicorn

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True) 