import configparser
import requests

air_conf = configparser.ConfigParser()
air_conf.read('air.ini', 'utf8')


# 第二步：添加section、options的值
# air_conf.add_section("path")
# air_conf.set("path","back_dir","/Users/abc/PycharmProjects/Pythoncoding/projects/") # option
# air_conf.set("path","target_dir","/Users/abc/PycharmProjects/Pythoncoding/")    # option
# air_conf.add_section("file")
# air_conf.set("file","back_file","apitest")

# 第三步：写入文件
def saveConfig(filename, config):
    with open(filename, 'w')as conffile:
        config.write(conffile)


def getValues(type):
    temps = air_conf.items(section=type)
    return temps



def setValues(infotype, location, value):
    air_conf.set(infotype, location, value)
    saveConfig('air.ini', air_conf)
    return 'success'

# setValues('temperature','bedroom1','30')
# getValues('temperature')
