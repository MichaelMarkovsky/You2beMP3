from flask import Flask, render_template, request, Response
from download import download_song
from link_check import link_check

app = Flask(__name__)

def generate_download_logs(link):
    """Generate logs during song download"""
    if link_check(link):  # Only proceed if the link is valid
        for message in download_song(link):
            yield f"data: {message}\n\n"
    else:
        yield "data: Invalid YouTube link.\n\n"  # If the link is invalid, return an error message

@app.route('/', methods=["GET", "POST"])
def index():
    """Main route to handle form submission and streaming download logs"""
    if request.method == "POST":
        youtube_link = request.form['link']

        if link_check(youtube_link):  # Valid link
            return render_template('index.html', link=youtube_link, error=None)
        else:  # Invalid link
            return render_template('index.html', link=None, error="Invalid YouTube link.")

    return render_template('index.html', link=None, error=None)  # GET request

@app.route('/stream')
def stream_download():
    """SSE route to stream download logs"""
    link = request.args.get('link')
    if not link:
        return "No link provided", 400  # Return error if no link is provided

    if link_check(link):  # Check if the link is valid before proceeding
        return Response(generate_download_logs(link), mimetype='text/event-stream')
    else:
        return Response("data: Invalid link. Download cannot start.\n\n", mimetype='text/event-stream')

if __name__ == "__main__":
    app.run(debug=True)
