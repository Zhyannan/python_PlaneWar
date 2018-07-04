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
        self.hero_plane = HeroPlane() # 创建飞机对象

    def draw(self):  # 贴图
        self.window.blit(self.bg_img, (0, 0))  # 帖背景图
        self.window.blit(self.hero_plane.image, (self.hero_plane.x, self.hero_plane.y))   # 贴飞机图

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
            self.hero_plane.move_left()
        if pressed_keys[pygame.K_d] or pressed_keys[pygame.K_RIGHT]:
            self.hero_plane.move_right()
        if pressed_keys[pygame.K_w] or pressed_keys[pygame.K_UP]:
            self.hero_plane.move_up()
        if pressed_keys[pygame.K_s] or pressed_keys[pygame.K_DOWN]:
            self.hero_plane.move_down()

    def run(self):  # 运行
        while True:
            # 贴图
            self.draw()
            # 刷新
            self.update()
            # 事件检测
            self.event()


"""
class 英雄飞机类
属性
image   飞机图片
x   坐标  
y
方法
move_left(self):  左移
fire(self):  发射子弹 """
class HeroPlane:  # 英雄飞机类
    def __init__(self):
        self.image = pygame.image.load("res/hero2.png")  # 图片
        self.x = 300  # 坐标
        self.y = 500

    def move_left(self):  # 左移
        self.x -= 5  # 让飞机的x减小

    def move_right(self):  # 右移
        self.x += 5

    def move_up(self):  # 上移
        self.y -= 5

    def move_down(self):  # 下移
        self.y += 5

def main():  # 主函数  设置为程序的入口
    # 创建游戏对象
    game = Game()
    # 运行
    game.run()

if __name__ == '__main__':
    main()
