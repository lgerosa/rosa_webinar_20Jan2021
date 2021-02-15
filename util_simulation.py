#utility functions used for model simulations

import numpy as np

def equilibrate(simulator, initials=None, param_values=None):
    """Simulate a model from given initial conditions until it reaches steady state"""
    scale = 10
    t_start = 100
    tspan = np.geomspace(t_start, t_start * scale)
    while True:
        res = simulator.run(tspan=tspan, initials=initials, param_values=param_values)
        initials = res.species[-1]
        close = np.isclose(
            *res.species[[-1,-2]].view(float).reshape(2,-1),
            rtol=1e-3
        )
        if np.all(close):
            break
        tspan *= scale
    return res