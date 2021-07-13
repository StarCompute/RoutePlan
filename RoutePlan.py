import urllib3
import json
import random
import time


# 请到高德开发平台获取key
appkey='xxxxxx'

def getUrl(url):
    http=urllib3.PoolManager()
    r=http.request('get',url)
    if r.status==200:
        return r.data
    return ''


def getGeoFromAddress(address):
    url1='https://restapi.amap.com/v3/geocode/geo?'+'key='+appkey+'&output=json'
    url=url1+'&address='+address
    data=getUrl(url)
    # print(data)
    return json.loads(str(data.decode('utf-8')))

def test_getGeoFromAddress():
    httpData=getGeoFromAddress('深圳市XX街道xx')
    httpData=getGeoFromAddress('深圳市福田区市民中心')
    print(httpData['geocodes'][0]['location'])


def getDrivePlan(origin,destination):
    url1='https://restapi.amap.com/v3/direction/driving?'+'key='+appkey+'&output=json'
    url=url1+'&show_fields=cost&strategy=10&extensions=all&origin='+str(origin['lng'])+','+str(origin['lat'])+'&destination='+str(destination['lng'])+','+str(destination['lat'])
    data=getUrl(url)
    # print(data)
    return json.loads(str(data.decode('utf-8')))

# 上面的getDrivePlan和本函数都是获取驾驶路线规划的，一个V3,一个V5,返回的数据方式不同，调用次数限制不同，请采用V3
def getDrivePlanV5(origin,destination):
    url1='https://restapi.amap.com/v5/direction/driving?'+'key='+appkey+'&output=json'
    url=url1+'&show_fields=cost&strategy=1&extensions=all&origin='+str(origin['lng'])+','+str(origin['lat'])+'&destination='+str(destination['lng'])+','+str(destination['lat'])
    data=getUrl(url)
    # print(data)
    return json.loads(str(data.decode('utf-8')))

# 请替换下面的city,city1,city2为你所在城市的电话区号
def getBusPlan(origin,destination):
    url1='https://restapi.amap.com/v3/direction/transit/integrated?'+'key='+appkey+'&output=json'
    url=url1+'&city=0755&city1=0755&city2=0755&strategy=1&extensions=all&show_fields=cost&origin='+str(origin['lng'])+','+str(origin['lat'])+'&destination='+str(destination['lng'])+','+str(destination['lat'])
    data=getUrl(url)
    # print(data)
    return json.loads(str(data.decode('utf-8')))

# 获取电动自行车的线路规划
def getBikePlan(origin,destination):
    url1='https://restapi.amap.com/v5/direction/electrobike?'+'key='+appkey+'&output=json'
    url=url1+'&show_fields=cost&origin='+str(origin['lng'])+','+str(origin['lat'])+'&destination='+str(destination['lng'])+','+str(destination['lat'])
    data=getUrl(url)
    # print(data)
    return json.loads(str(data.decode('utf-8')))

def compareBusAndDrive(origin,destination):
    
    minDriveTime=1000
    minDriveTimeV5=1000
    minDistance=1000
    minBusTime=1000
    minBikeTime=1000

    r=getDrivePlan(origin,destination)
    if 'route' in r:
        for p in (r['route']['paths']):
            distance=round(float(p['distance'])/1000,3)
            costTime=round(float(p['duration'])/60.0,2)
            if minDriveTime>costTime: minDriveTime=costTime
            if minDistance>distance: minDistance=distance
            # print(distance,costTime)
        # print(minDrivePath)
    else :minDriveTime=-1

    r=getDrivePlanV5(origin,destination)
    if 'route' in r:
        for p in (r['route']['paths']):
            distance=round(float(p['distance'])/1000,3)
            costTime=round(float(p['cost']['duration'])/60.0,2)
            if minDriveTimeV5>costTime: minDriveTimeV5=costTime
            if minDistance>distance: minDistance=distance
            # print(distance,costTime)
        # print(minDrivePath)
    else :minDriveTimeV5=-1

    r=getBikePlan(origin,destination)
    if 'route' in r:
        for p in (r['route']['paths']):
            distance=round(float(p['distance'])/1000,3)
            _costTime=0
            for s in p['steps']:
                _costTime=_costTime+int(s['cost']['duration'])
            costTime=round(float(_costTime)/60.0,2)
            if minBikeTime>costTime: minBikeTime=costTime
            if minDistance>distance: minDistance=distance
            # print(distance,costTime)
        # print(minDrivePath)
    else :minBikeTime=-1

    r=getBusPlan(origin,destination)
    if 'route' in r:
        for p in (r['route']['transits']):
            distance=round(float(p['distance'])/1000,3)
            # costTime=round(float(p['cost']['duration'])/60.0,2)
            costTime=round(float(p['duration'])/60.0,2)
            if minBusTime>costTime: minBusTime=costTime
            if minDistance>distance: minDistance=distance
    else:minBusTime=-1
    print(origin,destination,minDistance,minDriveTime,minDriveTimeV5,minBusTime,minBikeTime)
    # print(origin,destination,minDistance,minDriveTime,minBusTime,minBikeTime)
    time.sleep(1)

location_from=dict()
location_from['lng']=114.017xxx
location_from['lat']=22.726xxx

location_to=dict()
location_to['lng']=114.059616
location_to['lat']=22.543672
location_rand=dict()
location_rand['lat']=round(random.uniform(location_from['lat'], location_to['lat']),6)
location_rand['lng']=round(random.uniform(location_from['lng'], location_to['lng']),6)



# 随机获取499份数据
for i in range(1,500):
    location_rand['lat']=round(random.uniform(location_from['lat'], location_to['lat']),6)
    location_rand['lng']=round(random.uniform(location_from['lng'], location_to['lng']),6)
    compareBusAndDrive(location_from,location_rand)
 
