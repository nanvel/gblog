import traceback

from tornado.web import RequestHandler


class GBlogHandler(RequestHandler):

    def write_error(self, status_code, **kwargs):
        """Override to implement custom error pages.

        ``write_error`` may call `write`, `render`, `set_header`, etc
        to produce output as usual.

        If this error was caused by an uncaught exception (including
        HTTPError), an ``exc_info`` triple will be available as
        ``kwargs["exc_info"]``.  Note that this exception may not be
        the "current" exception for purposes of methods like
        ``sys.exc_info()`` or ``traceback.format_exc``.
        """
        if self.settings.get("serve_traceback") and "exc_info" in kwargs:
            # in debug mode, try to send a traceback
            self.set_header('Content-Type', 'text/plain')
            for line in traceback.format_exception(*kwargs["exc_info"]):
                self.write(line)
            self.finish()
        else:
            self.finish("""<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="utf-8">
        <title>{message}</title>
        <style>
            body {{
                margin: 0;
                padding: 0;
                background-color: #222;
            }}
            .content {{
                position: absolute;
                top: 50%;
                color: #fff;
                text-align: center;
                height: 4em;
                margin-top: -2em;
                width: 100%;
                font-size: 2em;
            }}
            #redirect-message {{
                display: none;
                font-size: .8em;
            }}
            #redirect-message > span {{
                color: #ffc40d;
            }}
        </style>
    </head>
    <body>
        <div class="content">
            {code}: {message}
            <div id="redirect-message">You'll be redirected to index page in <span id="redirect-seconds">10</span> seconds.</div>
        </div>
        <script>
            var page = {{
                index_url: '/',
                seconds: 11,
                redirect_message: document.getElementById('redirect-message'),
                redirect_seconds: document.getElementById('redirect-seconds'),
                dec_seconds: function() {{
                    page.seconds-=1;
                    page.redirect_seconds.innerHTML=page.seconds;
                    if(page.seconds>0) {{
                        setTimeout(page.dec_seconds, 1000);
                    }} else {{
                        window.location.href=page.index_url;
                    }}
                }},
                init: function() {{
                    if(window.location.pathname!=page.index_url) {{
                        page.redirect_message.style.display='block';
                        page.dec_seconds();
                    }}
                }}
            }};
            page.init();
        </script>
    </body>
</html>""".format(code=status_code, message=self._reason))
