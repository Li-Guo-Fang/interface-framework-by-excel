import logging
from logging import config
from Config.ProjConfigVar import conf_path

logging.config.fileConfig(conf_path) # 加载配置文件
logger = logging.getLogger("example01") # 读取配置文件中日志的配置


"""
日志配置文件：多个logger,每个logger，指定不同的handler
handler:设定了日志输出行的格式
handler:以及设定写日志到文件（是否回滚）？还是到屏幕
handler：还定了打印日志的级别。
"""
if __name__ == '__main__':
    logger.debug("Debug message")
    logger.info("Info message")
    logger.warning("Warning message")