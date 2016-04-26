# Guide: http://flask-.readthedocs.org/en/0.3/deploying/others.html
from gevent.wsgi import WSGIServer
from TWIDDER import app

http_server = WSGIServer(('', 5000), app)
http_server.serve_forever()

# Run file as a application
if __name__ == "__main__":
    app.run()
    # app.run(host = '127.0.0.1', port = 5051)
