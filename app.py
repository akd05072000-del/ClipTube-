from flask import Flask, request, send_file, render_template, jsonify
import subprocess
import os
import uuid

app = Flask(__name__)

# जब कोई आपकी वेबसाइट खोलेगा तो यह पेज दिखेगा
@app.route('/')
def index():
    return render_template('index.html')

# यह API वीडियो को प्रोसेस करेगी
@app.route('/download', methods=['POST'])
def download():
    data = request.json
    url = data.get('url')
    start_time = data.get('start') # उदाहरण: "00:01:10"
    end_time = data.get('end')     # उदाहरण: "00:01:40"

    if not url or not start_time or not end_time:
        return jsonify({"error": "लिंक और समय देना जरूरी है"}), 400

    # एक यूनीक फाइल का नाम बनाना ताकि फाइलें आपस में मिक्स न हों
    output_file = f"clip_{uuid.uuid4().hex}.mp4"

    # yt-dlp की कमांड जो *बिना पूरी वीडियो डाउनलोड किए* सिर्फ हिस्सा निकालेगी
    command =[
        'yt-dlp',
        '--download-sections', f"*{start_time}-{end_time}",
        '--force-keyframes-at-cuts',
        '-f', 'best[ext=mp4]',
        '-o', output_file,
        url
    ]

    try:
        # कमांड रन करना
        subprocess.run(command, check=True)
        
        # यूज़र को कटी हुई वीडियो फाइल भेजना
        response = send_file(output_file, as_attachment=True)
        return response
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # ऐप को रन करना
    app.run(host='0.0.0.0', port=8080)
