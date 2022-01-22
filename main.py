import json
import time
import urllib.parse
import argparse
from http.server import HTTPServer, BaseHTTPRequestHandler


class PaulusHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Type", "text/html")
        self.end_headers()
        self.wfile.write(form_html(args.questions).encode("utf-8"))

    def do_POST(self):
        content_length = int(self.headers.get("Content-Length"))
        body = self.rfile.read(content_length).decode("utf-8")
        form_data = parse_form_data(body)
        with open(args.output, "a") as file:
            file.write(json.dumps(form_data) + "\n")
        self.send_response(200)
        self.end_headers()
        self.wfile.write("Merci!".encode("utf-8"))


def run():
    server_address = ('', args.port)
    httpd = HTTPServer(server_address, PaulusHandler)
    httpd.serve_forever()


def parse_args():
    parser = argparse.ArgumentParser(description="Paulus")
    parser.add_argument(
        '--port', type=int,
        default=8000,
        help="Port to start the server on"
    )
    parser.add_argument(
        '--questions',
        type=str,
        default="questions.txt",
        help="File that contains newline-separated questions"
    )
    parser.add_argument(
        '--output',
        type=str,
        default="paulus.json",
        help="File to append poll data to"
    )
    return parser.parse_args()


def parse_form_data(string):
    form_data = {"time": int(time.time())}
    for line in string.split("&"):
        [key, val] = line.split("=")
        parsed_key = urllib.parse.unquote_plus(key).strip()
        parsed_val = urllib.parse.unquote_plus(val).strip()
        form_data[parsed_key] = parsed_val
    return form_data


def form_html(questions_file):
    questions = []
    with open(questions_file, "r") as file:
        questions = file.readlines()
    questions_html = ""
    for question in questions:
        questions_html += f"""
            <div class="form-question">
              <label for="{question}">{question}</label>
              <div>
                <input type="checkbox" name="{question}" id="{question}"/>
              </div>
            </div>
        """
    style = """
      .form-question {
        display: flex;
        width: 100%;
        padding-bottom: 0.5em;
      }

      .form-question > * {
        display: block;
        width: 50%;
      }

      .form-question > label {
        text-align: right;
        margin-right: 10px;
      }

      input[type=submit] {
        position: relative;
        left: 50%;
      }
    """
    message = f"""
      <!DOCTYPE html>
      <html>
        <head>
          <title>Paulus</title>
        </head>
        <body>
          <h1>Paulus</h1>
          <form action="" method="post">
            {questions_html}

            <div class="form-question">
              <label for="comment">comment</label>
              <textarea name="comment" id="comment"></textarea>
            </div>

            <input type="submit" value="Submit" />
          </form>
          <style>
            {style}
          </style>
        </body>
      </html>
    """
    return message


if __name__ == "__main__":
    args = parse_args()
    run()
