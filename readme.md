Test project for testing "test app"

### Build
1. Download https://github.com/dgusakov/test_app
1. Create dokcer-image and run:
```
docker build --tag test_app:latest .
docker run -p 5000:5000 -d test_app:latest
```
3. Download this project, create venv
4. Make in terminal in venv:
```
pip install -r requirements.txt
```
5. In venv's terminal write:
```
pytest -v --tb=short
```
