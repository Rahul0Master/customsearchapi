from flask import Flask, request, jsonify
from search import search
from storage import DBStorage
from filter import Filter
import html

app = Flask(__name__)

styles = """
<style>
    #search-bar{
        display:ruby-text;
        margin-bottom: 40px;
    }
    #result{
        display: flex;
        justify-content: space-between;
    }
    #search{
        width:250px;
        border-radius: 8px;
    }
    #search:hover{
        border: 2px solid #4D61EA
    }
    #search:focus{
        
        border-color:#0e3131
    }
    #btn{
        background-color: #4D61EA;
        color: white;
        border: 0px;
        border-radius: 25px;
        height: 22px;
    }
    #btn:hover{
        cursor: pointer;
    }
    .site {
        font-size: .9rem;
        color: green;
        display: flex;
        justify-content: space-between;
        margin-left: 50px;
        margin-right: 25px;
    }
    
    .snippet {
        font-size: .9rem;
        color: gray;
        margin-bottom: 30px;
        margin-left: 50px;
    }
    
    .rel-button {
        cursor: pointer;
        color: blue;
    }
</style>
<script>
const relevant = function(query, link){
    fetch("/relevant", {
        method: 'POST',
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
           "query": query,
           "link": link
          })
        });
}
</script>
"""

search_template = styles + """
    <div id="search-bar">
        <h3>Google Search API</h3><br>
        <form action="/" method="post">
        <input id="search" type="text" placeholder="Enter search query" name="query">
        <input id="btn" type="submit" value="Test Search">
        </form>
    </div>
    """

result_template = """
    
        <p class="site">{rank}: {link}<span class="rel-button" onclick='relevant("{query}", "{link}");'><a href="{link}">{title}</a></p>
        
"""

def show_search_form():
    return search_template

def run_search(query):
    results = search(query)
    fi = Filter(results)
    filtered = fi.filter()
    rendered = search_template
    for index, row in filtered.iterrows():
        rendered += result_template.format(**row)
    return rendered

@app.route("/", methods=['GET', 'POST'])
def search_form():
    if request.method == 'POST':
        query = request.form["query"]
        return run_search(query)
    else:
        return show_search_form()

# @app.route("/relevant", methods=["POST"])
# def mark_relevant():
#     data = request.get_json()
#     query = data["query"]
#     link = data["link"]
#     storage = DBStorage()
#     storage.update_relevance(query, link, 10)
#     return jsonify(success=True)