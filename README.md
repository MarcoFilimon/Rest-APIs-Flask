# https://rest-apis-flask.teclado.com/

docker build -t flask-smorest-api .

docker run -dp 5000:5000 -w /app -v "${PWD}:/app" flask-smorest-api


Docker debug

docker compose -f .\docker-compose.yml -f .\docker-compose.debug.yml up

And run python debug config


# dump_only=True -> https://gemini.google.com/share/521374387799
# blp.response -> https://g.co/gemini/share/59af914a17ff
