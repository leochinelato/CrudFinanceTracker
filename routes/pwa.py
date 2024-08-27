from flask import Blueprint, send_file

pwa_route = Blueprint("pwa", __name__)


@pwa_route.route("/manifest.json")
def serve_manifest():
    return send_file('manifest.json', mimetype='application/manifest+json')


@pwa_route.route('/sw.js')
def serve_sw():
    return send_file('sw.js', mimetype='application/javascript')
