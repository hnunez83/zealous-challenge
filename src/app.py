from flask import Flask, request, render_template_string
import datetime

app = Flask(__name__)

html_template = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Color Background</title>
    <style>
        body {
            background-color: {{ color }};
            color: #fff;
            font-family: Arial, sans-serif;
            text-align: center;
            padding: 50px;
        }
    </style>
</head>
<body>
    <h1>Hello, World!</h1>
    <p>The current background color is <strong>{{ color }}</strong>.</p>
    <p>The current time in Armenia : <strong>{{ armenia_time }}</strong>.</p>
    <form method="post">
        <label for="color">Choose a color:</label>
        <select name="color" id="color">
            {% for option in colors %}
            <option value="{{ option }}" {% if option == color %}selected{% endif %}>{{ option }}</option>
            {% endfor %}
        </select>
        <button type="submit">Change Color</button>
    </form>
</body>
</html>
'''

@app.route("/", methods=["GET", "POST"])
def hello_world():
    colors = ["red", "blue", "green", "yellow", "purple", "orange"]
    color = "blue"  # Default color
    if request.method == "POST":
        color = request.form.get("color", "blue")

    # Calculate the current time in Armenia (UTC+4)
    armenia_time = (datetime.datetime.utcnow() + datetime.timedelta(hours=4)).strftime("%Y-%m-%d %H:%M:%S")

    return render_template_string(html_template, color=color, colors=colors, armenia_time=armenia_time)

@app.route("/health", methods=["GET"])
def health_check():
    return "OK", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
