# -*- coding: utf-8 -*-
# author:pross


import web

urls = ('/dispatch', 'handle')


if __name__ == '__main__':
    app = web.application(urls, globals())
    app.run()

