# TLCEngineChatSearch
These commands work for Mac, if you have windows it is stil possible, just different commands
```bash
# run frontend
cd frontend

# install dependencies
npm install

# run dev server
npm run dev

# build for static site
npm run build
```


```bash
# run backend
cd backend

# create .env file if doesn't already exist using .env.example. Fill in the API_KEY accordingly. 
cp .env.example .env

# create .venv if it doesn't already exist
python3 -m venv .venv

# install dependencies
source .venv/bin/activate
pip install -r requirements.txt

# run server
python chatSearchServer.py

# update dependencies by doing 
pip freeze > requirements.txt
```

```

```
