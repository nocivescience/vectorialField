from manim import *
import operator as op
import itertools as it
def funcion(*puntos,**kwargs):
    radius=kwargs.get("radius",0.5)
    def func(point):
        result=np.array(ORIGIN)
        for center,strength in puntos:
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
    configure={
        "vector_field_config":{},
        "n_particles":6,
        "anim_time":5,
        "buff":0.5,
        "radio":0.5,
    }
    def __init__(self, color,sign=True, **kwargs):
        Dot.__init__(self, **kwargs)
        self.set(width=self.configure['radio'])
        if sign:
            TEX="+"
        else:
            TEX="-"
        signo=Tex(TEX)
        signo.set_color(color)
        self.add(signo)
class UpdateSinScene(Scene):
    configure={
        'amp': 1,
        't_offset': 0,
        'rate': TAU/4,
        'sin_graph_config': {
            'x_range': [-TAU, TAU, TAU/4],
            'color': RED,    
        },
        'run_time': 5,
        'colors': [
            BLUE,
            RED,
            GREEN,
            PURPLE,
            ORANGE,    
        ],
        'n_particles': 6,
        'charge_config': {
            'radius': 0.3,
        },
    }
    def construct(self):
        c=self.get_sin_graph(self.configure['t_offset'])
        cargas=self.get_charges(self.configure['n_particles'],c)
        vector_field=self.get_force_field(cargas)
        def update_cos(c,dt):
            rate=self.configure['rate']*dt
            c.become(self.get_sin_graph(self.configure['t_offset']+rate))
            self.configure['t_offset']+=rate
        def update_particles(cargas):
            for charge,i in zip(cargas, it.count()):
                charge.center=c.point_from_proportion((i+1)/self.configure['n_particles'])
                charge.move_to(charge.center)
        def update_vector_field(vector_field):
            new_field=self.get_force_field(cargas)
            vector_field.become(new_field)
        cargas.add_updater(update_particles)
        c.add_updater(update_cos)
        vector_field.add_updater(update_vector_field)
        self.play(Create(c))
        self.play(Create(cargas))
        self.play(Create(vector_field))
        self.add(c,cargas, vector_field)
        self.wait(self.configure['run_time'])
    def get_sin_graph(self, dx):
        c=FunctionGraph(
            lambda x: self.configure['amp']*np.sin(x+dx)+self.configure['amp']*np.sin(2*x+dx),
            **self.configure['sin_graph_config']
        )
        return c
    def get_charges(self,amount,curve):
        positions=[curve.point_from_proportion(t/config['frame_width']) for t in np.linspace(0,config['frame_width'],amount)]
        charges=VGroup()
        colors=it.cycle(self.configure['colors'])
        for position, i in zip(positions, it.count()):
            color=next(colors)
            if i%2==0:
                attribute=True
            else:
                attribute=False
            charge=ChargeParticle(color,attribute)
            if attribute:
                charge.carga=1
            else:
                charge.carga=-1
            charge.center=position
            charge.move_to(charge.center)
            charges.add(charge)
        return charges
    def get_force_field(self, charges):
        func=funcion(*list(zip(list(map(
            lambda x: x.center, charges
        )),
            [charge.carga for charge in charges]
                               )),
            **self.configure['charge_config'])
        vector_field=ArrowVectorField(func)
        return vector_field