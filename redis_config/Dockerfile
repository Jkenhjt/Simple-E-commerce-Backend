FROM redis

WORKDIR /redis_conf

COPY redis.conf /redis_conf

EXPOSE 6379

CMD ["redis-server", "/redis_conf/redis.conf"]