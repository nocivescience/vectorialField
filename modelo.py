def my_func(*my_points, **kwargs):
    radius = kwargs.get("radius", 0.5)

    def func(point):
        result = np.array(ORIGIN)
        for center, strength in my_points:
            to_center = center-point
            norm = get_norm(to_center)
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
        "buff": 0.5
    }

    def __init__(self, sign=True, **kwargs):
        Dot.__init__(self, **kwargs)
        # digest_config(self,kwargs)
        self.set_width(width=self.radio)
        self.set_color(BLUE)
        if sign:
            TEX = "+"
        else:
            TEX = "-"
        signo = TexMobject(TEX)
        self.add(signo)


class MiVectorField(Scene):
    CONFIG = {
        "anim_kwargs": {
            "run_time": 0.4,
            "rate_func": linear
        },
        "charge_kwargs": {
            "radius": 0.3
        }
    }

    def construct(self):
        charges = self.get_my_charges(6)
        vector_field = self.get_force_field(charges)
        self.play(ShowCreation(vector_field), **self.anim_kwargs)
        self.play(ShowCreation(charges))

        def update_vector_field(vector_field):
            new_field = self.get_force_field(charges)
            vector_field.become(new_field)
            # vector_field.func=new_field.func

        def update_particles(particles, dt):
            func = vector_field.func
            for particle in particles:
                force = func(particle.get_center())
                particle.center += particle.velocity*dt
                for i, L in zip([0, 1], [FRAME_X_RADIUS, FRAME_Y_RADIUS]):
                    if abs(particle.center[i]) > L:
                        particle.center[i] = np.sign(particle.center[i])*L
                        particle.velocity[i] *= -1*op.mul(
                            np.sign(particle.velocity[i]), np.sign(particle.center[i]))
                particle.shift(particle.velocity*dt)
        vector_field.add_updater(update_vector_field)
        charges.add_updater(update_particles)
        self.wait(60)

    def get_my_charges(self, amount, atribute=None):
        position = np.array([
            [
                FRAME_X_RADIUS*np.random.uniform(-1, 1),
                FRAME_Y_RADIUS*np.random.uniform(-1, 1),
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
                      [p.charge for p in mis_cargas])), **self.charge_kwargs
        )
        vector_field = VectorField(func)
        return vector_field
