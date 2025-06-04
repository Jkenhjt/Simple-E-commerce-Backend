FROM nginx

WORKDIR /nginx_conf

COPY nginx.conf /nginx_conf

EXPOSE 81

CMD ["nginx", "-c", "/nginx_conf/nginx.conf"]