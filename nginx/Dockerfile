FROM nginx:1.19.2

RUN rm -v /etc/nginx/nginx.conf
ADD ./nginx/nginx.conf /etc/nginx/

RUN mkdir /nginx
COPY /server/app/client /nginx/client
