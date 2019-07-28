import tornado.ioloop
import tornado.web
import tldextract
import time

import get
import settings
import statistics

newDomain = ""
origDomain = ""

class AllHandler(tornado.web.RequestHandler):
    async def get(self):
        print("access")
        newDomain = ""
        origDomain = ""
        headers = {"User-Agent" : self.request.headers.get("User-Agent")}
        
        start = time.time()
        statistics.countVisitor(self)
        print("stats took", time.time() - start)

        start = time.time()
        reqURI = self.request.full_url()
        uri = tldextract.extract(reqURI)

        if settings.args.ssl == True and self.request.protocol == "http":
            dest = "https://"
            if uri.subdomain != "":
                dest += uri.subdomain + "."
            dest += uri.domain
            if uri.domain != "":
                dest += "." + uri.suffix
            dest += self.request.path
            self.redirect(dest, permanent=False)
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

        print("domain shits took", time.time() - start)

        page = await get.getPage(url, origDomain, newDomain, headers)
        print("page served")
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
