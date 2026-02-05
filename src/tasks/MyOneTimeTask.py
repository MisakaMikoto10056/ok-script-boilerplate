import re

from qfluentwidgets import FluentIcon

from src.tasks.MyBaseTask import MyBaseTask
#src.tasks.
import json

from pathlib import Path


from ok import Box


class MyOneTimeTask(MyBaseTask):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = "点击触发运行任务"
        self.description = "用户点击时调用run方法"
        # self.icon = FluentIcon.SYNC
        # self.default_config.update({
        #     '下拉菜单选项': "第一",
        #     '是否选项默认支持': False,
        #     'int选项': 1,
        #     '文字框选项': "默认文字",
        #     '长文字框选项': "默认文字默认文字默认文字默认文字默认文字默认文字默认文字默认文字默认文字默认文字默认文字默认文字默认文字默认文字默认文字默认文字默认文字默认文字默认文字",
        #     'list选项': ['第一', '第二', '第3'],
        # })
        # self.config_type["下拉菜单选项"] = {'type': "drop_down",
        #                               'options': ['第一', '第二', '第3']}

    def run(self):
        self.log_info('检索任务开始运行!')
        try:
            jizhi_dianji_box_list = self.jizhi_box_list()
            self.jiazhi_Search(jizhi_dianji_box_list)
        except Exception as e:
            self.log_error(f"出现错误{e}")
        self.log_info('检索任务运行完成!')

    #用于识别基质词条位置，并输出向上移动副本
    def jizhi_box_list(self):
        jizhi_list_ben = self.ocr(match=["无瑕基质"])
        if jizhi_list_ben:
            jizhi_dianji_box = [box.copy(y_offset=-(box.height+20), name="jizhi_dianji_box") for box in jizhi_list_ben]
            ##测试基质点击
            # self.draw_boxes("jizhi_dianji_box", jizhi_dianji_box, color="green")
            # self.sleep(0.5)
            # self.screenshot(name="jizhi_dianji.png", show_box=True)
            self.notification("准备完成")
            return jizhi_dianji_box
    #导入识别参数组，调用触发方法
    def jiazhi_Search(self,box_list:list) ->None:
        json_path = Path(__file__).parent.parent.parent / "." / "assets"/ "jizhi_biaoshi.json"
        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                guanjianci_list = json.load(f)
            self.log_info(f"成功加载匹配列表，共 {len(guanjianci_list)} 组关键词")
        except FileNotFoundError:
            self.log_error(f"找不到文件: {json_path}")
            return
        except json.JSONDecodeError:
            self.log_error("JSON 格式错误")
            return
        #做获取次数判断，无发图像识别，用副本框点击
        if len(box_list) <= 5:
            # 右上角锁定点
            suoding_shang = {'x_offset': 482,'y_offset':-363,'name':"suoding_shang"}
            self.chufa_suoding(box_list,guanjianci_list,suoding_shang)
        else:
            #右下角锁定点
            suoding_shang = {'x_offset': 482, 'y_offset': 79, 'name': "suoding_shang"}
            self.chufa_suoding(box_list, guanjianci_list, suoding_shang)

    #判断条件组，用副本框进行锁定
    def chufa_suoding(self,box_list_chu,guanjianci_list_chu,suoding):
        for jizhi_dianji_box in box_list_chu:
            self.sleep(0.25)
            self.click(jizhi_dianji_box)
            suoding_shang = jizhi_dianji_box.copy(**suoding)
            # #测试锁定副本框用
            # self.draw_boxes("suoding_shang", suoding_shang, color="green")
            # self.sleep(0.5)
            # self.screenshot(name="suoding_shang.png", show_box=True)
            self.sleep(0.5)
            for guanjianci in guanjianci_list_chu:
                # print(f"测试数组{guanjianci}")
                jizhi_list_ben = self.ocr(y=0.3, match=guanjianci)
                # print(f"测试{jizhi_list_ben}")
                if len(jizhi_list_ben) == 3:
                    self.log_info('检索到关键字组')
                    self.click(suoding_shang)
                    # 图像识别
                    # suoding = self.find_one("ceshi_icon", threshold=0.9)
                    # self.draw_boxes("jizhi_dianji_box", suoding, color="green")
                    # if suoding:
                    #     self.log_info(f"找到 {len(suoding)} 个图标")
                    #     # 点击第一个找到的
                    #     self.click(suoding)
                    # else:
                    #     self.log_warn("未找到图标")
                else:
                    self.log_info('没有关键字')
            self.click(jizhi_dianji_box)

    def find_some_text_on_bottom_right(self):
        return self.ocr(box="bottom_right",match="商城", log=True) #指定box以提高ocr速度

    def find_some_text_with_relative_box(self):
        return self.ocr(0.5, 0.5, 1, 1, match=re.compile("招"), log=True) #指定box以提高ocr速度

    def test_find_one_feature(self):
        return self.find_one('box_battle_1')

    def test_find_feature_list(self):
        return self.find_feature('box_battle_1')

    def run_for_5(self):
        self.operate(lambda: self.do_run_for_5())

    def do_run_for_5(self):
        self.do_send_key_down('w')
        self.sleep(0.1)
        self.do_mouse_down(key='right')
        self.sleep(0.1)
        self.do_mouse_up(key='right')
        self.sleep(5)
        self.do_send_key_up('w')

    def ceshi(self):
        full_box = Box(0, 0, 1, 1)  # 相对坐标 0-1 表示整幅画面
        suoding = self.find_feature("ceshi_icon", threshold=0.9)
        self.draw_boxes("ceshi_icon", full_box, color="green")
        self.screenshot(name="jizhi_dianji.png", show_box=True)
        if suoding:
            self.log_info(f"找到 {len(suoding)} 个图标")
            # 点击第一个找到的
            self.click(suoding)
        else:
            self.log_info("未找到图标")

def ceshi():
    json_path = Path(__file__).parent.parent.parent / "." / "assets"/ "xiuzheng.json"
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            guanjianci_list = json.load(f)
    except FileNotFoundError:
        print(f"❌ 文件不存在: {json_path}")
        return
    except json.JSONDecodeError as e:
        print(f"❌ JSON 格式错误: {e}")
        return
    print("wenjian%s"%guanjianci_list)

if __name__ == "__main__":
    ceshi()


