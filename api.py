import falcon

class ThingsResource(object):
    def on_post(self, req, resp):
        value = req.get_param("value", required=True)
        print("Test")

app = falcon.API()
app.req_options.auto_parse_form_urlencoded=True

app.add_route('/things', ThingsResource())