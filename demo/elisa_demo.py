from flask import Flask, redirect, url_for, request, render_template
from elisalib import searchProcedure, retrieveSentences, assetToHTMLTable, EmotionDictionariesAndArrays
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
		cmpany = request.form['company']
		sentTypeList = request.form.getlist('sentenceType')
		sentType = ''
		for elem in sentTypeList:
			sentType = sentType + str(elem)
		minwordcount = request.form['minwordcount']
		#print 'sType: ' 
		#print sentType
		return redirect(url_for('keyword_search',keyword = kword, company=cmpany, sType=sentType, minWordCount=minwordcount))
	else:
		kword = request.args.get('keyword')
		cmpany = request.args.get('company')
		sentType = request.args.getlist('sentenceType')
		minwordcount = request.args.get('minwordcount')
		return redirect(url_for('keyword_search',keyword = kword, company=cmpany, sType=sentType, minWordCount=minwordcount))
		
#@app.route('/search/<keyword>')
#def keyword_search(keyword):
@app.route('/search/', methods=['GET'])
def keyword_search():
	keyword = request.args.get('keyword')
	cmp = request.args.get('company').lower()
	#sentenceList, qnaList = retrieveSentencesContainingWordInFullJSON('data_sent_year_new.json', 'fiber')
	sentenceTypeFilter = request.args.get('sType')
	minWordCountFilter = request.args.get('minWordCount')
	sentenceHTMLTable, keys_price, vals_price, emotionMaxHTMLTable, emotionAvgHTMLTable, emotionStdHTMLTable, emotionPercentageHTMLTable, emotionSpikeHTMLTable, wordcloud_path, emoArrayObj = searchProcedure(keyword, cmp, True, sentenceTypeFilter, minWordCountFilter)
	
	
	
	
	return render_template('searchresults.html', word = keyword, company = cmp, table = sentenceHTMLTable, price_keys = keys_price, price_vals = vals_price,  emotionMaxTable = emotionMaxHTMLTable, emotionAvgTable = emotionAvgHTMLTable, emotionStdTable = emotionStdHTMLTable, emotionPercentTable = emotionPercentageHTMLTable, emotionSpikeTable = emotionSpikeHTMLTable, sentenceType=sentenceTypeFilter, minWordCount=minWordCountFilter, wordCloudPath= wordcloud_path, arrStrPositive = emoArrayObj.arrStrPositive, arrStrNegative = emoArrayObj.arrStrNegative, arrStrAngerMax = emoArrayObj.arrStrAngerMax, arrStrDisgustMax = emoArrayObj.arrStrDisgustMax, arrStrFearMax = emoArrayObj.arrStrFearMax, arrStrHappinessMax = emoArrayObj.arrStrHappinessMax, arrStrNeutralMax = emoArrayObj.arrStrNeutralMax, arrStrSadnessMax = emoArrayObj.arrStrSadnessMax, arrStrSurpriseMax = emoArrayObj.arrStrSurpriseMax, arrStrAngerAvg = emoArrayObj.arrStrAngerAvg, arrStrDisgustAvg = emoArrayObj.arrStrDisgustAvg, arrStrFearAvg = emoArrayObj.arrStrFearAvg, arrStrHappinessAvg = emoArrayObj.arrStrHappinessAvg, arrStrNeutralAvg = emoArrayObj.arrStrNeutralAvg, arrStrSadnessAvg = emoArrayObj.arrStrSadnessAvg, arrStrSurpriseAvg = emoArrayObj.arrStrSurpriseAvg, arrStrAngerPercent = emoArrayObj.arrStrAngerPercent, arrStrDisgustPercent = emoArrayObj.arrStrDisgustPercent, arrStrFearPercent = emoArrayObj.arrStrFearPercent, arrStrHappinessPercent = emoArrayObj.arrStrHappinessPercent, arrStrNeutralPercent = emoArrayObj.arrStrNeutralPercent, arrStrSadnessPercent = emoArrayObj.arrStrSadnessPercent, arrStrSurprisePercent = emoArrayObj.arrStrSurprisePercent, arrStrAngerSpike = emoArrayObj.arrStrAngerSpike, arrStrDisgustSpike = emoArrayObj.arrStrDisgustSpike, arrStrFearSpike = emoArrayObj.arrStrFearSpike, arrStrHappinessSpike = emoArrayObj.arrStrHappinessSpike, arrStrNeutralSpike = emoArrayObj.arrStrNeutralSpike, arrStrSadnessSpike = emoArrayObj.arrStrSadnessSpike, arrStrSurpriseSpike = emoArrayObj.arrStrSurpriseSpike, arrStrDates = emoArrayObj.arrStrDates)

@app.route('/asset/<specs>')
def retrieve_assets(specs):
	keyword, company, yearQuartile, sentenceType,minWordCountFilter = specs.split("_")
	sentencesFound = retrieveSentences(keyword, company, yearQuartile, sentenceType, minWordCountFilter) 
	#print sentencesFound
	return render_template('asset.html', html_keyword = keyword, html_yearQuartile = yearQuartile, html_company = company, html_content = assetToHTMLTable(sentencesFound), sentenceType = sentenceType, minWordCount=minWordCountFilter)

if __name__ == '__main__':
	app.debug=True
	#app.run(host='0.0.0.0',port=1403)
	app.run(host='localhost',port=5000)