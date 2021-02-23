# exported from PySB model 'toy_example_RAF_RAFi'

from pysb import Model, Monomer, Parameter, Expression, Compartment, Rule, Observable, Initial, MatchOnce, EnergyPattern, Annotation, MultiState, Tag, ANY, WILD
from sympy import log

Model()

Monomer('R', ['r', 'i'])
Monomer('I', ['r'])

Parameter('R_0', 0.01)
Parameter('I_0', 0.0)
Parameter('kr_RR', 10.0)
Parameter('kf_RR', 1.0)
Parameter('phi_RR', 1.0)
Parameter('kr_RI', 0.1)
Parameter('kf_RI', 1.0)
Parameter('phi_RI', 1.0)
Parameter('f', 1.0)
Parameter('g', 1.0)

Expression('Gf_RR', log(kr_RR/kf_RR))
Expression('Ea0_RR', -phi_RR*log(kr_RR/kf_RR) - log(kf_RR))
Expression('Gf_RI', log(kr_RI/kf_RI))
Expression('Ea0_RI', -phi_RI*log(kr_RI/kf_RI) - log(kf_RI))
Expression('Gf_f', log(f))
Expression('Gf_g', log(g))
Expression('Gf_RRI', Gf_f)
Expression('Gf_IRRI', Gf_f + Gf_g)

Observable('Rtot_obs', R())
Observable('Itot_obs', I())
Observable('R_BRAFmut_active_obs', R(i=None))
Observable('R_RAFwt_active_obs', R(r=1, i=None) % R(r=1))
Observable('R_obs', R(r=None, i=None))
Observable('RR_obs', R(r=1, i=None) % R(r=1, i=None))
Observable('RRI_obs', R(r=1, i=None) % R(r=1, i=2) % I(r=2))
Observable('IRRI_obs', I(r=2) % R(r=1, i=2) % R(r=1, i=3) % I(r=3))

Rule('RR', R(r=None) + R(r=None) | R(r=1) % R(r=1), phi_RR, Ea0_RR, energy=True)
Rule('RI', R(i=None) + I(r=None) | R(i=1) % I(r=1), phi_RI, Ea0_RI, energy=True)

EnergyPattern('ep_RR', R(r=1) % R(r=1), Gf_RR)
EnergyPattern('ep_RI', R(i=1) % I(r=1), Gf_RI)
EnergyPattern('ep_RRI', R(r=1, i=None) % R(r=1, i=2) % I(r=2), Gf_RRI)
EnergyPattern('ep_IRRI', I(r=2) % R(r=1, i=2) % R(r=1, i=3) % I(r=3), Gf_IRRI)

Initial(R(r=None, i=None), R_0)
Initial(I(r=None), I_0)

