##Code to run download episodes locally

##install chrome or chromium-browser and respective driver
##install requirements_forlocal file requirements using "sudo pip3 install -r requirements_forlocal.txt"


#importing the modules
from  bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import requests as r
import threading
import time
import os

#define the required things below
anime_name = "HighschoolDxD"
url = "https://gogo-stream.com/videos/high-school-dxd-episode-"   #url without episode episode number in str 
no_of_eposides = 12       #no of episodes in anime to download
download_floder = "videos/"+anime_name+"/"  #change not needed
chrome_binary_path = "chromedriverpath/chromedriver" # for colab use chrome driver

#defining the thread function
def thread_call(list):
	options = webdriver.ChromeOptions()
	options.add_argument('--no-sandbox')
	options.add_argument('--headless')
	options.add_argument('--disable-dev-shm-usage')
	d = webdriver.Chrome(executable_path=chrome_binary_path, options=options)  #for local
	print(list)
	first = 1
	for i in list:
		res = r.get(url+str(i))
		print("requested")
		soup = bs(res.text,'html.parser')
		print("loading link")
		d.get("http:"+soup.find("iframe")['src'])
		time.sleep(2)
		if (first == 1):
			print("clicking on empty space")
			d.find_element_by_xpath("//body").click()
			print("switching to add")
			d.switch_to.window(d.window_handles[1])
			print("closing add")
			d.close()
			print("Going to main window")
			d.switch_to.window(d.window_handles[0])
		d.find_element_by_xpath("/html/body/div/div/div[3]/div[2]/div[12]/div[1]/div/div/div[2]/div").click()
		time.sleep(1)
		print("getting link")
		durl = d.find_element_by_xpath("/html/body/div/div/div[3]/div[2]/div[4]/video")
		dlink = durl.get_attribute("src")
		print(dlink)
		print('downloading and saving the file')
		data = r.get(dlink)
		with open(download_floder+anime_name+"-ep"+str(i)+".mp4","wb") as f:
			f.write(data.content)
			print("downloaded "+anime_name+"-"+str(i)+".mp4")
		first = 0
	d.quit()

#making the directory to download the episodes if not exists
if not os.path.exists(download_floder):
    os.makedirs(download_floder)

#creating the list by considering number of episodes
ls = no_of_eposides
l = []
for i in range(ls):
	l.append(i+1)
n = int(input("No of Threads to run :  ")) #input the number of threads to run, define number of threads based on bandwidth
splited = []
len_l = len(l)
for i in range(n):
	start = int(i*len_l/n)
	end = int((i+1)*len_l/n)
	splited.append(l[start:end])
print(splited)
t1 = time.perf_counter()

#Creating the threads and starting the threads
threads = []
for sub_list in splited:
	t = threading.Thread(target=thread_call, args=[sub_list])
	t.start()
	threads.append(t)

#waiting untile all the threads done executing
for thread in threads:
	thread.join()
t2 = time.perf_counter()
for _ in range(10):
  print("*"*300)
print(f"Time took to download is : {round(t2-t1,2)}")
#checking if all the episodes are downloaded
count = 0
for i in range((no_of_eposides)):
	if not os.path.exists(download_floder+anime_name+"-ep"+str(i+1)+".mp4"):
		print("The episode not downloaded : "+str(i+1))
		count = count+1
print("number of undownloaded episodes : "+str(count))