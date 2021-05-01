from logging import debug, log
from loguru import logger
from selenium.webdriver.common.by import By
from utils.DefaultSite import DefaultSite

class HduSite(DefaultSite):
    
    def __init__(self,driver,site_config):
        DefaultSite.__init__(self,driver,site_config)

    def check_attendance_result(self):
        result = False    
        site_config = self._site_config
        driver = self._driver
        driver.refresh()
        index_btn_xpath = site_config.get('index_btn_xpath')
        index_btn = driver.find_element(By.XPATH,index_btn_xpath)
        index_btn.click()
        attendance_btn_xpath_result = site_config.get('attendance_result_xpath')
        if self.check_elementExists(attendance_btn_xpath_result)==True:
            attendance_result = driver.find_element(By.XPATH,attendance_btn_xpath_result)
            if attendance_result.is_displayed() == True :
                logger.debug('签到按钮文本:{}',attendance_result.text)
                result = True
        else:
            result = True
        return result
