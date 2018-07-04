# pygame是第三方的游戏开发包  主要做2D游戏  pygame.org
import pygame, random, sys  # pygame内部实现了批量导入处理
"""
class 游戏类
属性
window   窗口
bg_img   背景图
方法
draw(self):  贴图
update(self):  刷新
event(self):   事件检测
run(self):  运行  """
class Game:  # 游戏类
    def __init__(self):
        self.window = pygame.display.set_mode((512, 768))  # 窗口
        self.bg_img = pygame.image.load("res/img_bg_level_%d.jpg" % random.randint(1, 5))  # 背景图

    def draw(self):  # 贴图
        self.window.blit(self.bg_img, (0, 0))  # 帖背景图

    def update(self):  # 刷新
        pygame.display.update()

    def event(self):  # 事件检测
        # 按下事件   控制发射子弹
        for event in pygame.event.get():  # iter会自动生成for遍历的代码块
            if event.type == pygame.QUIT:  # python中字母都是大写的变量 称为常量(告诉使用者一旦定义, 不要修改)
                print("点击了关闭按钮")
                sys.exit()  # 退出程序
            elif event.type == pygame.KEYDOWN:  # 键盘按下事件
                if event.key == pygame.K_SPACE:
                    print("按下了空格")

        # 长按事件    控制飞机移动  返回一个元组 每个元素对应一个键位(值只有两个  1 正在按  0 没有按)
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[pygame.K_a] or pressed_keys[pygame.K_LEFT]:
            print("左")
        if pressed_keys[pygame.K_d] or pressed_keys[pygame.K_RIGHT]:
            print("右")
        if pressed_keys[pygame.K_w] or pressed_keys[pygame.K_UP]:
            print("上")
        if pressed_keys[pygame.K_s] or pressed_keys[pygame.K_DOWN]:
            print("下")

    def run(self):  # 运行
        while True:
            # 贴图
            self.draw()
            # 刷新
            self.update()
            # 事件检测
            self.event()

def main():  # 主函数  设置为程序的入口
    # 创建游戏对象
    game = Game()
    # 运行
    game.run()

if __name__ == '__main__':
    main()
