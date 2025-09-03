# Stage 1: build
FROM node:20-alpine as build

WORKDIR /app
COPY package.json ./
RUN npm install --silent
COPY . .
RUN npm run build

# Stage 2: serve
FROM nginx:alpine
WORKDIR /usr/share/nginx/html
COPY --from=build /app/dist .
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
