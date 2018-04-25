import re
import json
from pprint import pprint
import math
#import pdfkit
from wordcloud import WordCloud
import numpy as np
import pandas as pd
import os
from time import gmtime, strftime
import csv
from datetime import datetime
import matplotlib

matplotlib.use('Agg')

class EmotionDictionariesAndArrays:
	
	
	def __init__(self, dicPositive, dicNegative, dicAngerMax, dicDisgustMax, dicFearMax, dicHappinessMax, dicNeutralMax, dicSadnessMax, dicSurpriseMax, dicAngerAvg, dicDisgustAvg, dicFearAvg, dicHappinessAvg, dicNeutralAvg, dicSadnessAvg, dicSurpriseAvg, dicAngerPercent, dicDisgustPercent, dicFearPercent, dicHappinessPercent, dicNeutralPercent, dicSadnessPercent, dicSurprisePercent, dicAngerSpike, dicDisgustSpike, dicFearSpike, dicHappinessSpike, dicNeutralSpike, dicSadnessSpike, dicSurpriseSpike, listOfDatesOfQuarters):
		self.dictionaryPositive, self.dictionaryNegative, self.dictionaryAngerMax, self.dictionaryDisgustMax, self.dictionaryFearMax, self.dictionaryHappinessMax, self.dictionaryNeutralMax, self.dictionarySadnessMax, self.dictionarySurpriseMax, self.dictionaryAngerAvg, self.dictionaryDisgustAvg, self.dictionaryFearAvg, self.dictionaryHappinessAvg, self.dictionaryNeutralAvg, self.dictionarySadnessAvg, self.dictionarySurpriseAvg, self.dictionaryAngerPercent, self.dictionaryDisgustPercent, self.dictionaryFearPercent, self.dictionaryHappinessPercent, self.dictionaryNeutralPercent, self.dictionarySadnessPercent, self.dictionarySurprisePercent, self.dictionaryAngerSpike, self.dictionaryDisgustSpike, self.dictionaryFearSpike, self.dictionaryHappinessSpike, self.dictionaryNeutralSpike, self.dictionarySadnessSpike, self.dictionarySurpriseSpike, self.listOfDatesOfQuarters = dicPositive, dicNegative, dicAngerMax, dicDisgustMax, dicFearMax, dicHappinessMax, dicNeutralMax, dicSadnessMax, dicSurpriseMax, dicAngerAvg, dicDisgustAvg, dicFearAvg, dicHappinessAvg, dicNeutralAvg, dicSadnessAvg, dicSurpriseAvg, dicAngerPercent, dicDisgustPercent, dicFearPercent, dicHappinessPercent, dicNeutralPercent, dicSadnessPercent, dicSurprisePercent, dicAngerSpike, dicDisgustSpike, dicFearSpike, dicHappinessSpike, dicNeutralSpike, dicSadnessSpike, dicSurpriseSpike, listOfDatesOfQuarters
		
		self.arrStrPositive, self.arrStrNegative, self.arrStrAngerMax, self.arrStrDisgustMax, self.arrStrFearMax, self.arrStrHappinessMax, self.arrStrNeutralMax, self.arrStrSadnessMax, self.arrStrSurpriseMax, self.arrStrAngerAvg, self.arrStrDisgustAvg, self.arrStrFearAvg, self.arrStrHappinessAvg, self.arrStrNeutralAvg, self.arrStrSadnessAvg, self.arrStrSurpriseAvg, self.arrStrAngerPercent, self.arrStrDisgustPercent, self.arrStrFearPercent, self.arrStrHappinessPercent, self.arrStrNeutralPercent, self.arrStrSadnessPercent, self.arrStrSurprisePercent, self.arrStrAngerSpike, self.arrStrDisgustSpike, self.arrStrFearSpike, self.arrStrHappinessSpike, self.arrStrNeutralSpike, self.arrStrSadnessSpike, self.arrStrSurpriseSpike, self.arrStrDates = "","","","","","","","","","","","","","","","","","","","","","","","","","","","","","", ""

	def replaceQuartilesWithCallDates(self, quartile):
		returnStr = ""
		for v in self.listOfDatesOfQuarters:
			if v[0] == quartile:
				returnStr = v[1]
		return returnStr
	
	def dictionaryToArrayString(self, dict, returnType):
		keys = ""
		vals = ""
		returnStr = ""
		for key in sorted(dict.iterkeys()):
			keys = keys + "'" + self.replaceQuartilesWithCallDates(key) + "', "
			vals = vals + str(dict[key]).replace(',','.') + ", "
		keys = "[" + keys[0:len(keys)-2] + "]"
		vals = "[" + vals[0:len(vals)-2] + "]"
		if returnType == 'keys':
			returnStr = keys
		if returnType == 'vals':
			returnStr = vals 
		return returnStr

	def convertDictionariesIntoArrays(self):
		self.arrStrPositive, self.arrStrNegative = self.dictionaryToArrayString(self.dictionaryPositive, 'vals'), self.dictionaryToArrayString(self.dictionaryNegative, 'vals')
		
		self.arrStrAngerMax, self.arrStrDisgustMax, self.arrStrFearMax, self.arrStrHappinessMax, self.arrStrNeutralMax, self.arrStrSadnessMax, self.arrStrSurpriseMax = self.dictionaryToArrayString(self.dictionaryAngerMax, 'vals'), self.dictionaryToArrayString(self.dictionaryDisgustMax, 'vals'), self.dictionaryToArrayString(self.dictionaryFearMax, 'vals'), self.dictionaryToArrayString(self.dictionaryHappinessMax, 'vals'), self.dictionaryToArrayString(self.dictionaryNeutralMax, 'vals'), self.dictionaryToArrayString(self.dictionarySadnessMax, 'vals'), self.dictionaryToArrayString(self.dictionarySurpriseMax, 'vals')
		
		self.arrStrAngerAvg, self.arrStrDisgustAvg, self.arrStrFearAvg, self.arrStrHappinessAvg, self.arrStrNeutralAvg, self.arrStrSadnessAvg, self.arrStrSurpriseAvg = self.dictionaryToArrayString(self.dictionaryAngerAvg, 'vals'), self.dictionaryToArrayString(self.dictionaryDisgustAvg, 'vals'), self.dictionaryToArrayString(self.dictionaryFearAvg, 'vals'), self.dictionaryToArrayString(self.dictionaryHappinessAvg, 'vals'), self.dictionaryToArrayString(self.dictionaryNeutralAvg, 'vals'), self.dictionaryToArrayString(self.dictionarySadnessAvg, 'vals'), self.dictionaryToArrayString(self.dictionarySurpriseAvg, 'vals')
		
		self.arrStrAngerPercent, self.arrStrDisgustPercent, self.arrStrFearPercent, self.arrStrHappinessPercent, self.arrStrNeutralPercent, self.arrStrSadnessPercent, self.arrStrSurprisePercent = self.dictionaryToArrayString(self.dictionaryAngerPercent, 'vals'), self.dictionaryToArrayString(self.dictionaryDisgustPercent, 'vals'), self.dictionaryToArrayString(self.dictionaryFearPercent, 'vals'), self.dictionaryToArrayString(self.dictionaryHappinessPercent, 'vals'), self.dictionaryToArrayString(self.dictionaryNeutralPercent, 'vals'), self.dictionaryToArrayString(self.dictionarySadnessPercent, 'vals'), self.dictionaryToArrayString(self.dictionarySurprisePercent, 'vals')
		self.arrStrAngerSpike, self.arrStrDisgustSpike, self.arrStrFearSpike, self.arrStrHappinessSpike, self.arrStrNeutralSpike, self.arrStrSadnessSpike, self.arrStrSurpriseSpike = self.dictionaryToArrayString(self.dictionaryAngerSpike, 'vals'), self.dictionaryToArrayString(self.dictionaryDisgustSpike, 'vals'), self.dictionaryToArrayString(self.dictionaryFearSpike, 'vals'), self.dictionaryToArrayString(self.dictionaryHappinessSpike, 'vals'), self.dictionaryToArrayString(self.dictionaryNeutralSpike, 'vals'), self.dictionaryToArrayString(self.dictionarySadnessSpike, 'vals'), self.dictionaryToArrayString(self.dictionarySurpriseSpike, 'vals')
		
		self.arrStrDates = self.dictionaryToArrayString(self.dictionaryAngerMax, 'keys')
		#print 'ARR DATES'
		#print self.arrStrDates
		#print len(self.arrStrDates)
		#print self.arrStrAngerMax
		#print len(self.arrStrAngerMax)
		return 0

def searchProcedure(word, company, sentenceLevelAggregation, sentenceType, minWordCountFilter):
	#jsonFilePath = 'nokia_data_with_emovec.json' ########################################## HARDCODED VALUE !
	jsonFilePath = company + '_master.json'
	
	# (1) Keyword search in the entire JSON list.
	# get the sentences containing the word, and the qna id list that these sentences belong to.
	print "Keyword search in progress..."
	sentenceList, qnaList = retrieveSentencesContainingWordInFullJSON(jsonFilePath, word, sentenceType, minWordCountFilter)
	print "Keyword search complete. " + str(len(sentenceList)) + " sentences found containing the word"
	
	# (2) [OPTIONAL] If QnA level aggregation is selected, retrieve the QnA objects having the sentences that contain the word
	if not sentenceLevelAggregation: # This means QNA level aggregation
		print "QnA-level aggregation selected. Retrieving relevant QnA objects..."
		qnaJSON = retrieveQnAsFromFullJSON(jsonFilePath, qnaList)
		sentenceList = qnaJSON
		print "QnA objects retrieved successfully."
		
	# (3) 
	print "Rolling up values from individual level to Quartile Level"
	dictPos = aggregateValuesForQuartile(sentenceList, 'positive_sentiment', 'MAX') ########################################## HARDCODED VALUE !
    #for key in sorted(mydict.iterkeys()):
    #    print "%s: %s" % (key, mydict[key])
	dictNeg = aggregateValuesForQuartile(sentenceList, 'negative_sentiment', 'MAX') ########################################## HARDCODED VALUE !
	#print dictionaryToTSV(dictPos, dictNeg)
	#print dictionaryToHTMLTable(dictPos, dictNeg)
	#print "Complete!"
	keys, vals_pos = dictionaryToArray(dictPos)
	keys, vals_neg = dictionaryToArray(dictNeg)

	# MAX
	dictAnger = aggregateValuesForQuartile(sentenceList, 'Anger', 'MAX') ########################################## HARDCODED VALUE !
	dictDisgust = aggregateValuesForQuartile(sentenceList, 'Disgust', 'MAX') ########################################## HARDCODED VALUE !
	dictFear = aggregateValuesForQuartile(sentenceList, 'Fear', 'MAX') ########################################## HARDCODED VALUE !
	dictHappiness = aggregateValuesForQuartile(sentenceList, 'Happiness', 'MAX') ########################################## HARDCODED VALUE !
	dictNeutral = aggregateValuesForQuartile(sentenceList, 'Neutral', 'MAX') ########################################## HARDCODED VALUE !
	dictSadness = aggregateValuesForQuartile(sentenceList, 'Sadness', 'MAX') ########################################## HARDCODED VALUE !
	dictSurprise = aggregateValuesForQuartile(sentenceList, 'Surprise', 'MAX') ########################################## HARDCODED VALUE !
	
	# AVG
	dictAngerAvg = aggregateValuesForQuartile(sentenceList, 'Anger', 'AVG') ########################################## HARDCODED VALUE !
	dictDisgustAvg = aggregateValuesForQuartile(sentenceList, 'Disgust', 'AVG') ########################################## HARDCODED VALUE !
	dictFearAvg = aggregateValuesForQuartile(sentenceList, 'Fear', 'AVG') ########################################## HARDCODED VALUE !
	dictHappinessAvg = aggregateValuesForQuartile(sentenceList, 'Happiness', 'AVG') ########################################## HARDCODED VALUE !
	dictNeutralAvg = aggregateValuesForQuartile(sentenceList, 'Neutral', 'AVG') ########################################## HARDCODED VALUE !
	dictSadnessAvg = aggregateValuesForQuartile(sentenceList, 'Sadness', 'AVG') ########################################## HARDCODED VALUE !
	dictSurpriseAvg = aggregateValuesForQuartile(sentenceList, 'Surprise', 'AVG') ########################################## HARDCODED VALUE !
	
	# STDDEV
	dictAngerStd = aggregateValuesForQuartile(sentenceList, 'Anger', 'STDDEV') ########################################## HARDCODED VALUE !
	dictDisgustStd = aggregateValuesForQuartile(sentenceList, 'Disgust', 'STDDEV') ########################################## HARDCODED VALUE !
	dictFearStd = aggregateValuesForQuartile(sentenceList, 'Fear', 'STDDEV') ########################################## HARDCODED VALUE !
	dictHappinessStd = aggregateValuesForQuartile(sentenceList, 'Happiness', 'STDDEV') ########################################## HARDCODED VALUE !
	dictNeutralStd = aggregateValuesForQuartile(sentenceList, 'Neutral', 'STDDEV') ########################################## HARDCODED VALUE !
	dictSadnessStd = aggregateValuesForQuartile(sentenceList, 'Sadness', 'STDDEV') ########################################## HARDCODED VALUE !
	dictSurpriseStd = aggregateValuesForQuartile(sentenceList, 'Surprise', 'STDDEV') ########################################## HARDCODED VALUE !
	
	# PERCENTAGE OF BEING MAX EMOTION
	dictAngerPercent = aggregateValuesForQuartile(sentenceList, 'Anger', 'PERCENTAGE') ########################################## HARDCODED VALUE !
	dictDisgustPercent = aggregateValuesForQuartile(sentenceList, 'Disgust', 'PERCENTAGE') ########################################## HARDCODED VALUE !
	dictFearPercent = aggregateValuesForQuartile(sentenceList, 'Fear', 'PERCENTAGE') ########################################## HARDCODED VALUE !
	dictHappinessPercent = aggregateValuesForQuartile(sentenceList, 'Happiness', 'PERCENTAGE') ########################################## HARDCODED VALUE !
	dictNeutralPercent = aggregateValuesForQuartile(sentenceList, 'Neutral', 'PERCENTAGE') ########################################## HARDCODED VALUE !
	dictSadnessPercent = aggregateValuesForQuartile(sentenceList, 'Sadness', 'PERCENTAGE') ########################################## HARDCODED VALUE !
	dictSurprisePercent = aggregateValuesForQuartile(sentenceList, 'Surprise', 'PERCENTAGE') ########################################## HARDCODED VALUE !
	
	# PERCENTAGE OF SPIKES (2 SD ABOVE THE MEAN)
	dictAngerSpike = aggregateValuesForQuartile(sentenceList, 'Anger', 'SPIKE') ########################################## HARDCODED VALUE !
	dictDisgustSpike = aggregateValuesForQuartile(sentenceList, 'Disgust', 'SPIKE') ########################################## HARDCODED VALUE !
	dictFearSpike = aggregateValuesForQuartile(sentenceList, 'Fear', 'SPIKE') ########################################## HARDCODED VALUE !
	dictHappinessSpike = aggregateValuesForQuartile(sentenceList, 'Happiness', 'SPIKE') ########################################## HARDCODED VALUE !
	dictNeutralSpike = aggregateValuesForQuartile(sentenceList, 'Neutral', 'SPIKE') ########################################## HARDCODED VALUE !
	dictSadnessSpike = aggregateValuesForQuartile(sentenceList, 'Sadness', 'SPIKE') ########################################## HARDCODED VALUE !
	dictSurpriseSpike = aggregateValuesForQuartile(sentenceList, 'Surprise', 'SPIKE') ########################################## HARDCODED VALUE !
	
	dictCount = aggregateValuesForQuartile(sentenceList, '', 'COUNT') ########################################## HARDCODED VALUE !
	
	# (4) Create a wordcloud
	wordcloud_path = getWordcloud(sentenceList)
	
	# (5) Price data
	dict_price = {}

	with open('price_' + company + '_yeni.csv', 'rb') as csvfile:
		prices = csv.reader(csvfile, delimiter=';', quotechar='"')
		#print prices
		for row in prices:
			dict_price[row[0]] = row[1]
	
	# Load the keys and values of the price dictionary into two arrays. 
	price_keys, price_vals = dictionaryToArray(dict_price)
	
	# (6) Emotion arrays to display on graph 
	listofQuarterDates = loadExactDatesOfQuarterCalls(company)
	emoDictArrayObject = EmotionDictionariesAndArrays(dictPos, dictNeg,dictAnger, dictDisgust, dictFear, dictHappiness, dictNeutral, dictSadness, dictSurprise, dictAngerAvg, dictDisgustAvg, dictFearAvg, dictHappinessAvg, dictNeutralAvg, dictSadnessAvg, dictSurpriseAvg, dictAngerPercent, dictDisgustPercent, dictFearPercent, dictHappinessPercent, dictNeutralPercent, dictSadnessPercent, dictSurprisePercent, dictAngerSpike, dictDisgustSpike, dictFearSpike, dictHappinessSpike, dictNeutralSpike, dictSadnessSpike, dictSurpriseSpike, listofQuarterDates)
	

	emoDictArrayObject.convertDictionariesIntoArrays()
	#print emoDictArrayObject.arrStrAngerMax
	
	return dictionaryToSentimentHTMLTable(dictPos, dictNeg, dictCount), price_keys, price_vals, dictionaryToEmotionHTMLTable("quartileEmotionTableMax", dictAnger, dictDisgust, dictFear, dictHappiness, dictNeutral, dictSurprise, dictSadness), dictionaryToEmotionHTMLTable("quartileEmotionTableAvg", dictAngerAvg, dictDisgustAvg, dictFearAvg, dictHappinessAvg, dictNeutralAvg, dictSurpriseAvg, dictSadnessAvg), dictionaryToEmotionHTMLTable("quartileEmotionTableStd", dictAngerStd, dictDisgustStd, dictFearStd, dictHappinessStd, dictNeutralStd, dictSurpriseStd, dictSadnessStd), dictionaryToEmotionHTMLTable("quartileEmotionTablePercentage", dictAngerPercent, dictDisgustPercent, dictFearPercent, dictHappinessPercent, dictNeutralPercent, dictSurprisePercent, dictSadnessPercent), dictionaryToEmotionHTMLTable("quartileEmotionTableSpike", dictAngerSpike, dictDisgustSpike, dictFearSpike, dictHappinessSpike, dictNeutralSpike, dictSurpriseSpike, dictSadnessSpike), wordcloud_path, emoDictArrayObject

def loadExactDatesOfQuarterCalls(comp):
	listoflists = []
	with open('datequartmap_yeni.csv', 'rb') as csvfile:
		prices = csv.reader(csvfile, delimiter=';', quotechar='"')
		for row in prices:
			if str(row[0]).lower() == comp:
				listtoadd = [row[1], row[2]]
				listoflists.append(listtoadd)
	return listoflists
		
def retrieveSentences(word, company, yearQuartile, sentenceType, minWordCountFilter):
	jsonFilePath = company + '_master.json'
	#jsonFilePath = 'data_with_emovec.json' ########################################## HARDCODED VALUE !
	#jsonFilePath = 'nokia_data_with_emovec.json' ########################################## HARDCODED VALUE !
	sentencesFound, QnAList = retrieveSentencesWithFilterInFullJSON(jsonFilePath, word, company, yearQuartile, sentenceType, minWordCountFilter)
	return sentencesFound
	
def dictionaryToArray(dict):
	keys = ""
	vals = ""
	for key in sorted(dict.iterkeys()):
		keys = keys + "'" + key + "', "
		vals = vals + str(dict[key]).replace(',','.') + ", "
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
    #printHTMLasPDF(table)
    return table

def dictionaryToSentimentHTMLTable(dictPos, dictNeg, dictCount):
    topHeader = "<TH></TH>"
    header = "<TH></TH>"
    rowPos = "<TD class='rowStart'>Positive</TD>"
    rowNeg = "<TD class='rowStart'>Negative</TD>"
    rowCount = "<TD class='rowStart'>COUNT</TD>"
    i = 0
    for key in sorted(dictPos.iterkeys()):
        if i%4==0:
            topHeader = topHeader + "<TH class = 'topHeaderTable' colspan='4'>" + key[0:4] + "</TH>"
        header = header + "<TH class='borderedTD'>Q" + key[4] + "</TH>"
        rowPos = rowPos + "<TD class='borderedTD' onclick='getAsset(\"" + key + "\")'>" + str(dictPos[key]) + "</TD>"
        rowNeg = rowNeg + "<TD class='borderedTD' onclick='getAsset(\"" + key + "\")'>" + str(dictNeg[key]) + "</TD>"  
        rowCount = rowCount + "<TD class='borderedTD' onclick='getAsset(\"" + key + "\")'>" + str(dictCount[key]) + "</TD>"  
        i = i + 1
    table = "<TABLE id='quartileSentimentTable' class='quartileTable'><TR>" + topHeader + "</TR>"
    table = table + "<TR>" + header + "</TR>"
    table = table + "<TR>" + rowPos + "</TR>"
    table = table + "<TR>" + rowNeg + "</TR>"
    table = table + "<TR>" + rowCount + "</TR>"
    table = table + "</TABLE>"
    return table    

def dictionaryToEmotionHTMLTable(tableID, dictAnger, dictDisgust, dictFear, dictHappiness, dictNeutral, dictSurprise, dictSadness):
	topHeader = "<TH></TH>"
	header = "<TH></TH>"
	rowAnger = "<TD onclick='addEmoGraph(\"" + tableID + "\", \"Anger\")' class='rowStart'>Anger</TD>"
	rowDisgust = "<TD onclick='addEmoGraph(\"" + tableID + "\", \"Disgust\")' class='rowStart'>Disgust</TD>"
	rowFear = "<TD onclick='addEmoGraph(\"" + tableID + "\", \"Fear\")' class='rowStart'>Fear</TD>"
	rowHappiness = "<TD onclick='addEmoGraph(\"" + tableID + "\", \"Happiness\")' class='rowStart'>Happiness</TD>"
	rowNeutral = "<TD onclick='addEmoGraph(\"" + tableID + "\", \"Neutral\")' class='rowStart'>Neutral</TD>"
	rowSurprise = "<TD onclick='addEmoGraph(\"" + tableID + "\", \"Surprise\")' class='rowStart'>Surprise</TD>"
	rowSadness = "<TD onclick='addEmoGraph(\"" + tableID + "\", \"Sadness\")' class='rowStart'>Sadness</TD>"
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
	table = "<TABLE id='" + tableID + "' class='quartileTable'><TR>" + topHeader + "</TR>"
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
def retrieveSentencesContainingWordInFullJSON(jsonFilePath, word, sentenceType, minWordCountFilter):
	data = json.load(open(jsonFilePath))
	sentencesFound = []
	QnAList = []
	for v in data["fragments"]:
		sentence = v['lines'][0]
		if sentence.count(' ') > int(minWordCountFilter): # Only select sentences with 4 or more words.
			qid = v['question_id']
			if sentenceTypeFits(sentenceType, qid):
				if re.search(word, sentence, re.IGNORECASE):
					sentencesFound.append(v)
					qid = v['question_id']
					if qid not in QnAList:
						QnAList.append(qid)
	return sentencesFound, QnAList

# Possible sentence types: Q, A, O, QA, QO, AO, QAO
# Example question_id: "question_id": "Nokia.20111.1.0.0"
def sentenceTypeFits(sentenceType, question_id):
	returnVal = False
	answer_bit = question_id[question_id.rfind(".")+1:]
	question_bit = question_id[question_id.rfind(".", 0, question_id.rfind("."))+1:question_id.rfind(".")]
	#Q
	if 'Q' in sentenceType and 'A' not in sentenceType and 'O' not in sentenceType: 
		if question_bit != '0' and answer_bit == '0':
			returnVal = True
	#A
	if 'Q' not in sentenceType and 'A' in sentenceType and 'O' not in sentenceType: 
		if answer_bit != '0':
			returnVal = True
	#O
	if 'Q' not in sentenceType and 'A' not in sentenceType and 'O' in sentenceType: 
		if question_bit == '0' and answer_bit == '0':
			returnVal = True
	#QA
	if 'Q' in sentenceType and 'A' in sentenceType and 'O' not in sentenceType: 
		if question_bit != '0' or answer_bit != '0':
			returnVal = True
	#QO
	if 'Q' in sentenceType and 'A' not in sentenceType and 'O' in sentenceType: 
		if answer_bit == '0':
			returnVal = True
	#AO
	if 'Q' not in sentenceType and 'A' in sentenceType and 'O' in sentenceType: 
		if question_bit == '0':
			returnVal = True
	#QAO
	if 'Q' in sentenceType and 'A' in sentenceType and 'O' in sentenceType: 
		returnVal = True

	return returnVal
	
# Finds and retrieves the JSON objects in which the sentence contain the specified word. 
# Retrieves also the QnAList that these sentences belong to.    
def retrieveSentencesWithFilterInFullJSON(jsonFilePath, word, company, yearQuartile, sentenceType, minWordCountFilter):
	data = json.load(open(jsonFilePath))
	sentencesFound = []
	QnAList = []
	for v in data["fragments"]:
		sentence = v['lines'][0]
		company = v['company']
		yq = v['yearQuartile']
		qid = v['question_id']
		if sentence.count(' ') > int(minWordCountFilter): # Only select sentences with 4 or more words.
			if sentenceTypeFits(sentenceType, qid) and re.search(word, sentence, re.IGNORECASE) and re.search(company, company, re.IGNORECASE) and yq == yearQuartile:
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

def aggregateValuesForQuartile(sentenceList, ofWhat, aggregateMethod):
    mydict = quartileDictionary(2011, 2019) ########################################## HARDCODED VALUE !
    for key in sorted(mydict.iterkeys()):
        filteredList = returnJSONobjectsFilteredDownByQuartile(sentenceList, key) #key=20141
        if aggregateMethod == 'MAX':
            mydict[key] = getMax(filteredList, ofWhat)
        if aggregateMethod == 'COUNT':
            mydict[key] = len(filteredList)
        if aggregateMethod == 'AVG':
            mydict[key] = getAvg(filteredList, ofWhat)
        if aggregateMethod == 'STDDEV':
           mydict[key] = getStdDev(filteredList, ofWhat)
        if aggregateMethod == 'PERCENTAGE':
           mydict[key] = getPercentageBeingMaxEmo(filteredList, ofWhat)
        if aggregateMethod == 'SPIKE':
           mydict[key] = get2SDAbove(filteredList, ofWhat)
        #print "%s: %s" % (key, mydict[key])
    return mydict



def getMax(jsonList, ofWhat):
	maxValue = 0
	for v in jsonList:
		try:
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
		except KeyError:
			print "KeyError detected. Ignoring the value... Explanation: "
			print v
	return maxValue

def getAvg(jsonList, ofWhat):
	avgValue = 0.0
	count = 0
	#debuk = False
	for v in jsonList:
		try:
			if ofWhat == "positive_sentiment" or ofWhat == "negative_sentiment":
				avgValue = avgValue + int(v[ofWhat])
				count = count + 1
			if ofWhat == "Anger":
				measurementString = v['elisaEmoVec']['Anger']
				transform = format(measurementString, 'f')
				avgValue = avgValue + int(math.ceil(float(transform) * 10))
				count = count + 1
			if ofWhat == "Disgust":
				measurementString = v['elisaEmoVec']['Disgust']
				transform = format(measurementString, 'f')
				avgValue = avgValue + int(math.ceil(float(transform) * 10))
				count = count + 1
			if ofWhat == "Fear":
				measurementString = v['elisaEmoVec']['Fear']
				transform = format(measurementString, 'f')
				avgValue = avgValue + int(math.ceil(float(transform) * 10))
				count = count + 1
			if ofWhat == "Happiness":
				measurementString = v['elisaEmoVec']['Happiness']
				transform = format(measurementString, 'f')
				avgValue = avgValue + int(math.ceil(float(transform) * 10))
				count = count + 1
			if ofWhat == "Neutral":
				measurementString = v['elisaEmoVec']['Neutral']
				transform = format(measurementString, 'f')
				avgValue = avgValue + int(math.ceil(float(transform) * 10))
				count = count + 1
			if ofWhat == "Sadness":
				measurementString = v['elisaEmoVec']['Sadness']
				transform = format(measurementString, 'f')
				avgValue = avgValue + int(math.ceil(float(transform) * 10))
				count = count + 1
			if ofWhat == "Surprise":
				measurementString = v['elisaEmoVec']['Surprise']
				transform = format(measurementString, 'f')
				avgValue = avgValue + int(math.ceil(float(transform) * 10))
				count = count + 1
				#if v['yearQuartile'] == '20162':
				#	print avgValue
				#	print count
				#	debuk = True
		except KeyError:
			print "KeyError detected. Ignoring the value... Explanation: "
			print v
	if count == 0:
		avgValue = 0
	else:
		#if debuk:
		#	print " avg before round: "
		#	print avgValue
		#	print float(avgValue / count)
		avgValue = round(avgValue / count, 1)
		#if debuk:
		#	print " avg after round: "
		#	print avgValue
	#if debuk:
	#	print 'RESULTS'
	#	print avgValue
	#	print count
	return avgValue

def getStdDev(jsonList, ofWhat):
	list = []
	debug = False
	for v in jsonList:
		try:
			if ofWhat == "positive_sentiment" or ofWhat == "negative_sentiment":
				value = float(v[ofWhat])
				list.append(value)
			if ofWhat == "Anger":
				measurementString = v['elisaEmoVec']['Anger']
				transform = format(measurementString, 'f')
				value = float(transform) * 10
				list.append(value)
				if v['yearQuartile']=='20141':
					debug = True
			if ofWhat == "Disgust":
				measurementString = v['elisaEmoVec']['Disgust']
				transform = format(measurementString, 'f')
				value = float(transform) * 10
				list.append(value)
			if ofWhat == "Fear":
				measurementString = v['elisaEmoVec']['Fear']
				transform = format(measurementString, 'f') 
				value = float(transform) * 10
				list.append(value)
			if ofWhat == "Happiness":
				measurementString = v['elisaEmoVec']['Happiness']
				transform = format(measurementString, 'f')
				value = float(transform) * 10
				list.append(value)
			if ofWhat == "Neutral":
				measurementString = v['elisaEmoVec']['Neutral']
				transform = format(measurementString, 'f')
				value = float(transform) * 10
				list.append(value)
			if ofWhat == "Sadness":
				measurementString = v['elisaEmoVec']['Sadness']
				transform = format(measurementString, 'f')
				value = float(transform) * 10
				list.append(value)
			if ofWhat == "Surprise":
				measurementString = v['elisaEmoVec']['Surprise']
				transform = format(measurementString, 'f')
				value = float(transform) * 10
				list.append(value)
		except KeyError:
			print "KeyError detected. Ignoring the value... Explanation: "
			print v
	sd = np.std(list)
	if debug:
		print list
		print sd
	return round(sd, 1)

def get2SDAbove(jsonList, ofWhat):
	sd = getStdDev(jsonList, ofWhat)
	avg = getAvg(jsonList, ofWhat)
	#print 'new quartile... ' + " SD: " + str(sd) + " AVG: " + str(avg)
	countEmoBeingAbove = 0.0
	countTotal = 0.0
	ret = 0.0
	for v in jsonList:
		try:
			if ofWhat == "Anger":
				measurementString = v['elisaEmoVec']['Anger']
				transform = format(measurementString, 'f')
				value = float(transform) * 10
				if(value>(avg+2*sd)):
					countEmoBeingAbove = countEmoBeingAbove + 1 
					print "AVG: " + str(avg) + " SD: " + str(sd) + " VALUE: " + str(value)
				countTotal = countTotal + 1
			if ofWhat == "Disgust":
				measurementString = v['elisaEmoVec']['Disgust']
				transform = format(measurementString, 'f') 
				value = float(transform) * 10
				if(value>(avg+2*sd)):
					countEmoBeingAbove = countEmoBeingAbove + 1 
					print "AVG: " + str(avg) + " SD: " + str(sd) + " VALUE: " + str(value)
				countTotal = countTotal + 1
			if ofWhat == "Fear":
				measurementString = v['elisaEmoVec']['Fear']
				transform = format(measurementString, 'f')
				value = float(transform) * 10
				if(value>(avg+2*sd)):
					countEmoBeingAbove = countEmoBeingAbove + 1 
					print "AVG: " + str(avg) + " SD: " + str(sd) + " VALUE: " + str(value)
				countTotal = countTotal + 1
			if ofWhat == "Happiness":
				measurementString = v['elisaEmoVec']['Happiness']
				transform = format(measurementString, 'f')
				value = float(transform) * 10
				if(value>(avg+2*sd)):
					countEmoBeingAbove = countEmoBeingAbove + 1  
					print "AVG: " + str(avg) + " SD: " + str(sd) + " VALUE: " + str(value)
				countTotal = countTotal + 1
			if ofWhat == "Neutral":
				measurementString = v['elisaEmoVec']['Neutral']
				transform = format(measurementString, 'f')
				value = float(transform) * 10
				if(value>(avg+2*sd)):
					countEmoBeingAbove = countEmoBeingAbove + 1  
					print "AVG: " + str(avg) + " SD: " + str(sd) + " VALUE: " + str(value)
				#else:
				#	print 'once: '
				#	print value
				#	print max(list)
				#	print list
				countTotal = countTotal + 1
			if ofWhat == "Sadness":
				measurementString = v['elisaEmoVec']['Sadness']
				transform = format(measurementString, 'f')
				value = float(transform) * 10
				if(value>(avg+2*sd)):
					countEmoBeingAbove = countEmoBeingAbove + 1 
					print "AVG: " + str(avg) + " SD: " + str(sd) + " VALUE: " + str(value)
				countTotal = countTotal + 1
			if ofWhat == "Surprise":
				measurementString = v['elisaEmoVec']['Surprise']
				transform = format(measurementString, 'f')
				value = float(transform) * 10
				if(value>(avg+2*sd)):
					countEmoBeingAbove = countEmoBeingAbove + 1  
					print "AVG: " + str(avg) + " SD: " + str(sd) + " VALUE: " + str(value)
				countTotal = countTotal + 1
		except KeyError:
			print "KeyError detected. Ignoring the value... Explanation: "
			print v
	if countTotal == 0:
		ret = 0.0
	else:
		ret = countEmoBeingAbove / countTotal
	return round(ret, 1)
	
def getPercentageBeingMaxEmo(jsonList, ofWhat):
	countEmoBeingMax = 0.0
	countTotal = 0.0
	ret = 0.0
	for v in jsonList:
		try:
			list = []
			measurementString = v['elisaEmoVec']['Anger']
			transform = format(measurementString, 'f')
			value = float(transform)
			list.append(value)
			measurementString = v['elisaEmoVec']['Disgust']
			transform = format(measurementString, 'f')
			value = float(transform)
			list.append(value)
			measurementString = v['elisaEmoVec']['Fear']
			transform = format(measurementString, 'f')
			value = float(transform)
			list.append(value)
			measurementString = v['elisaEmoVec']['Happiness']
			transform = format(measurementString, 'f')
			value = float(transform)
			list.append(value)
			measurementString = v['elisaEmoVec']['Neutral']
			transform = format(measurementString, 'f')
			value = float(transform)
			list.append(value)	
			measurementString = v['elisaEmoVec']['Sadness']
			transform = format(measurementString, 'f')
			value = float(transform)
			list.append(value)
			measurementString = v['elisaEmoVec']['Surprise']
			transform = format(measurementString, 'f')
			value = float(transform)
			list.append(value)
			
			if ofWhat == "Anger":
				measurementString = v['elisaEmoVec']['Anger']
				transform = format(measurementString, 'f')
				value = float(transform)
				if(value==max(list)):
					countEmoBeingMax = countEmoBeingMax + 1 
				countTotal = countTotal + 1
			if ofWhat == "Disgust":
				measurementString = v['elisaEmoVec']['Disgust']
				transform = format(measurementString, 'f')
				value = float(transform)
				if(value==max(list)):
					countEmoBeingMax = countEmoBeingMax + 1 
				countTotal = countTotal + 1
			if ofWhat == "Fear":
				measurementString = v['elisaEmoVec']['Fear']
				transform = format(measurementString, 'f')
				value = float(transform)
				if(value==max(list)):
					countEmoBeingMax = countEmoBeingMax + 1 
				countTotal = countTotal + 1
			if ofWhat == "Happiness":
				measurementString = v['elisaEmoVec']['Happiness']
				transform = format(measurementString, 'f')
				value = float(transform)
				if(value==max(list)):
					countEmoBeingMax = countEmoBeingMax + 1 
				countTotal = countTotal + 1
			if ofWhat == "Neutral":
				measurementString = v['elisaEmoVec']['Neutral']
				transform = format(measurementString, 'f')
				value = float(transform)
				if(value==max(list)):
					countEmoBeingMax = countEmoBeingMax + 1 
				#else:
				#	print 'once: '
				#	print value
				#	print max(list)
				#	print list
				countTotal = countTotal + 1
			if ofWhat == "Sadness":
				measurementString = v['elisaEmoVec']['Sadness']
				transform = format(measurementString, 'f')
				value = float(transform)
				if(value==max(list)):
					countEmoBeingMax = countEmoBeingMax + 1 
				countTotal = countTotal + 1
			if ofWhat == "Surprise":
				measurementString = v['elisaEmoVec']['Surprise']
				transform = format(measurementString, 'f')
				value = float(transform)
				if(value==max(list)):
					countEmoBeingMax = countEmoBeingMax + 1 
				countTotal = countTotal + 1
		except KeyError:
			print "KeyError detected. Ignoring the value... Explanation: "
			print v
	if countTotal == 0:
		ret = 0
	else:
		ret = countEmoBeingMax / countTotal
	return round(ret, 1)
	
#def printHTMLasPDF(html):
#	import pydf
#	try:
#		pdf = pydf.generate_pdf('<h1>this is html</h1>')
#		with open('test_doc.pdf', 'wb') as f:
#			f.write(pdf)
#		
#	except Exception, e:
#		print 'Exception: '+ str(e)
#	return 0

def getWordcloud(sentenceList):
	print "The sentence list contains " + str(len(sentenceList)) + " records."

	textCloud = ""

	i = 0
	for v in sentenceList:
		sent = v['lines'][0]
		sent = removeAdditionalStopwords(sent.lower()) # we may want to remove standard recruiting terminology
		textCloud = textCloud + sent
    # Generate a word cloud image
	if len(textCloud) < 1:
		imageFilePath="not_enough_data.png"
	else:
		wordcloud = WordCloud(background_color='white').generate(textCloud)

		# Display the generated image:
		# the matplotlib way:
		import matplotlib.pyplot as plt
		plt.imshow(wordcloud, interpolation='bilinear')
		plt.axis("off")
		
		imageFilePath = "clouds/wcloud_" + strftime("%Y_%m_%d_%H_%M_%S", gmtime()) + ".png"

		#try:
		#	os.remove(imageFilePath)
		#except OSError:
		#	pass
		plt.tight_layout(pad=0)
		plt.savefig("static/" + imageFilePath)
		#plt.show()
	return imageFilePath
	
def format_date_string(unformatted_date):
    formatted_date = ""
    year = unformatted_date[unformatted_date.rfind(".")+1:]
    month = unformatted_date[unformatted_date.rfind(".", 0, unformatted_date.rfind("."))+1:unformatted_date.rfind(".")]
    month = month.zfill(2)
    day = unformatted_date[:unformatted_date.find(".")]
    day = day.zfill(2)
    formatted_date_key = year + month + day
    return formatted_date_key
	
def removeAdditionalStopwords(text):
    text_file = open("additional_stopwords.txt", "r")
    stopwords = text_file.readlines()
    for a in stopwords:
        text = text.replace(a.lower().rstrip(), '')
    return text	
#filteredList = returnJSONobjectsFilteredDownByQuartile(sentenceList, '20141')
#print getMax(filteredList, 'positive_sentiment')

#searchProcedure('margins', True)

#mydict = quartileDictionary(2008, 2012)
#for key in sorted(mydict.iterkeys()):
#    print "%s: %s" % (key, mydict[key])