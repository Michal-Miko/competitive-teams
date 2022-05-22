# Stage 0, compile frontend to static html
FROM node:13.12.0-alpine as build-stage

# set working directory
WORKDIR /app

# install app dependencies
COPY package.json ./
COPY package-lock.json ./
RUN npm install
RUN npm install react-scripts@3.4.1 -g

# add app
COPY . ./

ARG react_app_firebase_apikey
ARG react_app_firebase_authdomain
ARG react_app_firebase_project_id
ARG react_app_firebase_storage_bucket
ARG react_app_firebase_messagingsenderid
ARG react_app_firebase_appid
ARG react_app_firebase_measurementid


# build app
RUN REACT_APP_FIREBASE_APIKEY=$react_app_firebase_apikey \
    REACT_APP_FIREBASE_AUTHDOMAIN=$react_app_firebase_authdomain \
    REACT_APP_FIREBASE_PROJECT_ID=$react_app_firebase_project_id \
    REACT_APP_FIREBASE_STORAGE_BUCKET=$react_app_firebase_storage_bucket \
    REACT_APP_FIREBASE_MESSAGINGSENDERID=$react_app_firebase_messagingsenderid \
    REACT_APP_FIREBASE_APPID=$react_app_firebase_appid \
    REACT_APP_FIREBASE_MEASUREMENTID=$react_app_firebase_measurementid \
    npm run build

# Stage 1, run nginx
FROM nginx:latest

# Set up default env attributes
ARG port=80
ARG frontend_name=127.0.0.1
ARG backend_url=http://127.0.0.1:8000

ENV PORT=$port
ENV FRONTEND_NAME=$frontend_name
ENV BACKEND_URL=$backend_url

COPY --from=build-stage /app/build/ /usr/share/nginx/html

COPY --from=build-stage /app/nginx.conf /etc/nginx/conf.d/default.conf.template

CMD /bin/bash -c "envsubst '\$PORT \$BACKEND_URL \$FRONTEND_NAME' < /etc/nginx/conf.d/default.conf.template > /etc/nginx/conf.d/default.conf && nginx -g 'daemon off;'"
