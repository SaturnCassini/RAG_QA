# This is a dockerfile for the knower app
FROM node:latest
WORKDIR /usr/app/
COPY package.json /usr/app/
RUN npm install
COPY . .
EXPOSE 5000
# run dev in port 5000
