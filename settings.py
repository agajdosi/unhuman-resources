import argparse

def init():
    global args
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", "-p", help="defines which port will be used by webserver for http", type=int, default=8080)
    parser.add_argument("--debug", "-d", help="debug mode - print out who access the server", type=bool, default=False)
    parser.add_argument("--ssl", help="enable ssl so https is available on port 443", type=bool, default=False)
    parser.add_argument("--servers", "-s", help="list of pairs joined with =, for example mockbook.com=facebook.com, first in the pair is the address of new modified server, the second is the address of original server. Default values is: localhost=idnes.cz", nargs="+", type=str, default=["localhost=idnes.cz"])
    args = parser.parse_args()
