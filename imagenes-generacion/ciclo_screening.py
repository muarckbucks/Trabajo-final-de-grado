from manim import *
import math


class Intercambiador(VGroup):
    def __init__(self, width=2, height=3, n_zig_zag=8, margen=0.3, **kwargs):
        super().__init__(**kwargs)
        self.hx_width  = width
        self.hx_height = height
        stroke_width = 3

        # Cuerpo
        rectangulo = RoundedRectangle(
            width=width, height=height,
            corner_radius=0.2,
            color=BLACK, fill_color=WHITE, fill_opacity=1,
            
        )
        self.add(rectangulo)



        # Zigzag discreto: segmento inicial + zigzag + segmento final
        for x_center in [-width * 0.25, width * 0.25]:
            y_top    =  height / 2
            y_bot    = -height / 2
            y_start  =  y_top  - margen   # fin del segmento inicial
            y_end    =  y_bot  + margen   # inicio del segmento final
            zag_h    = y_start - y_end    # altura disponible para el zigzag

            # Segmento recto superior
            self.add(Line(
                [x_center, y_top,   0],
                [x_center, y_start, 0],
                color=BLACK, stroke_width=stroke_width
            ))

            # Zigzag discreto: lista de coords, unidas con Lines
            n = n_zig_zag * 4 + 1
            coords = []
            for i in range(n):
                dx = width / 8 * math.sin(2 * math.pi * i / (n - 1) * n_zig_zag)
                dy = y_start - zag_h * i / (n - 1)
                coords.append((x_center + dx, dy, 0))

            for (ax, ay, az), (bx, by, bz) in zip(coords[:-1], coords[1:]):
                self.add(Line(
                    [ax, ay, az], [bx, by, bz],
                    color=BLACK, stroke_width=stroke_width
                ))

            # Segmento recto inferior
            self.add(Line(
                [x_center, y_end, 0],
                [x_center, y_bot, 0],
                color=BLACK, stroke_width=stroke_width
            ))

    @property
    def pt_lu(self): return self.get_top()    + LEFT  * self.hx_width * 0.25
    @property
    def pt_ru(self): return self.get_top()    + RIGHT * self.hx_width * 0.25
    @property
    def pt_ld(self): return self.get_bottom() + LEFT  * self.hx_width * 0.25
    @property
    def pt_rd(self): return self.get_bottom() + RIGHT * self.hx_width * 0.25


class Compresor(VGroup):
    """
    Trapecio asimétrico horizontal.
    Lado izquierdo alto (baja presión), lado derecho bajo (alta presión).
    Conexiones en el punto medio de cada lado vertical, tocando el cuerpo.
    """
    def __init__(self, width=1.5, height_left=2.0, height_right=1.0, **kwargs):
        super().__init__(**kwargs)
        self.cp_width        = width
        self.cp_height_left  = height_left
        self.cp_height_right = height_right

        hl, hr = height_left / 2, height_right / 2

        trapecio = Polygon(
            [-width/2, -hl, 0],
            [-width/2,  hl, 0],
            [ width/2,  hr, 0],
            [ width/2, -hr, 0],
            color=BLACK, fill_color=WHITE, fill_opacity=1,
        )
        self.add(trapecio)



    @property
    def pt_l(self): return self.get_left()
    @property
    def pt_r(self): return self.get_right()


class Valvula(VGroup):
    """
    Válvula de expansión: dos triángulos enfrentados por el vértice (mariposa).
    Conexiones en el extremo exterior de cada triángulo, tocando el cuerpo.
    """
    def __init__(self, size=1.0, **kwargs):
        super().__init__(**kwargs)
        self.v_size = size
        s = size / 2

        tri_l = Polygon(
            [-s,  s, 0],
            [-s, -s, 0],
            [ 0,  0, 0],
            color=BLACK, fill_color=WHITE, fill_opacity=1,
        )
        tri_r = Polygon(
            [ s,  s, 0],
            [ s, -s, 0],
            [ 0,  0, 0],
            color=BLACK, fill_color=WHITE, fill_opacity=1,
        )
        self.add(tri_l, tri_r)



    @property
    def pt_l(self): return self.get_left()
    @property
    def pt_r(self): return self.get_right()


# ── Escena de prueba ──────────────────────────────────────────────────────
class Diagrama(Scene):
    def construct(self):
        self.camera.background_color = WHITE

        evap = Intercambiador().move_to([-4, 0, 0])
        cond = Intercambiador().move_to([4, 0, 0])
        comp = Compresor().move_to([0, -2, 0])
        valv = Valvula().move_to([0, 2, 0])

        self.add(evap, cond, comp, valv)

        l_evap_comp_1 = Line(evap.pt_rd, [evap.pt_rd[0], comp.pt_l[1], 0], color = BLACK)
        l_evap_comp_2 = Line([evap.pt_rd[0], comp.pt_l[1], 0], comp.pt_l, 0, color = BLACK)

        l_comp_cond_1 = Line(comp.pt_r, [cond.pt_ld[0], comp.pt_r[1], 0], color = BLACK)
        l_comp_cond_2 = Line([cond.pt_ld[0], comp.pt_r[1], 0], cond.pt_ld, 0, color = BLACK)

        l_cond_v_1 = Line(cond.pt_lu, [cond.pt_lu[0], valv.pt_r[1], 0], color = BLACK)
        l_cond_v_2 = Line([cond.pt_lu[0], valv.pt_r[1], 0], valv.pt_r, color = BLACK)

        l_v_evap_1 = Line(valv.pt_l, [evap.pt_ru[0], valv.pt_l[1], 0], color = BLACK)
        l_v_evap_2 = Line([evap.pt_ru[0], valv.pt_l[1], 0], evap.pt_ru, color = BLACK)

        self.add(l_evap_comp_1, l_evap_comp_2, l_comp_cond_1, l_comp_cond_2, l_cond_v_1,
                 l_cond_v_2, l_v_evap_1, l_v_evap_2)


        dist_water = 1.2

        l_hw = Arrow(cond.pt_rd, cond.pt_rd - UP * dist_water, color = BLACK,stroke_width=3.5, buff=0)
        l_cw = Line(cond.pt_ru, cond.pt_ru + UP * dist_water, color = BLACK)
        l_cg = Arrow(evap.pt_lu, evap.pt_lu + UP * dist_water, color = BLACK,stroke_width=3.5, buff=0)
        l_hg = Line(evap.pt_ld, evap.pt_ld - UP * dist_water, color = BLACK)

        self.add(l_hw, l_cw, l_cg, l_hg)

        dist_text = 1.5

        temp_hw = MathTex(r"\text{T}_\text{hw}", color = BLACK).move_to(cond.pt_rd - UP * dist_text)
        temp_cw = MathTex(r"\text{T}_\text{cw}", color = BLACK).move_to(cond.pt_ru + UP * dist_text)
        temp_0 = MathTex(r"0\,^{\circ}C", color = BLACK).move_to(evap.pt_ld - UP * dist_text)
        temp_m3 = MathTex(r"-3\,^{\circ}C", color = BLACK).move_to(evap.pt_lu + UP * dist_text)

        self.add(temp_hw, temp_cw, temp_0, temp_m3)

        rend_comp = MathTex(r"\eta_\text{comp} = 0.6", color = BLACK).move_to(comp.get_center() - UP * 1.5)

        self.add(rend_comp)

        text_cond = Text(r"Condensador", color = BLACK, font_size = 30).move_to(cond.get_right() + RIGHT * 0.5).rotate(PI/2)
        text_evap = Text(r"Evaporador", color = BLACK, font_size = 30).move_to(evap.get_left() - RIGHT * 0.5).rotate(PI/2)

        self.add(text_cond, text_evap)








