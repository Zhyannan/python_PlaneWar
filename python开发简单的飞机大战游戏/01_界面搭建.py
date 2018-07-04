# pygame是第三方的游戏开发包  主要做2D游戏  pygame.org
import pygame, random  # pygame内部实现了批量导入处理
"""
class 游戏类
属性
window   窗口
bg_img   背景图
方法
draw(self):  贴图
update(self):  刷新
run(self):  运行"""
class Game:  # 游戏类
    def __init__(self):
        self.window = pygame.display.set_mode((512, 768))  # 窗口
        self.bg_img = pygame.image.load("res/img_bg_level_%d.jpg" % random.randint(1, 5))  # 背景图

    def draw(self):  # 贴图
        self.window.blit(self.bg_img, (0, 0))  # 帖背景图

    def update(self):  # 刷新
        pygame.display.update()

    def run(self):  # 运行
        while True:
            # 贴图
            self.draw()
            # 刷新
            self.update()

def main():  # 主函数  设置为程序的入口
    # 创建游戏对象
    game = Game()
    # 运行
    game.run()

if __name__ == '__main__':
    main()
