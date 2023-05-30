from flask import Flask, render_template, request
from video_comments import video_comments
from summarize import summarize
from word_freq import WordFreq

app = Flask(__name__, template_folder="templates", static_folder="static")


@app.route('/refresh', methods=["POST"])
def refresh_page():
    return render_template("index.html")


@app.route('/')
def hello_world():
    return render_template("index.html")


@app.route('/process-form', methods=["POST"])
def process_form():
    video_link = request.form['link']
    num_sent = request.form['num_sent']
    num_word = request.form['num_word']

    if num_sent.isdigit():  # Check if num_sent is a valid non-negative integer
        num_sent = int(num_sent)
    else:
        data = {"status": 0}
        return render_template("index.html", data=data)

    if len(video_link) == 0:
        data = {"status": 0}
    else:   
        vc = video_comments()
        video_id = vc.get_video_id(video_link)
        comments = vc.get_comments(video_id)
        count = vc.count
        sum = summarize(n=num_sent)
        extractive_summary = sum.extractive(comments)
        abstractive_summary = sum.abstractive()
        data = {"status": 1, 'video_id': video_id, 'extractive': extractive_summary, 'abstractive': abstractive_summary, 'count': count}

        # Generate word cloud
        word_freq = WordFreq()
        text = extractive_summary
        image_path = word_freq.generate_word_cloud(text, int(num_word))

    return render_template("index.html", data=data, word_freq=image_path)


if __name__ == "__main__":
    app.run(debug=True)
