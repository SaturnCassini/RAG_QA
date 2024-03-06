# This is a dockerfile for the knower app
FROM node:latest

WORKDIR /knower
COPY package*.json ./
RUN npm install
COPY . .
EXPOSE 5000
# run dev in port 5000
CMD npm run dev
