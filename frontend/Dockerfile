FROM node:latest

WORKDIR /app

COPY package.json ./

RUN npm i

COPY . .

#Change this to be the Variable in .env
EXPOSE 5173

CMD ["npm", "run", "dev"]