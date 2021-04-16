from logging import debug, log
from loguru import logger
from selenium.webdriver.common.by import By
from utils.DefaultSite import DefaultSite

class HaidanSite(DefaultSite):
    
    def __init__(self,driver,site_config):
        DefaultSite.__init__(self,driver,site_config)

    def check_attendance_result(self):
        result = False    
        site_config = self._site_config
        driver = self._driver
        attendance_btn_xpath = site_config.get('attendance_btn_xpath')
        index_btn_xpath = site_config.get('index_btn_xpath')
        index_btn = driver.find_element(By.XPATH,index_btn_xpath)
        index_btn.click()

        if self.check_elementExists(attendance_btn_xpath)==True:
            attendance_button = driver.find_element(By.XPATH,attendance_btn_xpath)
            btn_text = attendance_button.get_attribute('value')
            logger.debug("attendance_button_text:{}",btn_text)
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
        # logger.debug('站点【{}】attendance_result_xpath:{}',site_name,attendance_result_xpath)
        result_txt = ''
        if self.check_elementExists(attendance_result_xpath)==True:
            attendance_result_txt = driver.find_element(By.XPATH,attendance_result_xpath)
            result_txt = attendance_result_txt.get_attribute('value')
            logger.debug('站点【{}】签到结果:{}',site_name,result_txt)
        else:
            logger.debug('站点【{}】没有获取到签到结果',site_name)
        return result_txt
