from flask import Flask, render_template, request
import webbrowser
import questionary
from googlesearch import search

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        topic = request.form["topic"]
        wikipedia_url = search_topic(topic)
        if wikipedia_url:
            open_wikipedia_page(wikipedia_url)
            return render_template("index.html")
    return render_template("index.html")

def search_topic(topic):
    query = topic + " wikipedia"
    for url in search(query, num_results=5):
        if 'wikipedia.org' in url:
            return url
    return None

def open_wikipedia_page(url):
    webbrowser.open_new_tab(url)

def ask_question(topic):
    question = questionary.text("Enter your question about {}:".format(topic)).ask()
    query = topic + " " + question
    for url in search(query, num_results=5):
        if 'wikipedia.org' not in url:
            return url
    return None

def main():
    topic = questionary.text("Enter a topic:").ask()
    wikipedia_url = search_topic(topic)
    if wikipedia_url:
        open_wikipedia_page(wikipedia_url)
        while True:
            ask_more = questionary.confirm("Do you have another question about {}?".format(topic)).ask()
            if ask_more:
                search_url = ask_question(topic)
                if search_url:
                    open_wikipedia_page(search_url)
                else:
                    print("Sorry, I couldn't find information related to your question.")
            else:
                break
    else:
        print("Sorry, I couldn't find information about the topic.")

if __name__ == "__main__":
    main()