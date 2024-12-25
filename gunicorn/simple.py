def application(environ, start_response):
    status = '200 OK'
    response_headers = [('Content-type', 'text/html')]
    start_response(status, response_headers)

    query_string = environ['QUERY_STRING']
    post_data = environ['wsgi.input'].read(int(environ.get('CONTENT_LENGTH', 0)))

    body = f"""
    <html>
    <body>
        <h1>Query Parameters</h1>
        <p>GET: {query_string}</p>
        <p>POST: {post_data.decode('utf-8')}</p>
    </body>
    </html>
    """
    return [body.encode('utf-8')]