FROM nginx:latest

RUN mkdir -p /app/staticfiles && chmod -R 755 /app/staticfiles

COPY nginx.conf /etc/nginx/nginx.conf

EXPOSE 80
