import sys
from selenium import webdriver
from loguru import logger
from apscheduler.schedulers.blocking import BlockingScheduler
from utils.DefaultSite import DefaultSite
from utils.HaidanSite import HaidanSite
from utils.OpenCDSite import OpenCDSite
from utils.Notify import Notify
import yaml
import os
import datetime

logger.add('pt-qiandao.log', format='{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}',encoding='utf-8')

def get_config():
    # 获取当前脚本所在文件夹路径
    current_path = os.path.abspath(".")
    # 获取yaml配置文件路径
    yamlPath = os.path.join(current_path, "config.yaml")
    # open方法打开直接读出来
    file = open(yamlPath, 'r', encoding='utf-8')
    # 读出来是字符串
    cfgStr = file.read() 
    # 用load方法转字典
    cfg = yaml.load(cfgStr, Loader=yaml.FullLoader)
    qiandaoCfg = cfg.get('qiandao')
    # logger.info('签到配置文件:{}',str(qiandaoCfg))
    file.close()
    return qiandaoCfg

def get_dirver(qiandaoCfg):
    command_executor_cfg = ''
    desired_capabilities_cfg={'browserName': 'chrome'}
    if qiandaoCfg is not None :
        if qiandaoCfg.get('command_executor') is not None:
            command_executor_cfg = qiandaoCfg.get('command_executor')
    logger.debug('command_executor:{}',command_executor_cfg)

    options = webdriver.ChromeOptions()
    # options.add_argument("--headless")
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-gpu')#谷歌文档提到需要加上这个属性来规避bug
    options.add_argument('--disable-infobars')#隐藏"Chrome正在受到自动软件的控制"
    options.add_argument('lang=zh_CN.UTF-8')      # 设置中文
    options.add_experimental_option("excludeSwitches", ["enable-automation"])  # 此步骤很重要，设置为开发者模式，防止被各大网站识别出来使用了Selenium
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument("--disable-blink-features=AutomationControlled")
    # 更换头部
    user_agent = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36")
    options.add_argument('user-agent=%s'%user_agent)
    
    driver = webdriver.Remote(
        command_executor=command_executor_cfg,
        desired_capabilities=desired_capabilities_cfg,
        options=options
    )
    driver.delete_all_cookies()
    driver.maximize_window()
    #等待60秒
    driver.implicitly_wait(60)
    return driver

def get_sitesConfig(qiandaoCfg):
    sitesConfig = qiandaoCfg.get('sites')
    # logger.debug('sitesConfig:{}',sitesConfig)
    return sitesConfig

def run_main():
    config = get_config()
    notify_url = config.get('qiyeweixin')
    sites = get_sitesConfig(config)
    driver=get_dirver(config)
    # driver.get('https://bot.sannysoft.com/')
    # driver.get_screenshot_as_file('/Users/qiuyangjun/Documents/imageCaptcha/result.png')
    # driver.quit()
    results = []
    for site in sites:
        site.setdefault('image_captcha_save_path',config.get('image_captcha_save_path'))
        site_name = site.get('site_name')
        if '海胆(haidan)'== site_name:
            results.append(HaidanSite(driver,site).main())
        elif '皇后(opencd)' == site_name:
            results.append(OpenCDSite(driver,site).main())
        else:
            results.append(DefaultSite(driver,site).main())
    driver.quit()
    for result in results:
        logger.debug('站点:{},登录结果:{},签到结果:{}',result.siteName,result.loginResult,result.attendanceResult)
    
    Notify().notify(notify_list=results)

def do_job():
    #创建调度器：BlockingScheduler
    scheduler = BlockingScheduler()
    #添加任务,时间间隔10分钟
    scheduler.add_job(run_main, 'interval', days=1,next_run_time=datetime.datetime.now(), id='job_pt_qiandao')
    scheduler.start()

do_job()