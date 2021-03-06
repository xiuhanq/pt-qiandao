import json
from logging import debug, log
from loguru import logger
from selenium.webdriver.common.by import By
from utils.Captcha import Captcha
from utils.SiteResultInfo import SiteResultInfo
import time
import re

logger.add('pt-qiandao.log', format='{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}',encoding='utf-8')

class DefaultSite(object):
    def __init__(self,driver,site_config):
        self._driver=driver
        self._site_config=site_config

    def check_elementExists(self,xpath):
        # 从selenium.common.exceptions模块导入NoSuchElementException异常类
        from selenium.common.exceptions import NoSuchElementException
        driver = self._driver
        try:
            time.sleep(5)
            element = driver.find_element(By.XPATH, xpath)
        except NoSuchElementException as e:
            # logger.warning('没有获取到元素:{}',xpath)
            # logger.exception(e)
            # 发生了NoSuchElementException异常，说明页面中未找到该元素，返回False
            return False
        else:
            # 没有发生异常，表示在页面中找到了该元素，返回True
            return True
    
    def do_login(self):
        site_config = self._site_config
        site_name = site_config.get('site_name')
        username = site_config.get('username')
        password = site_config.get('password')
        cookies = site_config.get('cookies')
        if username is not None and password is not None :
            logger.debug("站点【{}】使用用户名密码登录",site_name)
            return self.do_login_unamepass()
        elif cookies is not None :
            logger.debug("站点【{}】使用Cookies登录",site_name)
            return self.do_login_cookies()
        else:
            logger.debug("站点【{}】没有配置用户名密码或者Cookies,无法登录",site_name)
            return False

    def get_cookies(self):
        site_config = self._site_config
        site_name = site_config.get('site_name')
        cookies_path = site_config.get('cookies_path')
        cookies_file_paht = cookies_path+site_config.get('cookies')
        # open方法打开直接读出来
        file = open(cookies_file_paht, 'r', encoding='utf-8')
        # 读出来是字符串
        cookies_str = file.read()
        cookies_list = json.loads(cookies_str)
        # logger.debug('站点【{}】 cookies:{}',site_name,cookies_list)
        return cookies_list

    def do_login_cookies(self):
        site_config = self._site_config
        site_name = site_config.get('site_name')
        login_url = site_config.get('login_url')
        index_url = site_config.get('index_url')
        index_url_str = site_config.get('index_url_str')
        logger.debug('登录地址:{}',login_url)
        login_result = False
        logger.debug('开始使用Cookies登录:{} =====>>',site_name)
        driver = self._driver
        cookies_list = self.get_cookies()
        driver.delete_all_cookies()
        driver.get(login_url)
        for cookie in cookies_list:
            # logger.debug("cookie:{}",cookie)
            #遍历删除sameSite,注意，旧版chrome可能是没有samesite
            try:
                cookie.pop('sameSite')
            except:
                pass
            driver.add_cookie(cookie)
        
        for i in range(1,10):
            logger.debug('第{}次尝试登录:{}',i,site_name)
            driver.get(index_url)
            current_url = driver.current_url
            if current_url.find(index_url_str)>0:
                login_result = True 
                break
            else:
                time.sleep(2)
        return login_result

    def do_login_unamepass(self): 
        site_config = self._site_config
        driver = self._driver
        site_name = site_config.get('site_name')
        logger.debug('开始使用账号密码登录:{} =====>>',site_name)
        index_url = site_config.get('index_url')
        login_url = site_config.get('login_url')
        index_url_str = site_config.get('index_url_str')
        login_url_str = site_config.get('login_url_str')
        username_input_xpath = site_config.get('username_input_xpath')
        password_input_xpath = site_config.get('password_input_xpath')
        submit_btn_xpath = site_config.get('submit_btn_xpath')
        username = site_config.get('username')
        password = site_config.get('password')

        logger.debug('首页地址:{}',index_url)
        login_result = False
        for i in range(1,10):
            logger.debug('第{}次尝试登录:{}',i,site_name)
            driver.get(login_url)
            current_url = driver.current_url
            logger.debug('当前登录url:{}',str(current_url))
            if current_url.find(login_url_str)>0:       
                username_input=driver.find_element(By.XPATH,username_input_xpath)
                logger.debug('开始输入站点: {} ,用户名:{}',site_name,username)
                username_input.send_keys(username)
                password_input=driver.find_element(By.XPATH,password_input_xpath)
                logger.debug('开始输入站点: {} ,密码:',site_name)
                password_input.send_keys(password)                
                if self.do_login_captcha() == False:
                    continue
                submit_button=driver.find_element(By.XPATH,submit_btn_xpath)      
                submit_button.click()
                current_url = driver.current_url
                logger.debug('登录后当前url:{}',str(current_url))
                if current_url.find(index_url_str)>0:
                    login_result = True
            if login_result :
                break
        logger.debug('登录完成:{},结果:{} <<=====',site_name,login_result)
        return login_result
    
    def do_login_captcha(self): 
        logger.debug('开始处理登录验证码')
        site_config = self._site_config
        driver = self._driver
        site_name = site_config.get('site_name')
        result = False
        if site_config.get('login_image_captcha_xpath') is not None:           
            if self.check_elementExists(site_config.get('login_image_captcha_xpath'))==True:
                image_captcha = driver.find_element(By.XPATH,site_config.get('login_image_captcha_xpath')) 
                if image_captcha.is_displayed() == True:
                    captcha = Captcha(driver,site_config.get('image_captcha_save_path'),site_config.get('login_image_captcha_xpath'))
                    captcha_str = captcha.image_text()
                    captcha_len = len(captcha_str)
                    verify_len = int(site_config.get('login_captcha_length'))
                    logger.debug('站点:{},验证码:{},验证码长度:{},有效长度:{}',site_name, captcha_str,captcha_len,verify_len)
                    if captcha_len != verify_len:
                        logger.debug('{},登录验证码[{}]有误,重新刷新页面!',site_name,captcha_str)
                        return result
                    captcha_input = driver.find_element(By.XPATH,site_config.get('login_image_captcha_input_xpath')) 
                    captcha_input.send_keys(captcha_str)
                    result = True
                else:
                    logger.debug('验证码元素不展示,无需处理登录验证码')
                    result=True  
            else:
                logger.debug('验证码元素不存在,无需处理登录验证码')
                result=True
        else:
            logger.debug('无需处理登录验证码')
            result=True
        return result

    def do_attendance(self):
        site_config = self._site_config
        driver = self._driver
        site_name = site_config.get('site_name')
        attendance_result = False
        logger.debug('开始签到:{} =====>>',site_name)
        for i in range(1,10):
            logger.debug('开始尝试第{}次签到:{} =====>>',i,site_name)
            driver.get(site_config.get('index_url'))
            attendance_btn_xpath = '' 
            if site_config.get('attendance_btn_xpath') is not None:
                attendance_btn_xpath = site_config.get('attendance_btn_xpath')
            if attendance_btn_xpath != '':
                # logger.debug('开始签到,attendance_btn_xpath:{}',attendance_btn_xpath)
                if self.check_attendance_result()==False:
                    attendance_button = driver.find_element(By.XPATH,attendance_btn_xpath)
                    attendance_button.click()
                    if self.do_attendance_captcha() == False:
                            continue
                    attendance_result = self.check_attendance_result()
                else:   
                    logger.debug('站点:{}无需签到或者已经完成签到',site_name)
                    attendance_result = True  
                    break   
            else:
                logger.debug('站点:{}无需签到',site_name)
                attendance_result = True
                break
            if attendance_result == True:
                break
        logger.debug('签到完成:{},结果:{}  <<=====',site_name,attendance_result)
        return attendance_result

    def do_attendance_captcha(self):
        logger.debug('开始处理签到验证码')
        return True

    def check_attendance_result(self):
        result = False    
        site_config = self._site_config
        driver = self._driver
        driver.refresh()
        index_btn_xpath = site_config.get('index_btn_xpath')
        index_btn = driver.find_element(By.XPATH,index_btn_xpath)
        index_btn.click()
        attendance_btn_xpath = site_config.get('attendance_btn_xpath')
        if self.check_elementExists(attendance_btn_xpath)==True:
            attendance_button = driver.find_element(By.XPATH,attendance_btn_xpath)
            btn_text = attendance_button.text
            logger.debug('签到按钮文本:{}',btn_text)
            if site_config.get('attendance_text') != btn_text:
                result = True
        else:
            result = True
        return result

    def get_attendance_result_text(self):
        site_config = self._site_config
        driver = self._driver
        site_name = site_config.get('site_name')
        logger.debug('开始获取站点【{}】签到结果',site_name)
        driver.refresh()
        index_btn_xpath = site_config.get('index_btn_xpath')
        index_btn = driver.find_element(By.XPATH,index_btn_xpath)
        index_btn.click()
        attendance_result_xpath = site_config.get('attendance_result_xpath')
        attendance_result_txt_matchType = site_config.get('attendance_result_txt_matchType')
        result_txt = ''
        if attendance_result_xpath is None:
            return result_txt
        # logger.debug('站点【{}】attendance_result_xpath:{}',site_name,attendance_result_xpath)
        
        if self.check_elementExists(attendance_result_xpath)==True:
            attendance_result_txt = driver.find_element(By.XPATH,attendance_result_xpath)
            result_txt = attendance_result_txt.text
            if attendance_result_txt_matchType == 1 :            
                p = re.compile(r'[(](.*?)[)]', re.S)           
                result_txt=re.findall(p, result_txt)[0]
            elif attendance_result_txt_matchType == 2 :
                p = re.compile(r'[\[](.*?)[]]', re.S)           
                result_txt=re.findall(p, result_txt)[0]
            elif attendance_result_txt_matchType == 3 :
                p = re.compile(r'[(](.*?)[)]', re.S)           
                result_txt=re.findall(p, result_txt)[1]
            elif attendance_result_txt_matchType == 4 :
                p = re.compile(r'[(](.*?)[)]', re.S)           
                result_txt=re.findall(p, result_txt)[2]

            logger.debug('站点【{}】签到结果:{}',site_name,result_txt)
        else:
            logger.debug('站点【{}】没有获取到签到结果',site_name)
        return result_txt

    def main(self):
        loginResult = False
        attendanceResult = False
        attendanceResultTxt = ''
        site_config = self._site_config
        siteName=site_config.get('site_name')
        try:
           loginResult = self.do_login()
           time.sleep(5)
        except Exception as err:
            logger.exception('登录站点:{} 异常!',siteName,err)
        else:
            if loginResult == True:
                try:
                    attendanceResult = self.do_attendance()
                    if attendanceResult == True:
                        try:
                           attendanceResultTxt = self.get_attendance_result_text() 
                        except Exception as err:
                            logger.exception('站点:{} 获取签到结果异常!',siteName,err)
                except Exception as err:
                    logger.exception('站点:{} 签到异常!',siteName,err)
        finally:
            siteResult = SiteResultInfo(siteName,loginResult,attendanceResult,attendanceResultTxt)
            return siteResult