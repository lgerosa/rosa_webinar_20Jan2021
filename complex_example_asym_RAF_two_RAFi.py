# exported from PySB model 'complex_example_asym_RAF_two_RAFi'

from pysb import Model, Monomer, Parameter, Expression, Compartment, Rule, Observable, Initial, MatchOnce, Annotation, MultiState, Tag, ANY, WILD

Model()

Monomer('R', ['r', 'i', 'state'], {'state': ['none', 'R1', 'R2']})
Monomer('I1', ['r'])
Monomer('I2', ['r'])

Parameter('R_0', 0.01)
Parameter('I1_0', 0.0)
Parameter('I2_0', 0.0)
Parameter('kr_1', 10.0)
Parameter('kf_1', 1.0)
Parameter('phi_1', 1.0)
Parameter('kr_2a', 0.1)
Parameter('kf_2a', 1.0)
Parameter('phi_2a', 1.0)
Parameter('kr_2b', 0.1)
Parameter('kf_2b', 1.0)
Parameter('phi_2b', 1.0)
Parameter('fa', 1.0)
Parameter('fb', 1.0)
Parameter('g1a', 1.0)
Parameter('g1b', 1.0)
Parameter('g2a', 1.0)
Parameter('g2b', 1.0)
Parameter('g3a', 1.0)
Parameter('g3b', 1.0)

Expression('Gf_1', log(kr_1/kf_1))
Expression('Ea0_1', -phi_1*log(kr_1/kf_1) - log(kf_1))
Expression('Gf_2a', log(kr_2a/kf_2a))
Expression('Ea0_2a', -phi_2a*log(kr_2a/kf_2a) - log(kf_2a))
Expression('Gf_2b', log(kr_2b/kf_2b))
Expression('Ea0_2b', -phi_2b*log(kr_2b/kf_2b) - log(kf_2b))
Expression('Gf_fa', log(fa))
Expression('Gf_fb', log(fb))
Expression('Gf_g1a', log(g1a))
Expression('Gf_g1b', log(g1b))
Expression('Gf_g2a', log(g2a))
Expression('Gf_g2b', log(g2b))
Expression('Gf_g3a', log(g3a))
Expression('Gf_g3b', log(g3b))

Rule('R1', R(r=None, state='none') + R(r=None, state='none') | R(r=1, state='R1') % R(r=1, state='R2'), phi_1, Ea0_1, energy=True)
Rule('R2a', R(i=None) + I1(r=None) | R(i=1) % I1(r=1), phi_2a, Ea0_2a, energy=True)
Rule('R2b', R(i=None) + I2(r=None) | R(i=1) % I2(r=1), phi_2b, Ea0_2b, energy=True)

Initial(R(r=None, i=None, state='none'), R_0)
Initial(I1(r=None), I1_0)
Initial(I2(r=None), I2_0)

