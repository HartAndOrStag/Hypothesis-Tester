import decimal
import math


def Phi(x: float, mu: float = 0.0, sigma: float = 1.0, k_max: int = 100, precision: int = 100):
    
    # error checking
    assert k_max > 0, "k_max must be a positive integer."
    assert sigma != 0, "sigma cannot be zero!"
    assert precision > 0, "precision must be a positive integer."
    
    # add decimal to everything to fix floating-point error
    decimal.getcontext().prec = precision

    x = decimal.Decimal(x)
    mu = decimal.Decimal(mu)
    sigma = decimal.Decimal(sigma)
    
    summation = decimal.Decimal(0)

    # Sum((-1 ^ k) / ((2 ^ k) * k! * (2k + 1))) * (((x - mu) / sigma) ^ (2k + 1))
    for k in range(k_max):
        summation += (
            # (-1) ^ k
            ((-1) ** k) * 
            # 1 / ((2 ^ k) * k! * (2k + 1))
            decimal.Decimal(1) / (
                (decimal.Decimal(2) ** k) * 
                decimal.Decimal(math.factorial(k)) * 
                decimal.Decimal(2 * k + 1) 
            ) * 
            # ((x - mu) / sigma) ^ 2k + 1
            decimal.Decimal((x - mu) / sigma) ** decimal.Decimal(2 * k + 1)
        )
        
        # multiply constant 1 / sqrt(2pi) and 
        # add 0.5 to center curve such that half is below the mean
    return decimal.Decimal(0.5) + summation / decimal.Decimal(math.sqrt(math.pi * 2))
