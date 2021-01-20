# InstaSTATS

version: "3.9"
services:
  frontend:
    image: instastatspy:lts
    volumes:
      - stats:/app/stats
volumes:
  stats:
