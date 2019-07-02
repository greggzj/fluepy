# http://www.dabeaz.com/coroutines/
# Example from A Curious Course on Coroutines and Concurrency

import xml.sax

'''
假设我们想完成解析一段XML成为json格式并过滤相应的数据：

原始数据：
<?xml version="1.0"?>
<buses>
    <bus>
        <id>7574</id>
        <route>147</route>
        <color>#3300ff</color>
        <revenue>true</revenue>
        <direction>North Bound</direction>
        <latitude>41.925682067871094</latitude>
        <longitude>-87.63092803955078</longitude>
        <pattern>2499</pattern>
        <patternDirection>North Bound</patternDirection>
        <run>P675</run>
        <finalStop><![CDATA[Paulina & Howard Terminal]]></finalStop>
        <operator>42493</operator>
        </bus>
        <bus>
        ...
    </bus>
</buses>

完成的功能比如：
<bus>
    <id>7574</id>
    <route>147</route>
    <revenue>true</revenue>
    <direction>North Bound</direction>
    ...
</bus>

转换为：
{
    'id' : '7574',
    'route' : '147',
    'revenue' : 'true',
    'direction' : 'North Bound'
    ...
}
'''



# xml.sax是一个解析xml的框架，用户继承xml.sax.ContentHandler,实现startElement、characters
# 和endElement， sax就会在对应的场景中通过事件驱动来调用对应的函数
# 使用coroutine来处理解析xml能够很好地增加可读性和程序运行速度，将class中处理事件的三个
# 不同函数合并到一个状态机函数中
class EventHandler(xml.sax.ContentHandler):
    def __init__(self, target):
        self.target = target
    def startElement(self, name, attrs):
        self.target.send(('start', (name, attrs._attrs)))
    def characters(self, content):
        self.target.send(('text', content))
    def endElement(self, name):
        self.target.send(('end', name))

# decorator, prime first node in coroutine automatically
def coroutine(func):
    def start(*args, **kwargs):
        cr = func(*args, **kwargs)
        cr.next()
        return cr
    return start

@coroutine
def buses_to_dicts(target):
    '''
    本函数完成将xml解析成Json功能。

    本函数实际上是一个状态机处理函数，两个yield分别代表对两个状态的处理
    状态A：look for a bus
    状态B：Collecting bus attributes
    '''
    while True:
        event, value = (yield)
        # Look for the start of a <bus> element
        if event == 'start' and value[0] == 'bus':
            busdict = {}
            fragments = []
            # Capture text of inner elements in a dict
            while True:
                event, value = (yield)
                if event == 'start':    fragments = []
                elif event == 'text':   fragments.append(value)
                elif event == 'end':
                    if value != 'bus':
                        busdict[value] = "".join(fragments)
                    else:
                        target.send(busdict)
                        break


@coroutine
def filter_on_field(fieldname, value, target):
    '''
    过滤generator(coroutine)。

    如果fieldname存在并且对应的value也一致，调用target.send将数据传递给其target
    generator
    
    嵌套使用该函数相当于一直累加过滤条件。

    Example:
        filter_on_field("route","22",target)
        filter_on_field("direction","North Bound",target)
    '''
    while True:
        d = (yield)
        if d.get(fieldname) == value:
            target.send(d)


@coroutine
def bus_location():
    while True:
        bus = (yield)
        print ("%(route)s,%(id)s,\"%(direction)s\","\
                "%(latitude)s,%(longitude)s" % bus)


'''
把上面所有的都hook起来：

EventHanlder中注册buses_to_dicts，读取xml后进入buses_to_dicts状态机处理，将xml
解析成对应Json后调用target.send(busdict)将解析后的json字典发送给第一个filter_on_field
进行数据过滤。

第一个filter_on_field过滤是否存在{"route": 22}这个Key/value对，如果有，那么调用target.send(d)
继续将json字典发送给第二个filter_on_field过滤是否存在{"direction": "North Bound"}，如果有，那么调用
target.send(d)将json字典发给bus_location，由bus_location来打印最终满足条件过滤后的json字典

'''
xml.sax.parse("abc.xml",
              EventHandler(
                  buses_to_dicts(
                      filter_on_field("route", "22",
                      filter_on_field("direction", "North Bound", 
                      bus_location()))
                  )
              ))