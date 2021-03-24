from  PIL import Image
from loguru import logger
from selenium.webdriver.common.by import By
from aip import AipOcr
import yaml
import os
import time
import re

logger.add('pt-qiandao.log', format='{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}',encoding='utf-8')

class Captcha:

    def __init__(self,driver,_save_path,image_captcha_xpath):
        self.driver=driver
        self._save_path=_save_path
        self.image_captcha_xpath=image_captcha_xpath

    #截图，裁剪图片并返回验证码图片名称
    # _save_path 保存路径 image_captcha_xpath 验证码元素标识
    def image_crop(self):
        try:
            _file_name = int(time.time())
            _file_name_wz = str(_file_name) + '.png'
            _file_path = self._save_path + _file_name_wz
            logger.debug('截屏保存文件:{}',_file_path)
            screenshot_result = self.driver.get_screenshot_as_file(_file_path)  # get_screenshot_as_file截屏
            logger.debug('截屏结果:{}',screenshot_result)
            captchaElem = self.driver.find_element(By.XPATH,self.image_captcha_xpath)  # # 获取指定元素（验证码）
            # 因为验证码在没有缩放，直接取验证码图片的绝对坐标;这个坐标是相对于它所属的div的，而不是整个可视区域
            # location_once_scrolled_into_view 拿到的是相对于可视区域的坐标  ;  location 拿到的是相对整个html页面的坐标
            captchaX = int(captchaElem.location['x'])
            captchaY = int(captchaElem.location['y'])
            # 获取验证码宽高
            captchaWidth = captchaElem.size['width']
            captchaHeight = captchaElem.size['height']

            captchaRight = captchaX + captchaWidth
            captchaBottom = captchaY + captchaHeight

            imgObject = Image.open(_file_path)  #获得截屏的图片
            imgCaptcha = imgObject.crop((captchaX, captchaY, captchaRight, captchaBottom))  # 裁剪
            captcha_file_name = self._save_path+str(_file_name) + '-crop.png'
            imgCaptcha.save(captcha_file_name)
            if os.path.exists(_file_path):
                os.remove(_file_path)
            return  captcha_file_name
        except Exception as e:
            logger.exception('错误!', e)


    # 获取验证码图片中信息（保存地址，要识别的图片名称）
    def image_text(self):
        # 截图当前屏幕，并裁剪出验证码保存为:_file_name副本.png，并返回名称
        captcha_file_name = self.image_crop()  ##对页面进行截图，弹出框宽高（因为是固定大小，暂时直接写死了）
        # process_file_name=self.process_image(captcha_file_name) 发现不处理图片识别率更高 ╮（╯＿╰）╭
        text = self.code_detect(captcha_file_name)
        # if os.path.exists(captcha_file_name):
        #         os.remove(captcha_file_name)
        return text


    #截图，裁剪图片并返回验证码图片名称
    # _save_path 保存路径 image_captcha_xpath 验证码元素标识
    def image_crop_iframe(self,iframe_x,iframe_y):
        try:
            _file_name = int(time.time())
            _file_name_wz = str(_file_name) + '.png'
            _file_path = self._save_path + _file_name_wz
            logger.debug('截屏保存文件:{}',_file_path)
            screenshot_result = self.driver.get_screenshot_as_file(_file_path)  # get_screenshot_as_file截屏
            logger.debug('截屏结果:{}',screenshot_result)
            captchaElem = self.driver.find_element(By.XPATH,self.image_captcha_xpath)  # # 获取指定元素（验证码）
            # 因为验证码在没有缩放，直接取验证码图片的绝对坐标;这个坐标是相对于它所属的div的，而不是整个可视区域
            # location_once_scrolled_into_view 拿到的是相对于可视区域的坐标  ;  location 拿到的是相对整个html页面的坐标
            logger.debug('iframe.x:{},iframe.y:{}',iframe_x,iframe_y)
            logger.debug('captchaElem.x:{},captchaElem.y:{}',captchaElem.location['x'],captchaElem.location['y'])
            captchaX = int(captchaElem.location['x'])+int(iframe_x)
            captchaY = int(captchaElem.location['y'])+int(iframe_y)
            # 获取验证码宽高
            captchaWidth = captchaElem.size['width']
            captchaHeight = captchaElem.size['height']

            captchaRight = captchaX + captchaWidth
            captchaBottom = captchaY + captchaHeight

            imgObject = Image.open(_file_path)  #获得截屏的图片
            imgCaptcha = imgObject.crop((captchaX, captchaY, captchaRight, captchaBottom))  # 裁剪
            captcha_file_name = self._save_path+str(_file_name) + '-crop.png'
            imgCaptcha.save(captcha_file_name)
            if os.path.exists(_file_path):
                os.remove(_file_path)
            return  captcha_file_name
        except Exception as e:
            logger.exception('错误!', e)
    # 获取验证码图片中信息（保存地址，要识别的图片名称）
    def image_text_iframe(self,iframe_x,iframe_y):
        # 截图当前屏幕，并裁剪出验证码保存为:_file_name副本.png，并返回名称
        captcha_file_name = self.image_crop_iframe(iframe_x,iframe_y)  ##对页面进行截图，弹出框宽高（因为是固定大小，暂时直接写死了）
        # process_file_name=self.process_image(captcha_file_name) 发现不处理图片识别率更高 ╮（╯＿╰）╭
        text = self.code_detect(captcha_file_name)
        # if os.path.exists(captcha_file_name):
        #         os.remove(captcha_file_name)
        return text



    def sum_9_region_new(img, x, y):
        '''确定噪点 '''
        cur_pixel = img.getpixel((x, y))  # 当前像素点的值
        width = img.width
        height = img.height
    
        if cur_pixel == 1:  # 如果当前点为白色区域,则不统计邻域值
            return 0
    
        # 因当前图片的四周都有黑点，所以周围的黑点可以去除
        if y < 3:  # 本例中，前两行的黑点都可以去除
            return 1
        elif y > height - 3:  # 最下面两行
            return 1
        else:  # y不在边界
            if x < 3:  # 前两列
                return 1
            elif x == width - 1:  # 右边非顶点
                return 1
            else:  # 具备9领域条件的
                sum = img.getpixel((x - 1, y - 1)) \
                    + img.getpixel((x - 1, y)) \
                    + img.getpixel((x - 1, y + 1)) \
                    + img.getpixel((x, y - 1)) \
                    + cur_pixel \
                    + img.getpixel((x, y + 1)) \
                    + img.getpixel((x + 1, y - 1)) \
                    + img.getpixel((x + 1, y)) \
                    + img.getpixel((x + 1, y + 1))
                return 9 - sum
    
    def collect_noise_point(self,img):
        '''收集所有的噪点'''
        noise_point_list = []
        for x in range(img.width):
            for y in range(img.height):
                res_9 = self.sum_9_region_new(img, x, y)
                if (0 < res_9 < 3) and img.getpixel((x, y)) == 0:  # 找到孤立点
                    pos = (x, y)
                    noise_point_list.append(pos)
        return noise_point_list
    
    def remove_noise_pixel(img, noise_point_list):
        '''根据噪点的位置信息，消除二值图片的黑点噪声'''
        for item in noise_point_list:
            img.putpixel((item[0], item[1]), 1)

    # 二值处理
    # 设定阈值threshold，像素值小于阈值，取值0，像素值大于阈值，取值1
    # 阈值具体多少需要多次尝试，不同阈值效果不一样
    def get_table(threshold=115):
        table = []
        for i in range(256):
            if i < threshold:
                table.append(0)
            else:
                table.append(1)
        return table

    def process_image(self,file_path):
        img = Image.open(file_path)  #获得图片
        img_L=img.convert('L')  #转化为灰度图
        # img1=img_L.convert('1') #转化为二值化图
        img1=img_L.point(self.get_table(120), '1')
        noise_point_list = self.collect_noise_point(img1)
        self.remove_noise_pixel(img1, noise_point_list)
        file_name =str(file_path).split('.png')[0]+'-1.png'
        img1.save(file_name)
        return file_name

    def get_config(self):
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
        return qiandaoCfg.get('baidu').get('APP_ID'),qiandaoCfg.get('baidu').get('API_KEY'),qiandaoCfg.get('baidu').get('SECRET_KEY')

    def code_detect(self,file_path):
        APP_ID, API_KEY, SECRET_KEY = self.get_config()
        client = AipOcr(APP_ID, API_KEY, SECRET_KEY)
        f=open(file_path,'rb')
        image =f.read()
        # #  调用通用文字识别, 图片参数为本地图片
        # result = client.general(image)
        # 定义参数变量
        # options = {
        # # 定义图像方向
        #     'detect_direction': 'true',
        #     'detect_language': 'true'
        # }
        # 调用通用文字识别接口
        result = client.basicGeneral(image)
        logger.debug(result)
        word_result = ''
        logger.debug(result['words_result_num'])
        for i in range(int(result['words_result_num'])):
            word_result = word_result + result['words_result'][(i)]['words']
        logger.debug('word_result:{}',word_result)
        return re.sub(u"([^\u0030-\u0039\u0041-\u005a\u0061-\u007a])","",word_result.replace(' ',''))
    

