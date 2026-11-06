#!/home/ttolmany/scripts/tide-alert/venv/bin/python3
"""집밥 레시피 노트(hojak-recipes) 패밀리 룩 PWA/파비콘 생성 스크립트.
디자인: 다크 네이비 배경 + 원형 림 + 요리 프라이팬(우드 핸들) + 팬 안의 생선 요리 + 모락모락 피어나는 칠리 스팀 + 허브 가니쉬.
초고해상도(1024x1024)에서 2배 슈퍼샘플링(2048x2048) 렌더링 후 리사이즈.
"""
import math
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter

SIZE = 1024
OUT_DIR = Path(__file__).resolve().parent

BG_COLOR = (18, 22, 28)        # 다크 네이비 #12161c
BG_RIM = (35, 43, 53)          # 림 테두리
PAN_BODY = (40, 50, 65)        # 주물 팬 차콜 #283241
PAN_INNER = (26, 33, 44)       # 팬 내부 딥차콜
PAN_RIM = (75, 90, 115)        # 팬 림 하이라이트
HANDLE_WOOD = (195, 135, 80)   # 우드 손잡이
HANDLE_DARK = (150, 95, 50)
GOLD = (245, 166, 35)          # 물고기 골드 #f5a623
GOLD_LIGHT = (255, 210, 90)
CHILI_STEAM = (225, 85, 65)    # 칠리 레드 스팀 #e15541
HERB_GREEN = (52, 211, 153)    # 허브 에메랄드 #34d399
WHITE = (255, 255, 255)


def draw_icon():
    scale = 2
    W = SIZE * scale
    H = SIZE * scale
    img = Image.new("RGBA", (W, H), BG_COLOR + (255,))
    draw = ImageDraw.Draw(img)

    cx, cy = W // 2, H // 2
    r_rim = int(W * 0.44)

    # 1. 은은한 배경 원형 림 (뱃지)
    draw.ellipse(
        [cx - r_rim, cy - r_rim, cx + r_rim, cy + r_rim],
        fill=(27, 33, 41, 255),
        outline=(46, 55, 66, 255),
        width=8 * scale
    )

    shadow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sdraw = ImageDraw.Draw(shadow)

    # 2. 요리 프라이팬 (Skillet / Pan)
    # 팬 원형 본체 중심: 살짝 좌하단에 배치하여 우상단으로 손잡이가 뻗어나가도록
    px = int(W * 0.45)
    py = int(H * 0.55)
    pan_r = int(W * 0.26)

    # 팬 손잡이 (우상단 40도 각도)
    h_angle = -math.radians(38)
    h_len = int(W * 0.36)
    h_w = 28 * scale

    # 손잡이 기하 좌표 (로컬 사각 -> 회전)
    def handle_pt(l, w):
        rx = px + (pan_r + l) * math.cos(h_angle) - w * math.sin(h_angle)
        ry = py + (pan_r + l) * math.sin(h_angle) + w * math.cos(h_angle)
        return (rx, ry)

    h_pts = [
        handle_pt(0, -h_w // 2),
        handle_pt(h_len, -h_w // 2 + 3 * scale),
        handle_pt(h_len + 15 * scale, 0),
        handle_pt(h_len, h_w // 2 - 3 * scale),
        handle_pt(0, h_w // 2),
    ]

    # 그림자 (팬 + 손잡이)
    sdraw.ellipse([px - pan_r + 14 * scale, py - pan_r + 20 * scale, px + pan_r + 14 * scale, py + pan_r + 20 * scale], fill=(0, 0, 0, 140))
    s_h_pts = [(p[0] + 12 * scale, p[1] + 18 * scale) for p in h_pts]
    sdraw.polygon(s_h_pts, fill=(0, 0, 0, 140))

    shadow = shadow.filter(ImageFilter.GaussianBlur(16 * scale))
    img = Image.alpha_composite(img, shadow)
    draw = ImageDraw.Draw(img)

    # 손잡이 우드 본체
    draw.polygon(h_pts, fill=HANDLE_WOOD + (255,), outline=HANDLE_DARK + (255,), width=3 * scale)
    # 손잡이 끝 걸이 구멍
    hole_pt = handle_pt(h_len - 22 * scale, 0)
    draw.ellipse([hole_pt[0] - 8 * scale, hole_pt[1] - 8 * scale, hole_pt[0] + 8 * scale, hole_pt[1] + 8 * scale], fill=BG_COLOR + (255,))

    # 팬 외부 원 (외벽)
    draw.ellipse([px - pan_r, py - pan_r, px + pan_r, py + pan_r], fill=PAN_BODY + (255,), outline=PAN_RIM + (255,), width=5 * scale)

    # 팬 내부 바닥 원
    inner_r = pan_r - 18 * scale
    draw.ellipse([px - inner_r, py - inner_r, px + inner_r, py + inner_r], fill=PAN_INNER + (255,), outline=(18, 24, 32, 255), width=3 * scale)

    # 3. 팬 안의 생선 요리 (Fish Dish)
    # 팬 중앙에 노릇하게 구워진 물고기 실루엣
    fx = px
    fy = py + 5 * scale
    # 물고기 몸통 좌표 (가로형, 머리 오른쪽)
    fish_pts = [
        (fx + 95 * scale, fy - 5 * scale),   # 입
        (fx + 65 * scale, fy - 45 * scale),  # 등 앞
        (fx + 5 * scale, fy - 55 * scale),   # 등 최고점
        (fx - 55 * scale, fy - 35 * scale),  # 등 뒤
        (fx - 95 * scale, fy - 15 * scale),  # 꼬리 목
        (fx - 135 * scale, fy - 40 * scale), # 꼬리 상단
        (fx - 120 * scale, fy),              # 꼬리 가운데 파임
        (fx - 135 * scale, fy + 40 * scale), # 꼬리 하단
        (fx - 95 * scale, fy + 15 * scale),  # 꼬리 목 아래
        (fx - 50 * scale, fy + 35 * scale),  # 배 뒤
        (fx + 10 * scale, fy + 45 * scale),  # 배 최저점
        (fx + 65 * scale, fy + 30 * scale),  # 배 앞
    ]
    # 생선 기름/그릴 자국 그림자
    f_shadow = [(p[0] + 3 * scale, p[1] + 5 * scale) for p in fish_pts]
    draw.polygon(f_shadow, fill=(15, 20, 28, 200))
    # 생선 본체 골드
    draw.polygon(fish_pts, fill=GOLD + (255,))

    # 등지느러미
    dorsal = [
        (fx - 10 * scale, fy - 55 * scale),
        (fx - 25 * scale, fy - 75 * scale),
        (fx - 50 * scale, fy - 42 * scale),
    ]
    draw.polygon(dorsal, fill=(215, 140, 20, 255))

    # 생선 눈 & 아가미
    eye_x = fx + 70 * scale
    eye_y = fy - 8 * scale
    draw.ellipse([eye_x - 6 * scale, eye_y - 6 * scale, eye_x + 6 * scale, eye_y + 6 * scale], fill=WHITE + (255,))
    draw.ellipse([eye_x - 3 * scale, eye_y - 3 * scale, eye_x + 3 * scale, eye_y + 3 * scale], fill=PAN_INNER + (255,))
    draw.arc([fx + 35 * scale, fy - 25 * scale, fx + 55 * scale, fy + 15 * scale], start=280, end=80, fill=(215, 140, 20, 255), width=3 * scale)

    # 4. 허브 가니쉬 (생선 위에 얹은 초록 허브 잎사귀 2개)
    leaf1 = [
        (fx + 5 * scale, fy - 15 * scale),
        (fx + 25 * scale, fy - 35 * scale),
        (fx + 40 * scale, fy - 25 * scale),
        (fx + 20 * scale, fy - 8 * scale),
    ]
    leaf2 = [
        (fx - 5 * scale, fy - 12 * scale),
        (fx - 15 * scale, fy - 35 * scale),
        (fx - 32 * scale, fy - 28 * scale),
        (fx - 18 * scale, fy - 5 * scale),
    ]
    draw.polygon(leaf1, fill=HERB_GREEN + (255,))
    draw.polygon(leaf2, fill=(40, 180, 130, 255))

    # 5. 모락모락 피어나는 칠리 스팀 (Aroma Steam Curves, 3줄기)
    steam_configs = [
        (px - 60 * scale, py - inner_r - 10 * scale, 0),
        (px, py - inner_r - 35 * scale, 1.2),
        (px + 60 * scale, py - inner_r - 15 * scale, 2.4),
    ]
    for sx, sy, phase in steam_configs:
        s_pts = []
        for i in range(24):
            t = i / 24.0
            cur_y = sy - t * (120 * scale)
            cur_x = sx + math.sin(t * math.pi * 2.5 + phase) * (18 * scale)
            s_pts.append((cur_x, cur_y))
        for j in range(len(s_pts) - 1):
            alpha = int(240 * (1.0 - j / len(s_pts)))
            color = CHILI_STEAM + (alpha,)
            draw.line([s_pts[j], s_pts[j + 1]], fill=color, width=5 * scale)

    # 리사이즈
    final_512 = img.resize((512, 512), Image.Resampling.LANCZOS)
    final_192 = img.resize((192, 192), Image.Resampling.LANCZOS)
    final_180 = img.resize((180, 180), Image.Resampling.LANCZOS)
    final_32 = img.resize((32, 32), Image.Resampling.LANCZOS)

    target_dirs = [OUT_DIR, Path.home() / "projects/hojak-recipes"]
    for td in target_dirs:
        td.mkdir(parents=True, exist_ok=True)
        final_512.save(td / "icon-512.png", "PNG")
        final_192.save(td / "icon-192.png", "PNG")
        final_180.save(td / "favicon-180.png", "PNG")
        final_32.save(td / "favicon-32.png", "PNG")
        print(f"[gen_icons] wrote {td}/(icon-512, icon-192, favicon-180, favicon-32).png")


if __name__ == "__main__":
    draw_icon()
