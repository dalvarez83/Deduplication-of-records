import re
import xml.etree.ElementTree as et
from pathlib import Path


class Item:
    Id = 0
    Text = ''

    def __init__(self, id, text):
        self.Id = id
        self.Text = text


class ArabicSoundex:
    _asoundexCodes = []
    _aphonixCode = []
    _transliteration = []
    _map = []
    _len = 4
    _code = 'soundex'
    _lang = "en"

    # constructor
    def __init__(self, xml_file):
        xtree = et.parse(xml_file)
        xroot = xtree.getroot()
        for node in xroot.iter('asoundexCode'):
            for x in node:
                myobj = Item(x.attrib['id'], x.text)
                self._asoundexCodes.append(myobj)
        for node in xroot.iter('aphonixCode'):
            for x in node:
                myobj = Item(x.attrib['id'], x.text)
                self._aphonixCode.append(myobj)
        for node in xroot.iter('transliteration'):
            for x in node:
                myobj = Item(x.attrib['id'], x.text)
                self._transliteration.append(myobj)
        self._map = self._asoundexCodes

    # Set the length of soundex key (default value is 4)
    # @param intValue $integer Soundex key length

    def setLen(self, intValue):
        self._len = intValue

    # Set the language of the soundex key (default value is "en")
    # @param string strValue Soundex key language [ar|en]

    def setLang(self, strValue):
        self._lang = strValue

    # Set the mapping code of the soundex key (default value is "soundex")
    # @param string strValue Soundex key mapping code [soundex|phonix]

    def setCode(self, strValue):
        xx = strValue.lower()
        if (xx == 'soundex' or xx == 'phonix'):
            self._code = xx
            if (xx == 'phonix'):
                self._map = self._aphonixCode
            else:
                self._map = self._asoundexCodes

    def getLen(self):
        return self._len

    def getLang(self):
        return self._lang

    def getCode(self):
        return self._code

    def mapCode(self, word):
        encodedWord = ''
        for elem in word:
            matchingVals = [x for x in self._map if x.Text == elem]
            if (not matchingVals):
                encodedWord = encodedWord + "0"
            else:
                encodedWord = encodedWord + matchingVals[0].Id
        return encodedWord

    def trimRep(self, word):
        lastChar = ''
        cleanWord = ''
        # max = len(word)
        for elem in word:
            if (elem != lastChar):
                cleanWord += elem
            else:
                lastChar = elem
        return cleanWord

    def soundex(self, word):
        soundex = word[0]
        if (self._lang == 'en'):
            matchingVals = [x for x in self._transliteration if x.Id == soundex]
            if (not matchingVals):
                soundex = ''
            else:
                soundex = matchingVals[0].Text
        # rest = word[1:len(word)]
        encodedRest = self.mapCode(word)
        cleanEncodedRest = self.trimRep(encodedRest)
        soundex += cleanEncodedRest
        soundex = soundex.replace("0", "")
        totalLen = len(soundex)
        if (totalLen > self._len):
            soundex = soundex[0:self._len]
        else:
            soundex += '0' * (self._len - totalLen)
        return soundex

    def arabicFixConfusingLettersKey(self, word):
        result = ''
        result = word.replace(" ", "")
        result = result.replace("أ", "ا")
        result = result.replace("آ", "ا")
        result = result.replace("ى", "ا")
        result = result.replace("ؤ", "ا")
        result = result.replace("إ", "ا")
        result = result.replace("ئ", "ا")
        result = result.replace("ة", "ه")
        result = result.replace("ص", "س")
        result = result.replace("ض", "د")
        result = result.replace("ث", "ت")
        result = result.replace("ذ", "ز")
        result = result.replace("ق", "ك")
        result = result.replace("ح", "ه")
        result = re.sub('[^A-Za-zا-ي]+', '', result)
        return result


absPath = Path(__file__).parent / 'ArSoundex.xml'

arabicSoundex = ArabicSoundex(absPath)
