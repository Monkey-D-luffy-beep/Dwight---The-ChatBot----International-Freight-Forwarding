cd backend
.\venv\Scripts\python.exe -m uvicorn main:app --host 127.0.0.1 --port 8000



cd ..
.\backend\venv\Scripts\python.exe -m http.server 3000 --directory frontend
