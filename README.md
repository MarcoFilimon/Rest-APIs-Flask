# Insomnia is the client. Or the web page itself. The server is the API?

# https://rest-apis-flask.teclado.com/

docker build -t flask-smorest-api .

docker run -dp 5000:5000 -w /app -v "${PWD}:/app" flask-smorest-api


Docker debug

docker compose -f .\docker-compose.yml -f .\docker-compose.debug.yml up

And run python debug config