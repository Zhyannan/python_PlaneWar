# pygame是第三方的游戏开发包  主要做2D游戏  pygame.org
import pygame, random, sys, time  # pygame内部实现了批量导入处理
WINDOW_W, WINDOW_H = 512, 768  #  窗口宽高  常量: 告诉使用者,该常量定义后,不要在后续程序中修改
"""公共父类 元素类
属性:
image   图片
x   坐标  
y"""
class Item:  # 元素类
    def __init__(self, img_path, x, y):
        self.image = pygame.image.load(img_path)  # 图片
        self.x = x  # 坐标
        self.y = y

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
        # 初始化pygame库，文本和音效需要做这个设置
        pygame.init()
        self.window = pygame.display.set_mode((WINDOW_W, WINDOW_H))  # 窗口
        self.map = Map()  # 创建地图对象
        self.hero_plane = HeroPlane("res/hero2.png", 300, 500)  # 创建飞机对象
        self.enemy_planes = []  # 敌机列表
        for _ in range(5):
            enemy = EnemyPlane("res/img-plane_%d.png" % random.randint(1, 7), random.randint(0, WINDOW_W-100), random.randint(-500, -70))  # 创建敌机对象
            self.enemy_planes.append(enemy)
        self.score = 0  # 记录得分

    def draw_map(self):  # 贴背景图
        if self.map.y2 < 0:
            self.window.blit(self.map.image, (self.map.x1, self.map.y1))  # 帖背景图
            self.window.blit(self.map.image2, (self.map.x2, self.map.y2))
        else:
           self.map.reset()  # 重置

    def draw_bullets(self):  # 贴子弹图
        out_window_bullets = []  # 记录所有需要删除的子弹

        for bullet in self.hero_plane.bullet_list:  # 取出每颗子弹, 贴图
            if bullet.y >= -31:  # 判断子弹是否飞出边界

                for enemy in self.enemy_planes:  # 和每架敌机检测碰撞

                    if bullet.is_hit_enemy(enemy):  # 再判断是否击中敌机
                        out_window_bullets.append(bullet)  # 发生碰撞 删除子弹
                        enemy.reset()  # 重置敌机状态
                        self.score += 10  # 累加得分
                        break  # 该子弹已经和一架飞机发生了碰撞, 所以不需要和其他敌机检测,所以直接跳出循环

                else:  # 没有和任何一架敌机碰撞
                    self.window.blit(bullet.image, (bullet.x, bullet.y))

            else:  # 飞出窗口
                out_window_bullets.append(bullet)  # 记录需要删除的子弹 不要边遍历边删除

        for out_window_bullet in out_window_bullets:
            self.hero_plane.bullet_list.remove(out_window_bullet)  # 将子弹从列表属性中移除  子弹占用的内存会自动回收

    def draw_hero(self):
        self.window.blit(self.hero_plane.image, (self.hero_plane.x, self.hero_plane.y))  # 贴飞机图

    def draw_enemy(self):
        for enemy in self.enemy_planes:
            if enemy.y >= WINDOW_H:
                enemy.reset()  # 重置敌机
            else:
                self.window.blit(enemy.image, (enemy.x, enemy.y))  # 贴敌机图

    def draw_text(self, font_size, content, x, y):  # 贴文本
        # 加载自定义字体，返回字体对象
        font = pygame.font.Font("res/SIMHEI.TTF", font_size)
        # 设置文本，返回文本对象   render(文本内容， 抗锯齿，颜色)
        text = font.render(content, 1, (255, 255, 255))
        # 在指定位置和尺寸绘制指定文字对象
        self.window.blit(text, (x, y))

    def draw(self):  # 贴图
        self.draw_map()
        self.draw_hero()
        self.draw_bullets()
        self.draw_enemy()
        self.draw_text(35, "得分:%d" % self.score, 30, 30)


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
        self.map.move()  # 地图移动

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
class HeroPlane(Item):  # 英雄飞机类
    def __init__(self, img_path, x, y):
        super().__init__(img_path, x, y)  # 调用父类方法,继承属性
        self.bullet_list = []  # 记录所有发出的子弹

    def fire(self):  # 发射子弹
        # 子弹x = 飞机x + 飞机宽度*0.5 - 子弹宽度*0.5  子弹y = 飞机y - 子弹高度
        bullet = Bullet("res/bullet_9.png", self.x + 50, self.y - 31) # 创建子弹对象
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
class Bullet(Item):  # 子弹类
    def move(self):  # 上移
        self.y -= 12

    def is_hit_enemy(self, enemy):  # 判断是否击中敌机  返回True/False
        # 子弹和敌机的矩形区域是否有交点
        bullet_rect = pygame.Rect(self.x, self.y, 20, 31)
        enemy_rect = pygame.Rect(enemy.x, enemy.y, 100, 68)
        # 两个矩形 相交返回True
        return pygame.Rect.colliderect(bullet_rect, enemy_rect)

    # def __del__(self):
        # print("子弹被删除")

"""
class 敌机类
属性
image   敌机图片
x   坐标  
y
方法
move(self):  下移
reset(self):   重置"""
class EnemyPlane(Item):  # 敌机类
    def move(self):  # 下移
        self.y += 14

    def reset(self):  # 重置
        self.__init__("res/img-plane_%d.png" % random.randint(1, 7), random.randint(0, WINDOW_W-100), random.randint(-500, -70))  # 数据重置

"""
class 地图类
属性
image   地图图片1
x1   坐标  
y1
image2   地图图片2
x2   坐标  
y2
方法
move(self):  下移"""
class Map:  # 地图类
    def __init__(self):
        self.image = pygame.image.load("res/img_bg_level_%d.jpg" % random.randint(1, 5))  # 图片1
        self.x1 = 0  # 图片1坐标
        self.y1 = 0

        self.image2 = self.image
        self.x2 = 0
        self.y2 = -WINDOW_H

    def move(self):  # 下移
        self.y1 += 5
        self.y2 += 5

    def reset(self):  # 重置
        self.x1 = 0
        self.y1 = 0
        self.x2 = 0
        self.y2 = -WINDOW_H

def main():  # 主函数  设置为程序的入口
    # 创建游戏对象
    game = Game()
    # 运行
    game.run()

if __name__ == '__main__':
    main()
