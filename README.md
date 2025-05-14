# Insomnia is the client. Or the web page itself. The server is the API?

## To run the deploy Dockerfile locally - https://rest-apis-flask.teclado.com/docs/deploy_to_render/docker_with_gunicorn/

'''
docker build -t deployed-site-flask .
docker run -dp 5000:5000 -w /app -v "$(PWD):/app" deployed-site-flask sh -c "flask run --host 0.0.0.0"
'''
