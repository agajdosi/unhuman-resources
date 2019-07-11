import argparse

import tornado.ioloop
import tornado.web
import requests
import tldextract

import get

newDomain = ""
origDomain = ""

class AllHandler(tornado.web.RequestHandler):
    def get(self):
        newDomain = ""
        origDomain = ""
        headers = {"User-Agent" : self.request.headers.get("User-Agent")}

        if args.debug == True:
            print("access from:", self.request, headers)
        
        reqURI = self.request.full_url()
        uri = tldextract.extract(reqURI)

        for server in args.servers:
            requestedDomain = uri.domain + "." + uri.suffix
            new, original = server.split("=") #handle if contains two == or zero =
            if "localhost" in new:
                newDomain = new + ":" + str(args.port)
                origDomain = original
            elif requestedDomain == new:
                newDomain = new
                origDomain = original

        if uri.subdomain != "":
            url = "http://" + uri.subdomain + "." + origDomain + self.request.path
        else:
            url = "http://" + origDomain + self.request.path

        page = get.getPage(url, origDomain, newDomain, headers)
        self.write(page)

def make_app():
    return tornado.web.Application([
        (r'/(robots\.txt)', tornado.web.StaticFileHandler, {'path' : 'static'}),
        (r".*", AllHandler),
    ],
    debug = args.debug
    )

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", "-p", help="defines which port will be used by webserver", type=int, default=8080)
    parser.add_argument("--debug", "-d", help="debug mode - print out who access the server", type=bool, default=False)
    parser.add_argument("--servers", "-s", help="list of pairs joined with =, for example mockbook.com=facebook.com, first in the pair is the address of new modified server, the second is the address of original server. Default values is: localhost=idnes.cz", nargs="+", type=str, default=["localhost=idnes.cz"])
    args = parser.parse_args()

    app = make_app()
    app.listen(args.port)
    tornado.ioloop.IOLoop.current().start()
