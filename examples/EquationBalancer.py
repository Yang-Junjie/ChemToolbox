import ChemToolbox.core.equaion_balancer as eb

equations = [
    "Ba^{2+} + SO_4^{2-} -> BaSO_4",
    "MnO_4^{-} + Fe^{2+} + H^{+} -> Mn^{2+} + Fe^{3+} + H_2O",
    "C_3H_8 + O_2 -> CO_2 + H_2O",
    "C_2H_5OH + O_2 -> CO_2 + H_2O",
    "NaOH + AlCl_3 -> NaCl + Al(OH)_3",
    "H_2+Ca(CN)_2+NaAlF_4+FeSO_4+MgSiO_3+KI+H_3PO_4+PbCrO_4+BrCl+CF_2Cl_2+SO_2->PbBr_2+CrCl_3+MgCO_3+KAl(OH)_4+Fe(SCN)_3+PI_3+Na_2SiO_3+CaF_2+H_2O",
]

balancer = eb.EquationBalancer()
for eq in equations:
    balancer.set_equation(eq)
    print("原始方程式:", eq)
    print("配平后的方程:", balancer.get_balanced_equation())
    print()
