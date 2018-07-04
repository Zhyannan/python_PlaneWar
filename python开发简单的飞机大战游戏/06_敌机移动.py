# pygame是第三方的游戏开发包  主要做2D游戏  pygame.org
import pygame, random, sys, time  # pygame内部实现了批量导入处理
WINDOW_W, WINDOW_H = 512, 768  #  窗口宽高  常量: 告诉使用者,该常量定义后,不要在后续程序中修改
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
        self.window = pygame.display.set_mode((WINDOW_W, WINDOW_H))  # 窗口
        self.bg_img = pygame.image.load("res/img_bg_level_%d.jpg" % random.randint(1, 5))  # 背景图
        self.hero_plane = HeroPlane()  # 创建飞机对象
        self.enemy_planes = []  # 敌机列表
        for _ in range(5):
            enemy = EnemyPlane()  # 创建敌机对象
            self.enemy_planes.append(enemy)

    def draw(self):  # 贴图
        self.window.blit(self.bg_img, (0, 0))  # 帖背景图
        self.window.blit(self.hero_plane.image, (self.hero_plane.x, self.hero_plane.y))   # 贴飞机图

        out_window_bullets = []  # 记录所有需要删除的子弹
        for bullet in self.hero_plane.bullet_list:  # 取出每颗子弹, 贴图
            if bullet.y >= -31:  # 判断子弹是否飞出边界
                self.window.blit(bullet.image, (bullet.x,  bullet.y))
            else:  # 飞出窗口
                out_window_bullets.append(bullet)  # 记录需要删除的子弹 不要边遍历边删除

        for out_window_bullet in out_window_bullets:
            self.hero_plane.bullet_list.remove(out_window_bullet)  # 将子弹从列表属性中移除  子弹占用的内存会自动回收

        for enemy in self.enemy_planes:
            if enemy.y <= WINDOW_H:
                self.window.blit(enemy.image, (enemy.x, enemy.y))  # 贴敌机图
            else:
                enemy.reset()  # 重置敌机

    def update(self):  # 刷新
        pygame.display.update()

    def event(self):  # 事件检测
        # 按下事件   控制发射子弹
        for event in pygame.event.get():  # iter会自动生成for遍历的代码块
            if event.type == pygame.QUIT:  # python中字母都是大写的变量 称为常量(告诉使用者一旦定义, 不要修改)
                sys.exit()  # 退出程序
            elif event.type == pygame.KEYDOWN:  # 键盘按下事件
                if event.key == pygame.K_SPACE:
                    self.hero_plane.fire()  # 发射子弹

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

    def action(self):   # 主动处理 比如 子弹移动,敌机移动
        for bullet in self.hero_plane.bullet_list: # 取出每颗子弹, 子弹移动
            if bullet.y >= -31:  # 在边界内
                bullet.move()

        for enemy in self.enemy_planes:
            enemy.move()  # 敌机移动

    def run(self):  # 运行
        while True:
            # 贴图
            self.draw()
            # 刷新
            self.update()
            # 事件检测
            self.event()
            # 主动处理
            self.action()
            # 让程序每个循环休息一会  降低CPU的使用率
            time.sleep(0.02)

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
        self.bullet_list = []  # 记录所有发出的子弹

    def fire(self):  # 发射子弹
        # 子弹x = 飞机x + 飞机宽度*0.5 - 子弹宽度*0.5  子弹y = 飞机y - 子弹高度
        bullet = Bullet(self.x + 50, self.y - 31) # 创建子弹对象
        self.bullet_list.append(bullet)  # 记录发出的子弹

    def move_left(self):  # 左移
        self.x -= 8  # 让飞机的x减小

    def move_right(self):  # 右移
        self.x += 8

    def move_up(self):  # 上移
        self.y -= 8

    def move_down(self):  # 下移
        self.y += 8

"""
class 子弹类
属性
image   子弹图片
x   坐标  
y
方法
move(self):  上移"""
class Bullet:  # 子弹类
    def __init__(self, x, y):
        self.image = pygame.image.load("res/bullet_9.png")  # 图片
        self.x = x  # 坐标
        self.y = y

    def move(self):  # 上移
        self.y -= 12

    def __del__(self):
        print("子弹被删除")

"""
class 敌机类
属性
image   敌机图片
x   坐标  
y
方法
move(self):  下移
reset(self):   重置"""
class EnemyPlane:  # 敌机类
    def __init__(self):
        self.image = pygame.image.load("res/img-plane_%d.png" % random.randint(1, 7))  # 图片
        self.x = random.randint(0, WINDOW_W-100)  # 坐标
        self.y = random.randint(-500, -70)

    def move(self):  # 下移
        self.y += 14

    def reset(self):  # 重置
        self.__init__()  # 数据重置


def main():  # 主函数  设置为程序的入口
    # 创建游戏对象
    game = Game()
    # 运行
    game.run()

if __name__ == '__main__':
    main()
