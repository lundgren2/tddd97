# Guide: http://flask-.readthedocs.org/en/0.3/deploying/others.html
from gevent.wsgi import WSGIServer
from gevent import pywsgi
from geventwebsocket.handler import WebSocketHandler
from TWIDDER import app



# Run file as a application
if __name__ == "__main__":
    http_server = WSGIServer(('', 5000), app, handler_class=WebSocketHandler)
    http_server.serve_forever()
    #app.run(debug=True)
    app.run(host = '127.0.0.1', port = 5000)
