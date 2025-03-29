# CDN

from flask import Flask, render_template, Response, send_file, current_app, request, make_response
from flask.logging import default_handler
from jinja2 import Environment, FileSystemLoader
from datetime import datetime
from werkzeug.utils import secure_filename
from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
import etc.etc.security.cxi as cxi
import etc.etc.handler as handler
import etc.net.net as net
import os
import sys
import cv2
import re
import mimetypes
import timeago, time
import random
import string

if sys.platform == 'win32':
   os.system('cls')
else:
   os.system('clear')

os.chdir(os.path.dirname(os.path.abspath(__file__)))

camera = cv2.VideoCapture(0)
errs = None
debug = True

def random_str(length, st='chars'):
    try:
        strc = None
        if st == 'chars':
            strc = string.ascii_letters
        elif st == 'digits':
            strc = string.digits
        result_str = ''.join(random.choice(strc) for i in range(length))
        return (result_str)
    except:
        return None

def _time(dt):
    dtm = datetime.strptime(dt, "%d/%m/%Y")
    now = datetime.now()
    dt = timeago.format(now, dtm, 'en_short')
    dt = dt.replace('in ', '')
    if "mo" in dt:
        dt = dtm.strftime("%d %b")
    return dt

def _path(f):
    try:
        if os.path.exists("./"+f) == True:
            return True
        else:
            return False
    except:
        return False

def gen_frames():  # generate frame by frame from camera
    while True:
        # Capture frame-by-frame
        success, frame = camera.read()  # read the camera frame
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

# €Server
app = None
try:
    app = Flask(__name__, template_folder="./", static_folder="et/")
    app.logger.removeHandler(default_handler)
    try:
#       €Configuration
        app.config.from_pyfile('et/net/config/config.py')
        app.config['SECRET_KEY'] = cxi.encrypt(random_str(12))
    except Exception as err:
        errs = (err)
        pass

except Exception as err:
    errs = (err)
    pass

@app.errorhandler(403)
def access_denied(e):
    # 403 status set explicitly
    return render_template('et/etc/err_pages/403.asp'), 403

@app.errorhandler(404)
def page_not_found(e):
    # 404 status set explicitly
    return render_template('et/etc/err_pages/404.asp'), 404

@app.errorhandler(500)
def internal_server_error(e):
    # 500 status set explicitly
    return render_template('et/etc/err_pages/500.asp'), 500


@app.after_request
def after_request(response):
    response.headers["Expires"] = 1
    return response

@app.route('/')
def index():
    return "Access to this site is restricted", 403

@app.route('/path', methods = ['GET'])
def path():
    file = request.args.get('filename')
    type = request.args.get('type')
    gen = request.args.get('gen')
    _id = request.args.get('id')
    if type == "image":
        path = "./et/uploads/users/{}/{}/images/{}".format(_id, gen, file)
    path = request.args.get("path")
    img_path = ""+path.replace("cxit2", "/")
    if _path(img_path) == True:
        return True
    else:
        return False

@app.route('/upload', methods = ['GET', 'POST'])
def upload():
    q = request.args.get('q')
    if q == "upload":
        f = request.files['file']
        f.save(app.config['UPLOAD_FOLDER'] + secure_filename(f.filename))

@app.route("/image", methods=["GET"])
def image():
    uuid = request.args.get("uuid")
    ppic = request.args.get("ppic")
    ptp = request.args.get("ptp")
    path = None
    if ptp == "profile":
        path = "uploads/users/{}/profiles/{}".format(uuid, ppic)
    if ptp == "story":
        path = "uploads/users/{}/stories/images/{}".format(uuid, ppic)
    if ptp == "post":
        path = "uploads/users/{}/posts/images/{}".format(uuid, ppic)
    img_path = "./et/" + path
    try:
        return send_file(img_path)
    except:
        return send_file("./et/uploads/defaults/imgerr.jpg")

@app.route("/script/all", methods=['GET', 'POST'])
def allscripts():
    userAgent = request.args.get("c")
    if userAgent == "Ceera.1.0 (Android >=8.0)":
        ph = "ext/scripts/000.asp"
        env = Environment(loader=FileSystemLoader("et"))
        t = env.get_template(ph)
        return t.render()
    else:
        return "error", 500

@app.route("/script", methods=["GET"])
def script():
    n = request.args.get("n")
    if n == "swipeEvent":
        path = "./et/ext/scripts/002.js"
    else:
        path = "etc/int/err_pages/403.asp"
    try:
        return send_file(path)
    except:
        return ""

@app.route("/style", methods=["GET"])
def style():
    s = request.args.get("s")
    s_path = "./et/ext/styles/" + s
    sn = secure_filename(s_path)
    try:
        with open(s_path) as f:
            st = f.read()
            print("Getting style")
            return st
    except:
        return ""

@app.route("/video", methods=["GET", 'POST'])
def video():
    headers = request.headers
    if not "range" in headers:
        return make_response("", 400)
    uuid = request.args.get("uuid")
    ppic = request.args.get("ppic")
    ptp = request.args.get("ptp")
    path = None
    if ptp == "profile":
        path = "uploads/users/{}/profiles/{}".format(uuid, ppic)
    if ptp == "story":
        path = "uploads/users/{}/stories/videos/{}".format(uuid, ppic)
    if ptp == "post":
        path = "uploads/users/{}/posts/videos/{}".format(uuid, ppic)
    video_path = "./et/" + path
    size = os.stat(video_path)
    size = size.st_size
    chunk_size = 10**3
    start = int(re.sub("\D", "", headers["range"]))
    end = min(start + chunk_size, size - 1)
    content_lenght = end - start + 1
    def get_chunk(video_path, start, end):
        with open(video_path, "rb") as f:
            f.seek(start)
            chunk = f.read(end)
        return chunk
    headers = {
        "Content-Range": f"bytes {start}-{end}/{size}",
        "Accept-Ranges": "bytes",
        "Content-Length": content_lenght,
        "Content-Type": "video/mp4"
    }
    return current_app.response_class(get_chunk(video_path, start, end), 206, headers, direct_passthrough=True, mimetype=mimetypes.guess_type(video_path)[0])

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/turbo-stream')
def stream():
    return 'ok'

@app.route('/robots.txt')
def noindex():
    return ""

@app.route('/favicon.ico')
def favicon():
    return ("et/theme/icons/icon.ng")

@app.route('/serverhealth')
def serverhealth():
    return "ok"

if __name__=='__main__':
    addr = net.get_ip()
    port = 80
    if errs != None:
        print(f' errors: ' + str(errs))
    try:
        server = HTTPServer(WSGIContainer(app))
        # €Start server
        print(f'• SERVER: CDN')
        time.sleep(1)
        print(f'• Ip: ' + addr)
        time.sleep(1)
        print(f'• Debug: ' + str(debug))
        time.sleep(1)
        if errs == None:
            print("••Online")
            server.listen(port=port)
            IOLoop.instance().start()
    # Show errors if server can't start
    except KeyboardInterrupt:
        print('• Server Stopped')
        handler.erreport(app)
else:
    print("Server error")
