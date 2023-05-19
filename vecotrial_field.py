from manim import *
import itertools as it
def universal_func(*puntos,**kwargs):
    radius=kwargs.get("radius",0.3)
    def func(punto):
        result=np.array(ORIGIN)
        for center, strength in puntos:
            to_center=center-punto
            norm=np.linalg.norm(to_center)
            if norm==0:
                continue
            elif norm<radius:
                to_center/=radius**3
            else:
                to_center/=norm**3
            to_center*=-strength
            result+=to_center
        return result
    return func
class ChargeParticle(Dot):
    CONFIG={
        "vector_field_config":{},
        "n_particles":6,
        "anim_time":5,
        "buff":0.5,
        "radio":0.3,
        "color":[
            "#FF0000",
            "#FF7F00",
            "#FFFF00",
            "#00FF00",
            "#0000FF",
        ]
    }
    def __init__(self, sign=True, **kwargs):
        Dot.__init__(self, **kwargs)
        self.set(width=self.CONFIG["radio"])
        self.set_color(next(it.cycle(self.CONFIG["color"])))
class VectorialField(Scene):
    CONFIG={
        "anim_kwargs":{
            "run_time":0.4,
            "rate_func": linear
        },
        "charge_kwargs":{
            "radius":0.3
        },
        "n_particles":6,
    }
    def construct(self):
        cargas=self.get_my_charge(self.CONFIG["n_particles"])
        vector_field=self.get_force_field(cargas)
        self.play(Create(cargas))
        self.play(Create(vector_field),**self.CONFIG["anim_kwargs"])
        self.wait()
    def get_my_charge(self, amount, attribute=None):
        position= np.array([
            [
                config["frame_width"]/2*np.random.uniform(-1,1),
                config["frame_height"]/2*np.random.uniform(-1,1),
                0
            ]
            for _ in range(amount)
        ])
        cargas=VGroup()
        for point in position:
            valor=np.random.random()
            carga=ChargeParticle(sign=attribute)
            if valor<.5:
                attribute=False
            else:
                attribute=True
            if attribute:
                carga.charge=1
            else:
                carga.charge=-1
            carga.center=point
            carga.move_to(carga.center)
            carga.velocity=rotate_vector(
                np.random.random()*RIGHT*config["frame_width"]/2,
                np.random.random()*TAU
            )
            cargas.add(carga)
        return cargas
    def get_force_field(self, charges):
        func=universal_func(
            *list(zip(list(map(lambda x: x.get_center(), charges)),[p.charge for p in charges])),
            **self.CONFIG["charge_kwargs"]
        )
        vector_field=VectorField(func)
        return vector_field