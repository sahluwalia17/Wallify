import random

test = None

def asd():
	if(random.randrange(10) < 5):
		try:
			global test
			test = "1-5"
		except Exception as e:
			print (e)
	else:
		try:
			#global test
			test = "6-10"
		except Exception as e:
			print (e)
def main():
	if test == None:
		print ("here")
	asd()
	if test != None:
		print (test)

if __name__ == "__main__":
	main()