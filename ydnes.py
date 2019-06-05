import tornado.ioloop
import tornado.web
import requests
import get

newAddress = "ydnes.cz:8080"
originalAddress = "idnes.cz"

class AllHandler(tornado.web.RequestHandler):
    def get(self):
        url = "http://" + originalAddress + self.request.uri
        page = get.getPage(url, originalAddress, newAddress)
        self.write(page)

def make_app():
    return tornado.web.Application([
        (r".*", AllHandler),
    ],
    debug = True
    )

if __name__ == "__main__":
    app = make_app()
    app.listen(8080)
    tornado.ioloop.IOLoop.current().start()
