import re
import json
from pprint import pprint
import math

def searchProcedure(word, sentenceLevelAggregation):
	jsonFilePath = 'data_with_emovec.json' ########################################## HARDCODED VALUE !

	# (1) Keyword search in the entire JSON list.
	# get the sentences containing the word, and the qna id list that these sentences belong to.
	print "Keyword search in progress..."
	sentenceList, qnaList = retrieveSentencesContainingWordInFullJSON(jsonFilePath, word)
	print "Keyword search complete. " + str(len(sentenceList)) + " sentences found containing the word"
	
	# (2) [OPTIONAL] If QnA level aggregation is selected, retrieve the QnA objects having the sentences that contain the word
	if not sentenceLevelAggregation: # This means QNA level aggregation
		print "QnA-level aggregation selected. Retrieving relevant QnA objects..."
		qnaJSON = retrieveQnAsFromFullJSON(jsonFilePath, qnaList)
		sentenceList = qnaJSON
		print "QnA objects retrieved successfully."
		
	# (3) 
	print "Rolling up values from individual level to Quartile Level"
	dictPos = aggregateValuesForQuartile(sentenceList, 'positive_sentiment') ########################################## HARDCODED VALUE !
    #for key in sorted(mydict.iterkeys()):
    #    print "%s: %s" % (key, mydict[key])
	dictNeg = aggregateValuesForQuartile(sentenceList, 'negative_sentiment') ########################################## HARDCODED VALUE !
	#print dictionaryToTSV(dictPos, dictNeg)
	#print dictionaryToHTMLTable(dictPos, dictNeg)
	#print "Complete!"
	keys, vals_pos = dictionaryToArray(dictPos)
	keys, vals_neg = dictionaryToArray(dictNeg)

	dictAnger = aggregateValuesForQuartile(sentenceList, 'Anger') ########################################## HARDCODED VALUE !
	dictDisgust = aggregateValuesForQuartile(sentenceList, 'Disgust') ########################################## HARDCODED VALUE !
	dictFear = aggregateValuesForQuartile(sentenceList, 'Fear') ########################################## HARDCODED VALUE !
	dictHappiness = aggregateValuesForQuartile(sentenceList, 'Happiness') ########################################## HARDCODED VALUE !
	dictNeutral = aggregateValuesForQuartile(sentenceList, 'Neutral') ########################################## HARDCODED VALUE !
	dictSadness = aggregateValuesForQuartile(sentenceList, 'Sadness') ########################################## HARDCODED VALUE !
	dictSurprise = aggregateValuesForQuartile(sentenceList, 'Surprise') ########################################## HARDCODED VALUE !
	
	return dictionaryToSentimentHTMLTable(dictPos, dictNeg), keys, vals_neg, vals_pos, dictionaryToEmotionHTMLTable(dictAnger, dictDisgust, dictFear, dictHappiness, dictNeutral, dictSurprise, dictSadness)

def retrieveSentences(word, company, yearQuartile):
	jsonFilePath = 'data_with_emovec.json'
	sentencesFound, QnAList = retrieveSentencesWithFilterInFullJSON(jsonFilePath, word, company, yearQuartile)
	return sentencesFound
	
def dictionaryToArray(dict):
	keys = ""
	vals = ""
	for key in sorted(dict.iterkeys()):
		keys = keys + "'" + key + "', "
		vals = vals + str(dict[key]) + ", "
	keys = "[" + keys[0:len(keys)-2] + "]"
	vals = "[" + vals[0:len(vals)-2] + "]"
	return keys, vals
	
def dictionaryToTSV(dictPos, dictNeg):
    tsv = "quartile\tpositive\tnegative\n"
    for key in sorted(dictPos.iterkeys()):
        tsv = tsv + key + "\t" + str(dictPos[key]) + "\t" + str(dictNeg[key]) + "\n"
    return tsv

def transformFloatToIntStr(fl):
    transform = format(fl, 'f')
    return str(int(math.ceil(float(transform) * 10)))

def assetToHTMLTable(sentences):
    table = '<table class="asset_table" id="asset_table">'
    th  = "<tr><th style='border-top: 1px solid black;'>Sentence</th><th style='border: 1px solid black;'>Audio</th><th class='asset_td'><img class='emo_image' src='/static/plus.png'></th><th class='asset_td'><img class='emo_image' src='/static/minus.png'></th><th class='asset_td'><img class='emo_image' src='/static/anger.png'></th><th class='asset_td'><img class='emo_image' src='/static/disgust.png'></th><th class='asset_td'><img class='emo_image' src='/static/fear.png'></th><th class='asset_td'><img class='emo_image' src='/static/sadness.png'></th><th class='asset_td'><img class='emo_image' src='/static/surprise.png'></th><th class='asset_td'><img class='emo_image' src='/static/happiness.png'></th><th class='asset_td'><img class='emo_image' src='/static/neutral.png'></th></tr>"
    table = table + th
    for v in sentences:
        sentence = v['lines'][0]
        mp3 = v['elisaEmoVec']['filename']
        senti_pos = v['positive_sentiment']
        senti_neg = v['negative_sentiment']
        emo_anger = transformFloatToIntStr(v['elisaEmoVec']['Anger'])
        emo_disgust = transformFloatToIntStr(v['elisaEmoVec']['Disgust'])
        emo_fear = transformFloatToIntStr(v['elisaEmoVec']['Fear'])
        emo_sad = transformFloatToIntStr(v['elisaEmoVec']['Sadness'])
        emo_surprise = transformFloatToIntStr(v['elisaEmoVec']['Surprise'])
        emo_happiness = transformFloatToIntStr(v['elisaEmoVec']['Happiness'])
        emo_neutral = transformFloatToIntStr(v['elisaEmoVec']['Neutral'])
        
        tr = '<tr class="asset_tr">' + '<td class="asset_sentence">' + sentence + '</td>' + '<td class="asset_td"><img class="play_button" src="/static/play_button.png" onclick="playMe(this)" id="' + mp3 + '"></td>' + '<td class="asset_td">' + senti_pos + '</td>' + '<td class="asset_td">' + senti_neg + '</td>' + '<td class="asset_td">' + emo_anger + '</td>' + '<td class="asset_td">' + emo_disgust + '</td>' + '<td class="asset_td">' + emo_fear + '</td>' + '<td class="asset_td">' + emo_sad + '</td>' + '<td class="asset_td">' + emo_surprise + '</td>' + '<td class="asset_td">' + emo_happiness + '</td>' + '<td class="asset_td">' + emo_neutral + "</td></tr>" 
        table = table + tr
    table = table + "</table>"
    return table

def dictionaryToSentimentHTMLTable(dictPos, dictNeg):
    topHeader = "<TH></TH>"
    header = "<TH></TH>"
    rowPos = "<TD class='rowStart'>Positive</TD>"
    rowNeg = "<TD class='rowStart'>Negative</TD>"
    i = 0
    for key in sorted(dictPos.iterkeys()):
        if i%4==0:
            topHeader = topHeader + "<TH class = 'topHeaderTable' colspan='4'>" + key[0:4] + "</TH>"
        header = header + "<TH class='borderedTD'>Q" + key[4] + "</TH>"
        rowPos = rowPos + "<TD class='borderedTD' onclick='getAsset(\"" + key + "\")'>" + str(dictPos[key]) + "</TD>"
        rowNeg = rowNeg + "<TD class='borderedTD' onclick='getAsset(\"" + key + "\")'>" + str(dictNeg[key]) + "</TD>"  
        i = i + 1
    table = "<TABLE class='quartileTable'><TR>" + topHeader + "</TR>"
    table = table + "<TR>" + header + "</TR>"
    table = table + "<TR>" + rowPos + "</TR>"
    table = table + "<TR>" + rowNeg + "</TR>"
    table = table + "</TABLE>"
    return table    

def dictionaryToEmotionHTMLTable(dictAnger, dictDisgust, dictFear, dictHappiness, dictNeutral, dictSurprise, dictSadness):
	topHeader = "<TH></TH>"
	header = "<TH></TH>"
	rowAnger = "<TD class='rowStart'>Anger</TD>"
	rowDisgust = "<TD class='rowStart'>Disgust</TD>"
	rowFear = "<TD class='rowStart'>Fear</TD>"
	rowHappiness = "<TD class='rowStart'>Happiness</TD>"
	rowNeutral = "<TD class='rowStart'>Neutral</TD>"
	rowSurprise = "<TD class='rowStart'>Surprise</TD>"
	rowSadness = "<TD class='rowStart'>Sadness</TD>"
	i = 0
	for key in sorted(dictAnger.iterkeys()):
		if i%4==0:
			topHeader = topHeader + "<TH class = 'topHeaderTable' colspan='4'>" + key[0:4] + "</TH>"
		header = header + "<TH class='borderedTD'>Q" + key[4] + "</TH>"
		rowAnger = rowAnger + "<TD class='borderedTD' onclick='getAsset(\"" + key + "\")'>" + str(dictAnger[key]) + "</TD>"
		rowDisgust = rowDisgust + "<TD class='borderedTD' onclick='getAsset(\"" + key + "\")'>" + str(dictDisgust[key]) + "</TD>"
		rowFear = rowFear + "<TD class='borderedTD' onclick='getAsset(\"" + key + "\")'>" + str(dictFear[key]) + "</TD>"  
		rowSadness = rowSadness + "<TD class='borderedTD' onclick='getAsset(\"" + key + "\")'>" + str(dictSadness[key]) + "</TD>"  
		rowSurprise = rowSurprise + "<TD class='borderedTD' onclick='getAsset(\"" + key + "\")'>" + str(dictSurprise[key]) + "</TD>"  
		rowHappiness = rowHappiness + "<TD class='borderedTD' onclick='getAsset(\"" + key + "\")'>" + str(dictHappiness[key]) + "</TD>"  
		rowNeutral = rowNeutral + "<TD class='borderedTD' onclick='getAsset(\"" + key + "\")'>" + str(dictNeutral[key]) + "</TD>"  
		i = i + 1
	table = "<TABLE class='quartileTable'><TR>" + topHeader + "</TR>"
	table = table + "<TR>" + header + "</TR>"
	table = table + "<TR>" + rowAnger + "</TR>"
	table = table + "<TR>" + rowDisgust + "</TR>"
	table = table + "<TR>" + rowFear + "</TR>"
	table = table + "<TR>" + rowSadness + "</TR>"
	table = table + "<TR>" + rowSurprise + "</TR>"
	table = table + "<TR>" + rowHappiness + "</TR>"
	table = table + "<TR>" + rowNeutral + "</TR>"
	table = table + "</TABLE>"
	return table    

# Finds and retrieves the JSON objects in which the sentence contain the specified word. 
# Retrieves also the QnAList that these sentences belong to.    
def retrieveSentencesContainingWordInFullJSON(jsonFilePath, word):
    data = json.load(open(jsonFilePath))
    sentencesFound = []
    QnAList = []
    for v in data["fragments"]:
        sentence = v['lines'][0]
        if re.search(word, sentence, re.IGNORECASE):
            sentencesFound.append(v)
            qid = v['question_id']
            if qid not in QnAList:
                QnAList.append(qid)
    return sentencesFound, QnAList

# Finds and retrieves the JSON objects in which the sentence contain the specified word. 
# Retrieves also the QnAList that these sentences belong to.    
def retrieveSentencesWithFilterInFullJSON(jsonFilePath, word, company, yearQuartile):
	data = json.load(open(jsonFilePath))
	sentencesFound = []
	QnAList = []
	for v in data["fragments"]:
		sentence = v['lines'][0]
		company = v['company']
		yq = v['yearQuartile']
		if re.search(word, sentence, re.IGNORECASE) and re.search(company, company, re.IGNORECASE) and yq == yearQuartile:
			sentencesFound.append(v)
			qid = v['question_id']
			if qid not in QnAList:
				QnAList.append(qid)
	return sentencesFound, QnAList
	
# Retrieves JSON objects of the specified QnA IDs
def retrieveQnAsFromFullJSON(jsonFilePath, qnaList):
    data = json.load(open(jsonFilePath))
    QnAListToReturn = []
    for v in data["fragments"]:
        qid = v['question_id']
        if qid in qnaList:
            QnAListToReturn.append(v) 
    return QnAListToReturn


#print qnaList
#qnaJSON = retrieveQnAsFromFullJSON('data_sent_year_new.json', qnaList)
#pprint(qnaJSON)

# create and return a dictionary with the keys as quartiles in YYYYQ format.  
def quartileDictionary(startYear, endYear):
    dict = {}
    for x in range(startYear, endYear):
        #print "We're on time %d" % (x)
        for y in range (1, 5):
            quart = str(x) + str(y)
            dict[quart] = 0
    return dict

def returnJSONobjectsFilteredDownByQuartile(jsonList, yearQuartile):
    filteredList = []
    for v in jsonList:
        if v['yearQuartile'] == yearQuartile:
            filteredList.append(v)
    return filteredList

def aggregateValuesForQuartile(sentenceList, ofWhat):
    mydict = quartileDictionary(2012, 2019) ########################################## HARDCODED VALUE !
    for key in sorted(mydict.iterkeys()):
        filteredList = returnJSONobjectsFilteredDownByQuartile(sentenceList, key) #key=20141
        mydict[key] = getMax(filteredList, ofWhat)
        #print "%s: %s" % (key, mydict[key])
    return mydict

def getMax(jsonList, ofWhat):
	maxValue = 0
	for v in jsonList:
		if ofWhat == "positive_sentiment" or ofWhat == "negative_sentiment":
			value = int(v[ofWhat])
		if ofWhat == "Anger":
			measurementString = v['elisaEmoVec']['Anger']
			transform = format(measurementString, 'f')
			value = int(math.ceil(float(transform) * 10))
		if ofWhat == "Disgust":
			measurementString = v['elisaEmoVec']['Disgust']
			transform = format(measurementString, 'f')
			value = int(math.ceil(float(transform) * 10))
		if ofWhat == "Fear":
			measurementString = v['elisaEmoVec']['Fear']
			transform = format(measurementString, 'f')
			value = int(math.ceil(float(transform) * 10))
		if ofWhat == "Happiness":
			measurementString = v['elisaEmoVec']['Happiness']
			transform = format(measurementString, 'f')
			value = int(math.ceil(float(transform) * 10))
		if ofWhat == "Neutral":
			measurementString = v['elisaEmoVec']['Neutral']
			transform = format(measurementString, 'f')
			value = int(math.ceil(float(transform) * 10))
		if ofWhat == "Sadness":
			measurementString = v['elisaEmoVec']['Sadness']
			transform = format(measurementString, 'f')
			value = int(math.ceil(float(transform) * 10))
		if ofWhat == "Surprise":
			measurementString = v['elisaEmoVec']['Surprise']
			transform = format(measurementString, 'f')
			value = int(math.ceil(float(transform) * 10))
		if value > maxValue:
			maxValue = value
	return maxValue
	
#filteredList = returnJSONobjectsFilteredDownByQuartile(sentenceList, '20141')
#print getMax(filteredList, 'positive_sentiment')

#searchProcedure('margins', True)

#mydict = quartileDictionary(2008, 2012)
#for key in sorted(mydict.iterkeys()):
#    print "%s: %s" % (key, mydict[key])