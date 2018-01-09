# coding: utf-8
  
import urllib2  
import hashlib  
import json  
import random  
  
  
class Baidu_Translation:  
    def __init__(self):  
        self._q = 'Welcome'  
        self._from = 'zh'
        self._to = 'en'
        self._appid = 2018010900xxxxx
        self._key = 'WlB9BcKQ8Rp********'
        self._salt = random.randint(10001,99999)
        self._sign = ''
        self._dst = ''
        self._enable = True  
          
    def GetResult(self, queryStr=''):  
        
        queryStr = queryStr.replace(' ', '')
        #print queryStr
        queryStr.encode('utf8') 

        m = str(self._appid) + queryStr + str(self._salt) + self._key  
        m_MD5 = hashlib.md5(m)  
        self._sign = m_MD5.hexdigest()          
        Url_1 = 'http://api.fanyi.baidu.com/api/trans/vip/translate?'  
        Url_2 = 'q='+queryStr+'&from='+self._from+'&to='+self._to+'&appid='+str(self._appid)+'&salt='+str(self._salt)+'&sign='+self._sign  
        Url = Url_1+Url_2  
        PostUrl = Url.decode()  
        TransRequest = urllib2.Request(PostUrl)  
        TransResponse = urllib2.urlopen(TransRequest, timeout=10)  
        TransResult = TransResponse.read()  
        data = json.loads(TransResult)  
        if 'error_code' in data:  
            print 'Crash'  
            print 'error:',data['error_code'], data['error_msg']  
            return '*err*'
        else:  
            self._dst = data['trans_result'][0]['dst']  
            return self._dst  
  
    def ShowResult(self,result):  
        print result  
          
    def Welcome(self):  
        self._q = 'Welcome to use icedaisy online translation tool'  
        self._from = 'auto'  
        self._to = 'zh'  
        self._appid = 20180109000113413  
        self._key = 'WlB9BcKQ8Rp2bT8CyvAG'  
        self._salt = random.randint(10001,99999)  
        welcome = self.GetResult()  
        self.ShowResult(welcome)  
          
    def StartTrans(self):  
        while self._enable:  
            self._q = raw_input()  
            if cmp(self._q, '!quit') == 0:  
                self._enable = False  
                print 'Thanks for using!'  
                break  
            _q_len = len(self._q)  
            if _q_len < 4096:  
                result = self.GetResult()  
                self.ShowResult(result)  
            else:  
                print 'Exceeds the maximum limit of 4096 characters'  
  