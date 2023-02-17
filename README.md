# ReFood
Search engine for book reviews dataset.

## Client
The user interface is created using Angluar.
Setup:
```
npm install -g @angular/cli
npm install
```

Run client:
```
ng serve --open
```

## Server
Back-end is coded in Python using FastAPI framework.

Setup:
```
pip install fastapi
pip install "uvicorn[standard]"
```

Run server:
```
uvicorn main:app --reload
```

## Benchmark
You can run benchmark in server/benchmark:
```
python main.py
```
