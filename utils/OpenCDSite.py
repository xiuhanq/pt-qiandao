from logging import debug, log
from loguru import logger
from selenium.webdriver.common.by import By
from utils.Captcha import Captcha
from utils.DefaultSite import DefaultSite
import time
class OpenCDSite(DefaultSite):
    
    def __init__(self,driver,site_config):
        DefaultSite.__init__(self,driver,site_config)

    def do_attendance_captcha(self):
        logger.debug('开始处理签到验证码')
        time.sleep(2)
        result = False    
        site_config = self._site_config
        driver = self._driver
        site_name = site_config.get('site_name')
        iframe_id=site_config.get('attendance_frame_id')
        if site_config.get('attendance_image_captcha_xpath') is not None:
            iframe = driver.find_element(By.ID,iframe_id)
            iframe_x = iframe.location['x']
            iframe_y = iframe.location['y']
            # logger.debug('iframe.x:{},iframe.y:{}',iframe_x,iframe_y)
            driver.switch_to.frame(iframe_id)
            if self.check_elementExists(site_config.get('attendance_image_captcha_xpath'))==True:
                captcha = Captcha(driver,site_config.get('image_captcha_save_path'),site_config.get('attendance_image_captcha_xpath'))
                captcha_str = captcha.image_text_iframe(iframe_x,iframe_y)
                captcha_len = len(captcha_str)
                verify_len = int(site_config.get('attendance_captcha_length'))
                logger.debug('站点:{},签到验证码:{},签到验证码长度:{},有效长度:{}',site_name, captcha_str,captcha_len,verify_len)
                if captcha_len != verify_len:
                    logger.debug('{},签到验证码[{}]有误,重新刷新页面!',site_name,captcha_str)
                    result = False  
                else:
                    captcha_input = driver.find_element(By.XPATH,site_config.get('attendance_image_captcha_input_xpath')) 
                    captcha_input.send_keys(captcha_str)
                    captcha_submit_btn = driver.find_element(By.XPATH, site_config.get('attendance_submit_btn_xpath'))
                    captcha_submit_btn.click()
                    result = True  
            else:
                result = False  
                logger.debug('没有找到签到验证码')
            driver.switch_to.default_content()
        return result
