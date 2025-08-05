# Hypothesis-Tester
GUI for testing a null hypothesis against an alternative hypothesis. 

Enter in all available data and GUI will decide the best method of calculation. GUI will output a P-value and write an interpretation based on the given alpha.  
Supports tests for mean greater, less than, or equal to; and population proportion greater than less than or equal to.
<br>
<br>

Calculation is based on the following algorithm, 
1. If normal population with known sigma use $z_0 = \frac{\bar{x} - \mu_0}{\frac{\sigma}{\sqrt{n}}} \sim N(0,1)$
2. If sigma is not known (i.e not normal population) and sample is large (n >= 30) use $z_0 = \frac{\bar{x} - \mu_0}{\frac{s}{\sqrt{n}}} \sim N(0,1)$
3. If sigma is not known and sample is small (n < 30) then run t-test with Student's t CDF $t_0 = \frac{\bar{x} - \mu_0}{\frac{s}{\sqrt{n}}} \sim t_{n-1}$
4. Population proportion is always calculated using $z_0 = \frac{\hat{p} - p_0}{\sqrt{\frac{p_0(1-p_0)}{n}}} \sim N(0,1)$
<br>

Normal CDF is calculated using a power series.  
Student's t is approxamated using the simple Student's t approximation $F(t;n)\approx\Phi\left(t \sqrt{\frac{n}{n+2}}\right)$ where phi is also calculated using the same normal CDF as before.
