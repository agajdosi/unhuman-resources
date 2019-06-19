import argparse

import tornado.ioloop
import tornado.web
import requests
import tldextract

import get

#newDomain = "ydnes.cz"
newDomain = "localhost:8080"
origDomain = "idnes.cz"

class AllHandler(tornado.web.RequestHandler):
    def get(self):
        headers = {"User-Agent" : self.request.headers.get("User-Agent")}

        if args.debug == True:
            print("access from:", self.request, headers)
        
        reqURI = self.request.full_url()
        uri = tldextract.extract(reqURI)

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
    parser.add_argument("--original", "-o", help="original address of server from which pages will be downloaded", type=str, default="idnes.cz")
    parser.add_argument("--new", "-n", help="address of new fake edited server", type=str, default="localhost:8080")
    parser.add_argument("--debug", "-d", help="debug mode - print out who access the server", type=bool, default=False)
    args = parser.parse_args()
    
    origDomain = args.original
    newDomain = args.new

    app = make_app()
    app.listen(args.port)
    tornado.ioloop.IOLoop.current().start()
