import tornado.ioloop
import tornado.web
import requests
import tldextract

import get
import settings
import statistics

newDomain = ""
origDomain = ""

class AllHandler(tornado.web.RequestHandler):
    def get(self):
        newDomain = ""
        origDomain = ""
        headers = {"User-Agent" : self.request.headers.get("User-Agent")}
        
        if settings.args.debug == True:
            print("access from:", self.request, headers)
        else:
            statistics.countVisitor(self)

        reqURI = self.request.full_url()
        uri = tldextract.extract(reqURI)

        if settings.args.ssl == True and self.request.protocol == "http":
            self.redirect("https://" + uri.subdomain + uri.domain + "." + uri.suffix + self.request.path, permanent=False)
            return

        for server in settings.args.servers:
            requestedDomain = uri.domain + "." + uri.suffix
            new, original = server.split("=") #handle if contains two == or zero =
            if "localhost" in new:
                newDomain = new + ":" + str(settings.args.port)
                origDomain = original
            elif requestedDomain == new:
                newDomain = new
                origDomain = original

        if uri.subdomain != "":
            url = "https://" + uri.subdomain + "." + origDomain + self.request.path
        else:
            url = "https://" + origDomain + self.request.path

        page = get.getPage(url, origDomain, newDomain, headers)
        self.write(page)

def make_app():
    return tornado.web.Application([
        (r'/(robots\.txt)', tornado.web.StaticFileHandler, {'path' : 'static'}),
        (r".*", AllHandler),
    ],
    debug = settings.args.debug
    )

if __name__ == "__main__":
    settings.init()

    app = make_app()
    app.listen(settings.args.port)

    if settings.args.ssl == True:
        app.listen(443, ssl_options={
            "certfile": "/etc/letsencrypt/live/l-dnes.cz/cert.pem",
            "keyfile": "/etc/letsencrypt/live/l-dnes.cz/privkey.pem",
        })

    tornado.ioloop.IOLoop.current().start()
