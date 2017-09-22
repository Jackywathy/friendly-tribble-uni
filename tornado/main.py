import tornado.ioloop
import tornado.web
import tornado.log
import tornado

class MainHandler(tornado.web.RequestHandler):
    def get(self, *args):
        self.write("Hello, world{}".format("" if not args else " from" + str(args)))
        tornado.log.app_log("404 GET /{}".format(args))


if __name__ == "__main__":
    application = tornado.web.Application([
        (r"/", MainHandler),
        (r"/(.*)", MainHandler)
    ], autoreload=True)

    application.listen(8888)
    tornado.ioloop.IOLoop.current().start()