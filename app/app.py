from platform import version
from flask import Flask

# print a nice greeting.
def say_hello(username = "World"):
    return '<p>Hello %s!</p>\n' % username

# some bits of text for the page.
header_text = '''
    <html>\n<head> <title>EB Flask Test</title> </head>\n<body>'''
instructions = '''
    <p>No entries here so far</p>\n'''
home_link = '<p><a href="/">Back</a></p>\n'
footer_text = '</body>\n</html>'

def create_app(test_config=None):
    application = Flask(__name__)
    if test_config:
        application.config.update(test_config)

    application.add_url_rule('/', 'index', (lambda: header_text +
        say_hello() + instructions + footer_text))
    
    application.add_url_rule("/health", "health", lambda: "healthy")

    application.add_url_rule('/<username>', 'hello', (lambda username:
        header_text + say_hello(username) + home_link + footer_text))
    return application

    
if __name__ == "__main__":
    application = create_app()
    application.run()