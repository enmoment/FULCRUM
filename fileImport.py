from models import db, Resources
import os, hashlib, shutil
from psycopg2 import DataError
from flask import current_app

class FileImporter():
    filePath = ''
    resclass = ''
    ressubclass = ''

    def __init__(self, filePath='', resClass='', resSubClass=''):
        self.filePath = os.path.join(os.path.abspath('.'), 'upload', filePath)
        self.resclass = resClass
        self.ressubclass = resSubClass
        print(self.filePath)
        self.importFile(self.filePath)

    # 递归导入文件
    def importFile(self, root_path):
        dir_or_files = os.listdir(root_path)
        # 获取文件夹名当作title
        title = root_path
        for dir_file in dir_or_files:
            # 获取目录或者文件的路径
            dir_file_path = os.path.join(root_path, dir_file)
            # 判断该路径为文件还是路径
            if os.path.isdir(dir_file_path):
                # 递归获取所有文件和目录的路径
                self.importFile(dir_file_path)
            else:
                res_title = title.split('/')[-1]
                # 检查文件是否需要被清理并获得文件类型
                resPath = self.clean(dir_file_path)
                # 如果没有被清理则导入数据库
                if resPath != None:
                    res = Resources(res_type=resPath[2], res_class=self.resclass, res_subclass=self.ressubclass,
                                    res_title=res_title, res_origin='PC', res_path=resPath[0], file_name=resPath[1])
                    try:
                        db.session.add(res)
                        db.session.commit()
                        print('导入文件成功:', resPath[0])
                    except DataError as e:
                        print('导入%s失败' % (resPath[0]))
                        print(e)

    # 清理文件并拷贝到资源目录下
    def clean(self, filepath):
        clearner = ['.chm', 'Sky.jpg', '.gif', '.mht', '.url', '.torrent']
        fileName = filepath.split('/')[-1]
        fileext = '.' + fileName.split('.')[-1]
        if fileName in clearner or fileext in clearner:
            os.remove(filepath)
            print('Delete file :', fileName)
            return None
        else:
            # 将文件移动到资源文件夹，并使用md5加密文件名
            type = self.getResType(fileext)

            Dir = os.path.join(current_app.config.get('RES_FOLDER'), self.resclass, self.ressubclass, filepath.split('/')[-2])
            # sysDir = os.path.join(os.path.abspath('.'), Dir)
            newName = hashlib.md5(('66' + filepath).encode(encoding='utf-8')).hexdigest() + fileext
            savePath = os.path.join(Dir, newName)
            if not os.path.exists(Dir):
                os.makedirs(Dir)
                print("目录创建成功！:", Dir)
            shutil.move(filepath, savePath)
            return Dir, newName, type

    # 根据扩展名获取资源类型
    def getResType(self, type):
        pic = ['.jpg', '.png', '.bmp', '.jpeg','.JPG','.PNG','.BMP','JPEG']
        video = ['.mp4',  '.MP4','.avi', '.AVI', '.rmvb', '.mov' '.MOV']
        if type in pic:
            return 'pic'
        elif type in video:
            return 'video'
        else:
            return 'other'
