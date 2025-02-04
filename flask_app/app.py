version: '3.8'
services:
  web:
    build: .
    ports:
      - "10100:5000"
    environment:
      FLASK_ENV: production
      MYSQL_HOST: db
      MYSQL_USER: flask_user
      MYSQL_PASSWORD: flask_password
      MYSQL_DATABASE: flask_app
    depends_on:
      db:
        condition: service_healthy  # Wartet, bis MySQL bereit ist
    networks:
      - app_network

  db:
    image: mysql:8.0
    restart: always
    environment:
      MYSQL_ROOT_PASSWORD: rootpassword
      MYSQL_DATABASE: flask_app
      MYSQL_USER: flask_user
      MYSQL_PASSWORD: flask_password
    ports:
      - "3306:3306"
    volumes:
      - mysql_data:/var/lib/mysql
    healthcheck:
      test: ["CMD", "mysqladmin", "ping", "-h", "localhost"]
      interval: 10s
      retries: 5
      start_period: 20s
    networks:
      - app_network

volumes:
  mysql_data:

networks:
  app_network:
    driver: bridge
