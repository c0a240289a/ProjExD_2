import os
import random
import sys
import pygame as pg
import time

WIDTH, HEIGHT = 1100, 650
DELTA = {  # 移動量辞書
    pg.K_UP:(0,-5),
    pg.K_DOWN:(0,5),
    pg.K_LEFT:(-5,0),
    pg.K_RIGHT:(5,0),
}
os.chdir(os.path.dirname(os.path.abspath(__file__)))


def check_bound(rct: pg.Rect) -> tuple[bool,bool]:
    """
    引数：こうかとんRectまたはばくだんRect
    戻り値：タプル（横方向判定結果，縦方向判定結果）
    画面内ならTrue、画面外ならFalse
    """
    yoko,tate = True, True  # 初期値:画面の中
    if rct.left < 0 or WIDTH < rct.right:
        yoko = False
    if rct.top < 0 or HEIGHT < rct.bottom:
        tate = False
    return yoko, tate  # 横方向、縦方向の画面内判定結果を返す


def gameover(screen: pg.Surface) -> None:
    ba_img = pg.Surface((WIDTH,HEIGHT))  # 空のSurface(ブラックアウト用)
    pg.draw.rect(ba_img,(0,0,0),(0,0,WIDTH,HEIGHT)) 
    ba_img.set_alpha(100)  # 透明度(ブラックアウト)
    screen.blit(ba_img,[0,0])
    gameover_fonto = pg.font.Font(None,80)  # フォントの大きさ80
    txt = gameover_fonto.render("Gameover",True,(255,255,255))  # 「Gameover」のフォント
    txt_rct = txt.get_rect()
    txt_rct.center = WIDTH/2,HEIGHT/2  # フォントの座標
    screen.blit(txt,txt_rct)
    kkn_img = pg.transform.rotozoom(pg.image.load("fig/8.png"), 0, 0.9)
    kkn_rct = kkn_img.get_rect()
    kkn_rct2 = kkn_img.get_rect()
    kkn_rct.center = WIDTH/2+170,HEIGHT/2  # 右側こうかとんの位置を設定
    kkn_rct2.center = WIDTH/2-170,HEIGHT/2  # 左側こうかとんの位置を設定
    screen.blit(kkn_img,kkn_rct)  # 泣いてるこうかとんを表示
    screen.blit(kkn_img,kkn_rct2)  # 泣いているこうかとんを表示
    pg.display.update() 
    time.sleep(5)  # 5秒間の表示


    # def init__bb_imgs() -> tuple[list[pg.Surface], list[int]]:
    #     bb_accs = [a for a in range(1,11)]

    #     for r in range(1,11):
    #         bb_img = pg.Surface((20*r,20*r))
    #         pg.draw.circle(bb_img,(255,0,0),(10*r,10*r),10*r)

    
    # avx = vx*bb_accs[min(tmr//500,9)]
    # bb_img = bb_imgs[min(tmr//500,9)]  # 演習2途中


def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200
    # bb_imgs, bb_accs = init_bb_imgs()  # 演習2途中
    bb_img = pg.Surface((20,20))  # 空のSurfaceを作る（爆弾用）
    pg.draw.circle(bb_img,(255,0,0),(10,10),10)
    bb_img.set_colorkey((0,0,0))
    bb_rct = bb_img.get_rect()  # 爆弾Rectを取得
    bb_rct.centerx = random.randint(0,WIDTH)  # 横座標
    bb_rct.centery = random.randint(0,HEIGHT)  #縦座標
    vx,vy = +5,+5  # 爆弾の移動速度
    clock = pg.time.Clock()
    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return 
        if kk_rct.colliderect(bb_rct):  # こうかとんRectと爆弾Rectの衝突判定
            print("ゲームオーバー")
            gameover(screen)
            return    
        screen.blit(bg_img, [0, 0]) 
        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for key, mv in DELTA.items():
            if key_lst[key]:
                sum_mv[0] += mv[0]
                sum_mv[1] += mv[1]
        # if key_lst[pg.K_UP]:
        #     sum_mv[1] -= 5
        # if key_lst[pg.K_DOWN]:
        #     sum_mv[1] += 5
        # if key_lst[pg.K_LEFT]:
        #     sum_mv[0] -= 5
        # if key_lst[pg.K_RIGHT]:
        #     sum_mv[0] += 5
        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0],-sum_mv[1])  # 移動をなかったことにする
        screen.blit(kk_img, kk_rct)
        bb_rct.move_ip(vx,vy)  # 爆弾の移動
        yoko,tate = check_bound(bb_rct)
        if not yoko:  # 横方向にはみ出ていたら
            vx *= -1
        if not tate:  #縦方向にはみ出ていたら
            vy *= -1 
        screen.blit(bb_img,bb_rct)
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
