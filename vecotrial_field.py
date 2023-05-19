from manim import *
import operator as op
import itertools as it
def my_func(*my_points, **kwargs):
    radius=kwargs.get("radius",0.5)
    def func(point):
        result=np.array(ORIGIN)
        for center,strength in my_points:
            to_center=center-point
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
        "radio":0.5,
    }
    def __init__(self,color,sign=True,**kwargs):
        Dot.__init__(self,**kwargs)
        self.set(width=self.CONFIG['radio'])
        self.set_color(color)
        if sign:
            TEX="+"
        else:
            TEX="-"
        signo=Tex(TEX)
        self.add(signo)
class MyVectorField(Scene):
    CONFIG={
        'anim_kwargs':{
            'run_time':0.4,
            'rate_func':linear
        },
        'charge_kwargs':{
            'radius':0.3
        },
        'radio':0.5,
        "colors":[
            BLUE,
            RED,
            GREEN,
            YELLOW,
            PURPLE,
            ORANGE
        ]
    }
    def construct(self):
        charges=self.get_charges(12)
        self.play(Create(charges),**self.CONFIG['anim_kwargs'])
        self.wait()
    def get_charges(self,amount):
        positions = np.array([
            [
                config['frame_width']/2*np.random.uniform(-1,1),
                config['frame_height']/2*np.random.uniform(-1,1),
                0
            ]
            for _ in range(amount)
        ])
        charges = VGroup()
        colors = it.cycle(self.CONFIG['colors'])
        for position in positions:
            color = next(colors)
            valor=np.random.choice([True,False])
            if valor:
                atributte=True
            else:
                atributte=False
            charge = ChargeParticle(color,atributte,**self.CONFIG['charge_kwargs'])
            if atributte:
                charge.carga=1
            else:
                charge.carga=-1
            charge.center = position
            charge.move_to(charge.center)
            charges.velocity=rotate_vector(
                np.random.random(3)*RIGHT,
                np.random.uniform(0,2*np.pi)
            )
            charges.add(charge)
        return charges
            
                
        