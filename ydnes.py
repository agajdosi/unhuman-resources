import tornado.ioloop
import tornado.web
import requests
import get
import tldextract

#newDomain = "ydnes.cz"
newDomain = "localhost:8080"
origDomain = "idnes.cz"

class AllHandler(tornado.web.RequestHandler):
    def get(self):
        reqURI = self.request.full_url()
        uri = tldextract.extract(reqURI)

        if uri.subdomain != "":
            url = "http://" + uri.subdomain + "." + origDomain + self.request.path
        else:
            url = "http://" + origDomain + self.request.path

        page = get.getPage(url, origDomain, newDomain)
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
