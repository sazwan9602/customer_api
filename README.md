# FastAPI (Customer Management)

###Local Database
1. This project used MySql database
2. Your local database setting can be configured in .env file

###Install required files
1. Create your python virtual environment in your command line
```
python -m venv myenv
```
2. Activate virtual environment (windows)
```
source myenv/Scripts/activate
```
3. Navigate to project folder, install requirements
```
pip install -r requirements.txt
```

###Run App
1. On root project folder, run
```
uvicorn src.main:app
```
2. Upon testing, you are required to authenticate before run any API endpoints.
```
username: admin
password: admin123
```
