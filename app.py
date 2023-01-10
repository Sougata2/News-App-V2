from flask import Flask, request, render_template
import requests

app = Flask(__name__)
category = 'top'
page_no = 0


@app.route('/', methods=["GET", "POST"])
def index():
    global category, page_no
    if request.method == 'POST':
        if request.form.get("category_name") is not None \
                and request.form.get("previous_page") is None \
                and request.form.get("next_page") is None:
            page_no = 0
        category = category if request.form.get("category_name") is None else request.form.get("category_name")
        go_prev = request.form.get('previous_page')
        go_next = request.form.get('next_page')
        if go_prev is not None:
            page_no -= 1
        if go_next is not None:
            page_no += 1
        print(category, go_prev, go_next)
    print(page_no)
    url = f'https://newsdata.io/api/1/news?apikey=pub_15486def9a8a909c70f2f8395b1b5d6d7cea7&' \
          f'country=in&category={category}&' \
          f'language=en&' \
          f'page={page_no}'
    response = requests.get(url).json()
    if response["status"] == "error":
        return render_template('error.html', results=response["results"])
    print(response)
    print(response["totalResults"])
    total_pages = (response["totalResults"] // 10) if response["totalResults"] % 10 > 0 \
        else (response["totalResults"] // 10) - 1
    prev_possible = True
    next_possible = True
    if page_no >= total_pages:
        next_possible = False
    if page_no == 0:
        prev_possible = False
    results = response["results"]
    return render_template('index.html', category=category.title(), results=results, page_no=page_no + 1, prev_possible=prev_possible,
                           next_possible=next_possible)


if __name__ == '__main__':
    app.run()
