from flask import Flask, redirect, url_for, request, render_template
from elisalib import searchProcedure, retrieveSentences, assetToHTMLTable
app = Flask(__name__)


@app.route('/hello/<user>')
def hello_name(user):
   return render_template('hello.html', name = user)

@app.route('/')
def index():
	#url = "http://52.166.193.245:1403/search"
	url = "http://localhost:5000/search"
	
	return render_template('searchform.html', search_url = url)
	
@app.route('/search',methods = ['POST', 'GET'])
def login():
	if request.method == 'POST':
		kword = request.form['keyword']
		return redirect(url_for('keyword_search',keyword = kword))
	else:
		kword = request.args.get('keyword')
		return redirect(url_for('keyword_search',keyword = kword))

		
@app.route('/search/<keyword>')
def keyword_search(keyword):
	#sentenceList, qnaList = retrieveSentencesContainingWordInFullJSON('data_sent_year_new.json', 'fiber')
	sentenceHTMLTable, keys, vals_neg, vals_pos, emotionHTMLTable = searchProcedure(keyword, True)
	return render_template('searchresults.html', word = keyword, table = sentenceHTMLTable, quartiles = keys, neg_results = vals_neg, pos_results = vals_pos, emotionTable = emotionHTMLTable)

@app.route('/asset/<specs>')
def retrieve_assets(specs):
	keyword, company, yearQuartile = specs.split("_")
	sentencesFound = retrieveSentences(keyword, company, yearQuartile) 
	print sentencesFound
	return render_template('asset.html', html_keyword = keyword, html_yearQuartile = yearQuartile, html_company = company, html_content = assetToHTMLTable(sentencesFound))

if __name__ == '__main__':
	app.debug=True
	#app.run(host='0.0.0.0',port=1403)
	app.run(host='localhost',port=5000)