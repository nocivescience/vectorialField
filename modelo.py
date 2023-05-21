from manim import *
import operator as op
def my_func(*my_points, **kwargs):
    radius = kwargs.get("radius", 0.5)

    def func(point):
        result = np.array(ORIGIN)
        for center, strength in my_points:
            to_center = center-point
            norm = np.linalg.norm(to_center)
            if norm == 0:
                continue
            elif norm < radius:
                to_center /= radius**3
            else:
                to_center /= norm**3
            to_center *= -strength
            result += to_center
        return result
    return func
class ChargeParticle(Dot):
    CONFIG = {
        "vector_field_config": {},
        "n_particles": 6,
        "anim_time": 5,
        "buff": 0.5,
        "radio": 0.5
    }
    def __init__(self, sign=True, **kwargs):
        Dot.__init__(self, **kwargs)
        # digest_config(self,kwargs)
        self.set(width=self.CONFIG['radio'])
        self.set_color(BLUE)
        if sign:
            TEX = "+"
        else:
            TEX = "-"
        signo = Tex(TEX)
        self.add(signo)


class MiVectorField(Scene):
    CONFIG = {
        "anim_kwargs": {
            "run_time": 0.4,
            "rate_func": linear
        },
        "charge_kwargs": {
            "radius": 0.3
        },
        "radio": 0.5
    }

    def construct(self):
        charges = self.get_my_charges(6)
        vector_field = self.get_force_field(charges)
        self.play(Create(vector_field), **self.CONFIG['anim_kwargs'])
        self.play(Create(charges))

        def update_vector_field(vector_field):
            new_field = self.get_force_field(charges)
            vector_field.become(new_field)
            # vector_field.func=new_field.func

        def update_particles(particles, dt):
            func = vector_field.func
            for particle in particles:
                force = func(particle.get_center())
                particle.center += particle.velocity*dt
                for i, L in zip([0, 1], [config['frame_width']/2, config['frame_height']/2]):
                    if abs(particle.center[i]) > L:
                        particle.center[i] = np.sign(particle.center[i])*L
                        particle.velocity[i] *= -1*op.mul(
                            np.sign(particle.velocity[i]), np.sign(particle.center[i]))
                particle.shift(particle.velocity*dt)
        vector_field.add_updater(update_vector_field)
        charges.add_updater(update_particles)
        self.wait(4)

    def get_my_charges(self, amount, atribute=None):
        position = np.array([
            [
                config['frame_width']/2*np.random.uniform(-1, 1),
                config['frame_height']/2*np.random.uniform(-1, 1),
                0
            ]
            for n in range(amount)
        ])
        cargas = VGroup()
        for point in position:
            valor = np.random.random()
            if valor < .5:
                atribute = False
            else:
                atribute = True
            carga = ChargeParticle(sign=atribute)
            if atribute:
                carga.charge = 1
            else:
                carga.charge = -1
            carga.center = point
            carga.move_to(carga.center)
            carga.velocity = rotate_vector(
                np.random.random()*RIGHT, np.random.uniform(0, TAU))
            cargas.add(carga)
        return cargas

    def get_force_field(self, mis_cargas):
        func = my_func(
            *list(zip(list(map(lambda x: x.get_center(), mis_cargas)),
                      [p.charge for p in mis_cargas])), **self.CONFIG['charge_kwargs']
        )
        vector_field = ArrowVectorField(func)
        # vector_field = ArrowVectorField(
        #     func, x_range=[-7, 7, 1], y_range=[-4, 4, 1], length_func=lambda x: x / 2
        # )
        return vector_field

