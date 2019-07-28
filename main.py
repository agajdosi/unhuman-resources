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
    def write_error(self, status_code, **kwargs):
        self.finish("""
        <html style="font-size:2em;color:white;"><title>Určitě bude líp</title>
        <link href="https://fonts.googleapis.com/css?family=Work+Sans&display=swap" rel="stylesheet"> 
        <body style="background:url(error.jpg) no-repeat center center fixed;background-size:cover;font-family: 'Work Sans', sans-serif;">
        <div style="max-width:80vw;margin-left: auto;margin-right: auto;margin-top:7vh;">
            <div><span style="font-size:2em;background:black;">Ano, něco se pokazilo:</span></div>
            <div style="margin-bottom: 50px;"><span style="background:black;">%(message)s (%(code)s)</span></div>
            <div><a href="/" style="background:white;color:black;">zkusme to znovu</a></div>
        </div>
        </body></html>
        """ % {
                "code": str(status_code).lower(),
                "message": self._reason.lower(),
            })

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
        (r'/(robots\.txt|error\.jpg)', tornado.web.StaticFileHandler, {'path' : 'static'}),
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
