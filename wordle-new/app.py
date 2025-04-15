from flask import Flask, request, jsonify, render_template
import re

app = Flask(__name__)

wordList = []
with open("enable1.txt") as f:
    for line in f:
        if len(line.strip()) == 5:
            wordList.append(line.strip())

@app.route("/")
def mainpage():
    return render_template("main.html")

@app.route('/fetch')
def fetchpage():
    data = request.args.get("letters")
    return jsonify({"letters": data.lower()})

@app.route('/solver/<greyLetters>/<yellowLetters>/<yellowPos>/<greenLetters>')
def solve_wordle(greyLetters, yellowLetters, yellowPos, greenLetters):

    if greenLetters == "none":
        greenLetters = ""
    if yellowLetters == "none":
        yellowLetters = ""
    if yellowPos == "none":
        yellowPos = ""
    if greyLetters == "none":
        greyLetters = ""

    pattern_parts = []

    for letter in greyLetters:
        pattern_parts.append(f"(?!.*{letter})")

    for idx, letter in enumerate(yellowLetters):
        pattern_parts.append(f"(?=.*{letter})")
        if len(yellowPos) > idx:
            pattern_parts.append(f"(?!{'*' * int(yellowPos[idx])}{letter})")

    if greenLetters:
        pattern_parts.append(f"^{greenLetters}$")

    final_pattern = ''.join(pattern_parts)

    regex = re.compile(final_pattern)

    filtered_words = []
    for word in wordList:
        if regex.match(word):
            filtered_words.append(word)
    
    return jsonify(filtered_words)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
