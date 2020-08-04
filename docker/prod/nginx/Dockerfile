FROM nginx:latest

# nginx configuration
#RUN mv /etc/nginx/nginx.conf /etc/nginx/nginx.conf_orig
#RUN mv ./docker/prod/nginx/docker_nginx.conf /etc/nginx/nginx.conf

# REMOVE DEFAULT NGINX DEFAULT CONF
RUN rm /etc/nginx/conf.d/default.conf
COPY ./docker/prod/nginx/docker_nginx.conf /etc/nginx/conf.d/