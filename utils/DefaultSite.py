from logging import debug, log
from loguru import logger
from selenium.webdriver.common.by import By
from utils.Captcha import Captcha
from utils.SiteResultInfo import SiteResultInfo
import time


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
            time.sleep(10)
            element = driver.find_element(By.XPATH, xpath)
        except NoSuchElementException as e:
            # 发生了NoSuchElementException异常，说明页面中未找到该元素，返回False
            return False
        else:
            # 没有发生异常，表示在页面中找到了该元素，返回True
            return True

    def do_login(self): 
        site_config = self._site_config
        driver = self._driver
        site_name = site_config.get('site_name')
        logger.debug('开始登录:{} =====>>',site_name)
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
                # if self.check_elementExists(attendance_btn_xpath)==True:
                #     attendance_button = driver.find_element(By.XPATH,attendance_btn_xpath)
                #     btn_text = attendance_button.text
                #     logger.debug('签到按钮文本:{}',btn_text)
                #     if site_config.get('attendance_text')==btn_text:
                #         attendance_button.click()
                #         if self.do_attendance_captcha() == False:
                #             continue
                #         attendance_result = self.check_attendance_result()
                #     else:
                #         logger.debug('站点:{}无需签到或者已经完成签到',site_name)
                #         attendance_result = True 
                #         break
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
        # if site_config.get('attendance_image_captcha_xpath') is not None:
        #     logger.debug('开始处理签到验证码')
        #     driver.switch_to.frame(0)
        #     if self.check_elementExists(site_config.get('attendance_image_captcha_xpath'))==True:
        #         captcha = Captcha(driver,site_config.get('image_captcha_save_path'),site_config.get('login_image_captcha_xpath'))
        #         captcha_str = captcha.image_text()
        #         captcha_len = len(captcha_str)
        #         verify_len = int(site_config.get('attendance_captcha_length'))
        #         logger.debug('站点:{},签到验证码:{},签到验证码长度:{},有效长度:{}',site_name, captcha_str,captcha_len,verify_len)
        #         if captcha_len != verify_len:
        #             logger.debug('{},签到验证码[{}]有误,重新刷新页面!',site_name,captcha_str)
        #             continue
        #         captcha_input = driver.find_element(By.XPATH,site_config.get('attendance_image_captcha_input_xpath')) 
        #         captcha_input.send_keys(captcha_str)
        #         captcha_submit_btn = driver.find(By.XPATH, site_config.get('attendance_submit_btn_xpath'))
        #         captcha_submit_btn.click()
        #     else:
        #         logger.debug('没有找到签到验证码')
        return True

    def check_attendance_result(self):
        result = False    
        site_config = self._site_config
        driver = self._driver
        attendance_btn_xpath = site_config.get('attendance_btn_xpath')
        index_btn_xpath = site_config.get('index_btn_xpath')
        driver.refresh()
        index_btn = driver.find_element(By.XPATH,index_btn_xpath)
        index_btn.click()
        if self.check_elementExists(attendance_btn_xpath)==True:
            attendance_button = driver.find_element(By.XPATH,attendance_btn_xpath)
            btn_text = attendance_button.text
            logger.debug('签到按钮文本:{}',btn_text)
            if site_config.get('attendance_text') != btn_text:
                result = True
        else:
            result = True
        return result


    def main(self):
        loginResult = False
        attendanceResult = False
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
                except Exception as err:
                    logger.exception('站点:{} 签到异常!',siteName,err)
        finally:
            siteResult = SiteResultInfo(siteName,loginResult,attendanceResult)
            return siteResult