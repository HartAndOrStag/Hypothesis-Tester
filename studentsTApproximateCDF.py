import normalCDF
import decimal


def ScaledNormalApproximation(t: float, n: float):
    
    t = decimal.Decimal(t)
    n = decimal.Decimal(n)

    # Phi(t * sqrt(n / (n + 2)))
    return normalCDF.Phi(t * (n / (n + 2)).sqrt())
