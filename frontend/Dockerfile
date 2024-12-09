FROM node:latest

WORKDIR /app

COPY package.json ./

RUN npm i

RUN npm rebuild esbuild

COPY . .

#Change this to be the Variable in .env
EXPOSE 5173

# Command to run the application
CMD ["npm", "run", "dev"]
