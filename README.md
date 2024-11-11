# TLCEngineChatSearch

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

# create .env file if doesn't already exist using .env.example
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
#to run via docker containers
docker-compose up
```

### Note to self for expo

- Run front end locally
- Run chatSearchServer.py on Mac Studio
- Run `ssh -L 5000:localhost:5000 tlcengine@dev.tlcengine.com` on my machine to forward Mac Studio localhost:5000 to my localhost:5000
