from tornado.websocket import WebSocketHandler
import tornado
import logging
import re
from logging.handlers import SMTPHandler

class ChatHandler(WebSocketHandler):  #creating our main websocket class
    waiters = set()  #set number of joinable users
    cache = []
    cache_size = 200

    def get_compression_options(self):
        #non-none enables compression with default options.
        return {}

    def open(self):  #accepts a connection request and stores the parameters, a socket object for that user
        ChatSocketHandler.waiters.add(self)

    def on_close(self):  #removes the user by removing the object
        ChatSocketHandler.waiters.remove(self)

    @classmethod 
    def update_cache(cls, chat):  #Maintains a list of chat for broadcasting the messages
        cls.cache.append(chat)
        if len(cls.cache) > cls.cache_size:
            cls.cache = cls.cache[-cls.cache_size :]

    @classmethod 
    def send_updates(cls, chat):  #mange sending messages
        logging.info("sending message to %d users", len(cls.waiters))
        for waiter in cls.waiters:
            try:
                waiter.write_message(chat)  #outputting the messages
            except:  #except, in case of any errors
                logging.error("Error sending message", exc_info=True)

    def on_message(self, message):
        logging.info("got message %r", message)
        parsed = tornado.escape.json_decode(message)
        chat = {"id": str(uuid.uuid4()), "body": parsed["body"]}
        chat["html"] = tornado.escape.to_basestring(
            self.render_string("int/chat.html", message=chat)
        )

        ChatHandler.update_cache(chat)
        ChatHandler.send_updates(chat)

def erreport(app):
    mail_handler = SMTPHandler(
       mailhost='http://127.0.0.1',
       fromaddr = 'server.errs@dnx.com',
       toaddrs = ['asherlitaunyane@gmail.com'],
       subject = 'Server Error')
    mail_handler.setLevel(logging.ERROR)
    mail_handler.setFormatter(logging.Formatter('[%(asctime)s] %(levelname)s in %(module)s: %(message)s'))
    if not app.debug:
        app.logger.addHandler(mail_handler)

class GoogleAccAuth(tornado.web.RequestHandler):
    async def get(self):
        if self.get_argument('code', False):
            user = await self.get_authenticated_user(
                redirect_uri='http://127.0.0.1:8080/',
                code=self.get_argument('code'))
            # Save the user with e.g. set_secure_cookie
        else:
            await self.authorize_redirect(
                redirect_uri='http://127.0.0.1:8080/',
                client_id=self.settings['google_oauth']['key'],
                scope=['profile', 'email'],
                response_type='code',
                extra_params={'approval_prompt': 'auto'})

class Text:
    def _corr(text):
        return None
    def _tags(regex, text):
        tag_list = re.findall(regex, text)
        for tag in tag_list:
            return tag

