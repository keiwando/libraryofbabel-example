#This is just meant to be an example to show how the Library of Babel (libraryofbabel.info) algorithm works 
#in its core (especially the search). I am not saying that this is the exact 
#algorithm that Jonathan Basile has implemented (obviously it isn't) but I'm just trying 
#to provide an example for those who don't believe that this actually works and think the search is a hoax.
#For this, I also don't consider the structure of the rooms - the addresses could be considered as roomnumbers without
#a wall/shelf/volume number - since the way you interpret the address does not change the basic idea of how this works in general.
#You can think of this as a library with 1 book containing all the pages (and the address being the page number)
#This algorithm is purely based on a linear congruential generator
#more steps can be added inbetween for achieving more 'randomness'
#The LCG is what enables "searchability"

from random import randint
import Euclid

ALPHABET = "abcdefghijklmnopqrstuvwxyz,. "
ADDRESSCHARSET = "0123456789abcdefghijklmnopqrstuvwxyz"

def generateRandomPage():
	page = ""
	for i in range(0,3200):
		page += ALPHABET[randint(0,28)]

	return page

def generateRandomAddress():
	length = randint(0,3260)
	address = ""
	for i in range(0,length):
		address += ADDRESSCHARSET[randint(0,35)]

	return address

def generateAllSpacePage():
	#this would be the 'last page if they were in order so it helps us calculate the
	#MOD for the LCG
	page = ""
	for i in range(0,3200):
		page += " "

	return page

def fillWithXBefore(text,x,length):
	diff = length - len(text)
	for i in range(0,diff):
		text = x + text
	return text

def fillWithXAfter(text,x,length):
	diff = length - len(text)
	for i in range(0,diff):
		text = text + x
	return text

def convertNumberToString(number,characterset):
	base = len(characterset)
	output = ""
	digits = list(characterset)

	if number == 0:
		return "a"

	currentNumber = number

	while currentNumber != 0:
		remainder = currentNumber % base 
		output += digits[remainder]
		currentNumber = currentNumber / base

	result = output[::-1]

	if number < 0:
		result = "-" + result

	return result

def convertStringToNumber(text,characterset):
	base = len(characterset)

	result = 0
	multiplier = 1

	for i in range(len(text)-1,-1,-1):
		c = text[i]

		if i == 0 and c == '-':
			result = -result
			break

		digit = characterset.index(c)
		result += digit * multiplier
		multiplier *= base

	return result

def testConversion(number,text):
	#both outputs should be true
	print convertStringToNumber(convertNumberToString(number,ALPHABET),ALPHABET) == number
	print convertNumberToString(convertStringToNumber(text,ALPHABET),ALPHABET) == text

def calculateMOD():
	lastPage = generateAllSpacePage()
	MOD = convertStringToNumber(lastPage,ALPHABET)
	return MOD


#Parameters for the LCG
MOD = calculateMOD()
C = 982451653			#MOD and C are relatively prime
A = MOD + 1
AINV = Euclid.modinv(A,MOD)


def lcg(x):
    return ((A * x + C) % MOD)

def lcgInverse(x):
    return ((AINV * (x - C)) % MOD)


def pageAtAddress(address):
	addressAsNumber = convertStringToNumber(address,ADDRESSCHARSET)
	pageAsNumber = lcg(addressAsNumber)
	page = convertNumberToString(pageAsNumber,ALPHABET)
	page = fillWithXBefore(page,'a',3200)
	return page

def addressOfPage(page):
	#aka 'THE SEARCH'
	pageAsNumber = convertStringToNumber(page,ALPHABET)
	addressAsNumber = lcgInverse(pageAsNumber)
	address = convertNumberToString(addressAsNumber,ADDRESSCHARSET)
	return address

def searchForTextExact(text):
	page = fillWithXAfter(text," ",3200)
	return addressOfPage(page)

def searchForTextWithinOtherCharacters(text):
	diff = 3200 - len(text)
	before = randint(0,diff)
	for i in range(0,before):
		text = ALPHABET[randint(0,28)] + text 
	if len(text) < 3200:
		for i in range (0,3200-len(text)):
			text = text + ALPHABET[randint(0,28)]

	
	page = text

	return addressOfPage(page)

def searchForText(text,exact):
	text = text.lower()	#make sure everything is in lowercase
	address = 0
	if exact:
		address = searchForTextExact(text)
	else:
		address = searchForTextWithinOtherCharacters(text)

	print "The text you were looking for can be found on page/at address:", address
	print
	print "THE PAGE:"
	print pageAtAddress(address)



def testLibrary():
	#returns true if the library works

	page = generateRandomPage()
	address = addressOfPage(page) #search for the page in the library
	pageAtLocation = pageAtAddress(address)	#get the page at that address
	return page == pageAtLocation	#check if both are equal	(the other way around does not necessarily work since the pages repeat)

def testLibraryAutomated():
	print "testing"
	for i in range (0,100):
		if not testLibrary():
			print "error"
			return

	print "works"

#testLibraryAutomated()
#searchForText("Enter any text you want to search for here",True)	#True = exact search, False = text within other caracters
#searchForText("              Your Text                   ",False)	#putting spaces before and after your text makes it easier to locate on a page






