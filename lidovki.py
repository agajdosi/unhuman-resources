import tornado.ioloop
import tornado.web
import requests

import replace, get

newAddress = "lidovki.cz:8080"
originalAddress = "www.lidovky.cz"

class AllHandler(tornado.web.RequestHandler):
    def get(self):
        url = "http://" + originalAddress + self.request.uri
        page = get.getPage(url)

        page = replace.replaceLinks(page, originalAddress, newAddress)
        page = replace.replaceBabis(page)
        page = replace.replaceANO(page)

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
    print("Server has started!")
    tornado.ioloop.IOLoop.current().start()
