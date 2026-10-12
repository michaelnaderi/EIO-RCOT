using JuMP
using HiGHS  

M = [
  0.65  -0.15  -0.23  -0.26  -0.28  -0.24
 -0.25   0.78   0.84  -0.22  -0.21  -0.25
 -0.20  -0.26  -0.30   0.69   0.67   0.70
 -2.10  -3.20  -1.90  -1.20  -0.80  -1.40
 -1.20  -2.20  -1.30  -1.30  -1.10  -1.10
]
C = [20, 25, 22, -540, -342]
Pi = [0, 0, 0, 1, 0.9]
F = [
  0.0  0.0  0.0  0.0  0.0  0.0
  0.0  0.0  0.0  0.0  0.0  0.0
  0.0  0.0  0.0  0.0  0.0  0.0
  2.1  3.2  1.9  1.2  0.8  1.4
  1.2  2.2  1.3  1.3  1.1  1.1
]
############################################################################################
# M = [I* - A*; -F*] = hetero-functional incidence matrix (5×6)
# M matches the output of MLPPos_MLPNeg_reader.py: M = MLPPos - MLPNeg
# U = X = Capabilities (firing vector / technology-output vector)
# C = [Y; -f] = right-hand side (final demand stacked with negated factor availability)

model = Model(HiGHS.Optimizer)
@variable(model, U[1:6] >= 0)
@constraint(model, M * U .>= C)
q = Pi' * F   
@objective(model, Min, sum(q[i] * U[i] for i in 1:6))
optimize!(model)



############################################################################################
println(" Z = ", objective_value(model))
println(" U = ", value.(U))
