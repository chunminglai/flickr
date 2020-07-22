# coding: utf-8
import flickrapi
import simplejson as json
import time
import csv
# global constants
api_key = u'19d8657e49a7f6c41117843ddecaa8c2'
api_secret = u'996e2f199f913380'
flickr = flickrapi.FlickrAPI(api_key, api_secret)
#定義函數-確認資料數量
def check(lx,ly,ux,uy,year):
	l_x=lx
	_l_x=str(l_x)
	l_y=ly
	_l_y=str(l_y)
	u_x=ux
	_u_x=str(u_x)
	u_y=uy
	_u_y=str(u_y)
	t=year
	_t=str(t)
	_bbox=str(_l_x+","+_l_y+","+_u_x+","+_u_y)
	response = flickr.photos.search(bbox=_bbox,per_page ="200",min_taken_date=_t+"-01-\
01",max_taken_date=_t+"-12-31",has_geo=1,extras='owner_name, geo, date_taken, tags',format="json")
	data = json.loads(response.decode('utf-8'))
	u=int(data["photos"]["total"])
	print(u)

check(121.534996,25.0218,121.5351,25.0219,2005)

def mining(lx,ly,ux,uy,year):
	l_x=lx
	_l_x=str(l_x)
	l_y=ly
	_l_y=str(l_y)
	u_x=ux
	_u_x=str(u_x)
	u_y=uy
	_u_y=str(u_y)
	t=year
	_t=str(t)
	_bbox=str(_l_x+","+_l_y+","+_u_x+","+_u_y)
#確定範圍是否>4000
	time.sleep(1)
	response = flickr.photos.search(bbox=_bbox,per_page ="200",min_taken_date=_t+"-01-\
01",max_taken_date=_t+"-12-31",has_geo=1,extras='owner_name, geo, date_taken, tags',format="json")
	data = json.loads(response.decode('utf-8'))
	pages=int(data["photos"]["pages"])
	print(pages)
	u=int(data["photos"]["total"])
	print(u)
	try:
		if u>3999:
		#切成四格
			x_leng=u_x-l_x
			y_leng=u_y-l_y
			x_half=x_leng/2
			y_half=y_leng/2
#判斷經緯度
			if x_leng>0.0001and y_leng>0.0001:
				one_x=l_x;one_y=l_y
				two_x=l_x+x_half;two_y=l_y
				three_x=l_x;three_y=l_y+y_half
				four_x=l_x+x_half;four_y=l_y+y_half
				five_x=four_x+x_half;five_y=four_y
				six_x=four_x;six_y=four_y+y_half
				seven_x=four_x+x_half;seven_y=four_y+y_half

				mining(one_x,one_y,four_x,four_y,t);mining(two_x,two_y,five_x,five_y,t);mining(three_x,three_y,six_x,six_y,t);mining(four_x,four_y,seven_x,seven_y,t)
			else:
				bbox_list.append(_bbox)
		else:
			#執行抓取
			photo_list=[["photoID","userID","onername","taken_time","latitude","longitude","tags"]]
			for i in range(1,pages+1):
				_page=str(i)
				response = flickr.photos.search(bbox=_bbox,page=_page,per_page="200",min_taken_date=_t+"-01-01",max_taken_date=_t+"-12-31",has_geo=1,extras='owner_name, geo,\
date_taken, tags',format="json")
				data = json.loads(response)
				for aa in data["photos"]["photo"]:
					photo_list.append([aa['id'],aa["owner"],aa["ownername"].encode("utf8"),aa["datetaken"],aa['latitude'],aa['longitud\
e'],aa["tags"].encode("utf8")])
					t_l_check.append(str(aa["datetaken"])+str(aa['latitude'])+str(aa['longitude']))
					idcheck.append(aa['id'])
				w = csv.writer(f)
				w.writerows(photo_list)
				all_list.append(photo_list)
				print ("目前抓到",len(idcheck))
				photo_list=[]
				time.sleep(1)
	except:
		error_bbox_list.append(_bbox)
		print("error")
error_bbox_list=[]
idcheck=[]
t_l_check=[]
all_list=[]
bbox_list=[]
f = open(str(2005)+".csv","w")
mining(121.534996,25.0218,121.5351,25.0219,2005)
# 抓取資料
# 選擇要抓取的年份
'''
year_list=[2001,2002,2003,2004,2005,2006,2007,2008,2009,2010,2011,2012,2013,2014,2015]
year_list=[2005]
for s_year in year_list:
#設定年度
year=s_year
#確認資料此年度之總數
check(121.454,24.957,121.670,25.213,year)
for s_year in year_list:
#設定年度

	year=s_year
	print(year)
#確認資料此年度之總數
check(121.454,24.957,121.670,25.213,year)
#宣告 list
idcheck=[]
t_l_check=[]
all_list=[]
bbox_list=[]
error_bbox_list=[]
f = open(str(year)+".csv","w")
# print (time.strftime("%H:%M:%S"))
mining(121.454,24.957,121.670,25.213,year)
f.close()
# print (time.strftime("%H:%M:%S"))
print "ID 總數:",len(idcheck),"不重複 ID 總數:",len(set(idcheck))
print "ID 總數相差:",len(idcheck)-len(set(idcheck))
print "時間+地點總數:",len(t_l_check),"不同時間或不同地點總數:",len(set(t_l_check))
print "時間+地點相差:",len(t_l_check)-len(set(t_l_check))
time.sleep(10)
print "error_area",error_bbox_list
print "need time split",bbox_list

time_split=[["neendtimesplit_error"]]
error_list=[["error_bbox"]]
for a in bbox_list:
b=a.split(",")
time_split.append(b)
for c in error_bbox_list:
d=c.split(",")
error_list.append(d)
f_error = open(str(year)+"_error.csv","w")
w_error = csv.writer(f_error)
w_error.writerows(time_split)
w_error.writerows(error_list)
f_error.close()
'''