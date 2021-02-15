#utility functions used to display model properties

from pysb import Expression
from sympy import Symbol, latex, simplify
from IPython.core.display import display
import pandas as pd

def display_model_info(model):
    # print model infomration
    print ('Model information')
    print ('Species:',len(model.species))
    print ('Parameters:',len(model.parameters)+len(model.initial_conditions))
    print ('Expressions:',len(model.expressions))
    print ('Observables:', len(model.observables))
    ntotr=len(model.rules);
    nenergy=len([r for r in model.rules if r.energy]);
    print ('Total Rules:', ntotr)
    print ('Energy Rules:', nenergy)
    print('Non-energy Rules:', ntotr-nenergy)
    print('Energy Patterns:', len(model.energypatterns))
    print('Reactions:',len(model.reactions))

def transform_rate(r):
    # Expand PySB Expressions into their full contents.
    r = r.replace(
        lambda a: isinstance(a, Expression),
        lambda e: e.expand_expr()
    )
    # Eliminate Species symbols by replacing them with 1.
    r = r.replace(
        lambda a: isinstance(a, Symbol) and a.name.startswith('__s'),
        lambda s: 1
    ) 
    r = r.simplify()
    return r

def format_sp(species):
    # Return LaTeX-formated sum of species variables for given species numbers.
    # Turns a list like [1,3] into "$s_1$ + $s_3$".
    return " + ".join(f"$s_{{{i}}}$" for i in species)

def to_latex(e):
    return latex(e, mul_symbol="dot")

def format_species_reactions(model):
    #display the species in the model 
    speciesdisp = pd.DataFrame(
        data=[[f"\[s_{{{idx}}}\]", str(species)] for idx, species in enumerate(model.species)],
        columns=['ID', 'Pattern']
    )
    #display the reactions and reaction rules in the model
    reactions_unidirectional = pd.DataFrame(model.reactions)
    for c in "rule", "reverse":
        if (reactions_unidirectional[c].map(len) > 1).any():
            raise Exception("Cannot handle models that produce the same reaction from different rules")
        reactions_unidirectional[c] = reactions_unidirectional[c].map(lambda x: x[0])
    reactions_unidirectional["K"] = reactions_unidirectional["rate"].map(transform_rate)
    group_direction = reactions_unidirectional.groupby("reverse")
    forward = group_direction.get_group(False)[["reactants", "products", "rule", "K"]]
    reverse = group_direction.get_group(True)[["reactants", "products", "K"]]
    reverse[["reactants", "products"]] = reverse[["products", "reactants"]]
    reactions = pd.merge(forward, reverse, on=["reactants", "products"], suffixes=["f", "r"])
    reactions["Kd"] = (reactions["Kr"] / reactions["Kf"]).apply(simplify)
    reactionsdisp = pd.DataFrame({
        "ID": [f"\[R_{{{i}}}\]" for i in range(len(reactions))],
        "Base rule": reactions["rule"],
        "Reaction": [f"{format_sp(r.reactants)} \u21c4 {format_sp(r.products)}" for r in reactions.itertuples()],
        "Forward rate ($k$ )": "\[" + reactions["Kf"].map(to_latex)
                                        .str.replace('kf_', 'k_', regex=False)
                                        .str.replace('kr_', 'kr_', regex=False)
                                        + "\]",
        "Backward rate ($kr$ )": "\[" + reactions["Kr"].map(to_latex)
                                        .str.replace('kf_', 'k_', regex=False)
                                        .str.replace('kr_', 'kr_', regex=False)
                                        + "\]",
        "Dissociation constant ($K_d$ )": "\[" + reactions["Kd"].map(to_latex)
                                        .str.replace('kf_', 'k_', regex=False)
                                        .str.replace('kr_', 'kr_', regex=False)
                                        + "\]",
    })
    return ( speciesdisp, reactionsdisp)

def display_table(df, caption=None):
    display(
        df.style
        .set_properties(**{"text-align": "center"})
        .set_table_styles([
            dict(selector="th", props=[("text-align", "center")]),
            dict(selector=".MathJax_Display", props=[("text-align", "center !important")]),
        ])
        .hide_index()
        .set_caption(caption)
    )