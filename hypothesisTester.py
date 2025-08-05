import normalCDF
import studentsTApproximateCDF
import tkinter
from tkinter import messagebox
import decimal

class HypothesisTester:
    def __init__(self, root):
        # set window title
        self.root = root
        self.root.title("Hypothesis Tester")
        
        # make several columns for more control,
        for i in range(10):  
            self.root.grid_columnconfigure(i, weight=1)
        # with right side having more weight for resizing
        for i in range(10, 20):  
            self.root.grid_columnconfigure(i, weight=2) 

        # create entries with text
        self.createEntry("μ₀/p₀:", 0)        
        self.createEntry("x̄/p̂:", 1)
        self.createEntry("σ:", 2)
        self.createEntry("s:", 3)
        self.createEntry("n:", 4)
        self.createEntry("α:", 5)
        
        # configure entry rows to be bigger than buttons
        for i in range(6):  
            self.root.grid_rowconfigure(i, minsize=40, weight=4)
        
        # create buttons for each hypothesis type
        self.button1 = tkinter.Button(root, text="μ > μ₀", command=self.TestMuGreaterThan)
        # use large number of columns to limit size of buttons while keeping them sticky to north, south, east, west
        self.button1.grid(row=6, column=11, columnspan=4, padx=5, pady=1, sticky="nsew")
        self.button2 = tkinter.Button(root, text="μ < μ₀", command=self.TestMuLessThan)
        self.button2.grid(row=7, column=11, columnspan=4, padx=5, pady=1, sticky="nsew")
        self.button3 = tkinter.Button(root, text="μ ≠ μ₀", command=self.TestMuNotEqualTo)
        self.button3.grid(row=8, column=11, columnspan=4, padx=5, pady=1, sticky="nsew")
        self.button4 = tkinter.Button(root, text="p > p₀", command=self.TestPGreaterThan)
        self.button4.grid(row=9, column=11, columnspan=4, padx=5, pady=1, sticky="nsew")
        self.button5 = tkinter.Button(root, text="p < p₀", command=self.TestPLessThan)
        self.button5.grid(row=10, column=11, columnspan=4, padx=5, pady=1, sticky="nsew")
        self.button6 = tkinter.Button(root, text="p ≠ p₀", command=self.TestPNotEqualTo)
        self.button6.grid(row=11, column=11, columnspan=4, padx=5, pady=1, sticky="nsew")
        
        # configure coloumn rows to have less weight when resizing
        for i in range(6, 12):  
            self.root.grid_rowconfigure(i, weight=1)
    
    # helper for creating entries    
    def createEntry(self, text, row):
        # text label set to span first half of columns
        tkinter.Label(self.root, text=text).grid(row=row, column=0, columnspan=10)
        
        # entry box set to span second half of columns
        entry = tkinter.Entry(self.root)
        entry.grid(row=row, column=10, columnspan=10, sticky="nsew")
        
        # set variable name based on row number
        setattr(self, f"entry{row}", entry) 

    # tests the hypothesis that true average is greater than what is stated
    # against the null hypothesis that the true average is equal to what is stated
    def TestMuGreaterThan(self):  
        
        # set to track 100 decimal places
        decimal.getcontext().prec = 100
        
        # set entry values to corresponding variable    
        entries = [self.entry0, self.entry1, self.entry2, self.entry3]
        values = []                
        
        # if no entry is given, set to NaN
        for entry in entries:
            try:
                values.append(float(entry.get()))
            except ValueError:
                values.append(decimal.Decimal('NaN'))

        # make each a decimal type
        mu_0, xBar, sigma, s = map(decimal.Decimal, values)

        # same process but for different types
        try:
            n = int(self.entry4.get())
        except ValueError:
            n = decimal.Decimal('NaN')  
        try:
            alpha = float(self.entry5.get())
        except ValueError:
            alpha = decimal.Decimal('NaN')
            
            
        # check user input for hypothesis specific requirements   
        if mu_0.is_nan():
            messagebox.showerror("Error", "Please enter value for μ₀")
            return
        elif xBar.is_nan():
            messagebox.showerror("Error", "Please enter value for x̄")
            return
        elif sigma.is_nan() and s.is_nan():
            messagebox.showerror("Error", "Please enter value for σ or s")
            return
        elif decimal.Decimal(n).is_nan():
            messagebox.showerror("Error", "Please enter value for n")
            return
        elif decimal.Decimal(alpha).is_nan():
            messagebox.showerror("Error", "Please enter value for α")
            return
        elif sigma == 0:
            messagebox.showerror("Error", "σ cannot be 0")
            return
        elif sigma.is_nan() and s == 0:
            messagebox.showerror("Error", "s cannot be 0")
            return
        elif alpha > 1 or alpha < 0:
            messagebox.showerror("Error", "α must be within range of 0 - 1")
            return
        elif n < 1:
            messagebox.showerror("Error", "n must be greater than 0")
            return

        # determine p-value by performing appropriate test based on information provided
        
        # if sigma is known, use sigma for z value and find Phi
        if not sigma.is_nan():
            # (x - mu) / sqrt(sigma / n)
            z = (xBar - mu_0) / (sigma / decimal.Decimal(n).sqrt())
            
            # ensure number stability by rejecting extreme values
            if z > 6:
               messagebox.showerror("Error", "Test statistic extreme.\n"
                                    "H₀ should be rejected at any reasonable significance level")
               return 
            if z < -6:
                messagebox.showerror("Error", "Test statistic extreme.\n"
                                    "H₀ should be maintained at any reasonable significance level")
                return
            
            # P(Z > z_0) = 1 - Phi(z)
            try:
                P = 1 - normalCDF.Phi(z)
            except Exception as exc:
                messagebox.showerror("Error", "Failed, please check for invalid entries")
                return
            
        # if sigma is not known, but sample size is large (n >= 30), use s for z value and find Phi
        elif n >= 30:
            # (x - mu) / sqrt(s / n)
            z = (xBar - mu_0) / (s / decimal.Decimal(n).sqrt())
            
            # ensure number stability by rejecting extreme values
            if z > 6:
               messagebox.showerror("Error", "Test statistic extreme.\n"
                                    "H₀ should be rejected at any reasonable significance level")
               return 
            if z < -6:
                messagebox.showerror("Error", "Test statistic extreme.\n"
                                    "H₀ should be maintained at any reasonable significance level")
                return
            
            # P(Z > z_0) = 1 - Phi(z)
            try:
                P = 1 - normalCDF.Phi(z)
            except Exception as exc:
                messagebox.showerror("Error", "Failed, please check for invalid entries")
                return
        
        # if sigma is not known, and sample size is small (n < 30), use s for t value and perform t-test
        else:
            # (x - mu) / sqrt(s / n)
            t = (xBar - mu_0) / (s / decimal.Decimal(n).sqrt())
            
            # ensure number stability by rejecting extreme values
            if t > 6:
               messagebox.showerror("Error", "Test statistic extreme.\n"
                                    "H₀ should be rejected at any reasonable significance level")
               return 
            if t < -6:
                messagebox.showerror("Error", "Test statistic extreme.\n"
                                    "H₀ should be maintained at any reasonable significance level")
                return
            
            # P(T > t_0) = 1 -  T_n-1(z)
            try:
                P = 1 - studentsTApproximateCDF.ScaledNormalApproximation(t, n - 1)
            except Exception as exc:
                messagebox.showerror("Error", "Failed, please check for invalid entries")
                return
        
        # determine if hypothesis should be rejected based on p-value and alpha
        if P <= alpha:
            messagebox.showinfo("Result", f"P-value: {round(P, 4)}\n"
                                f"There is sufficient evidence to suggest that H₀: μ = μ₀ should be rejected "
                                f"at the significance level α = {alpha} in favor of Hₐ: μ > μ₀")
        else:
            messagebox.showinfo("Result", f"P-value {round(P, 4)}\n"
                                f"There is NOT sufficient evidence to suggest that H₀: μ = μ₀ should be rejected "
                                f"at the significance level α = {alpha} in favor of Hₐ: μ > μ₀")

    # tests the hypothesis that true average is less than what is stated
    # against the null hypothesis that the true average is equal to what is stated
    def TestMuLessThan(self):  
        
        # set to track 100 decimal places
        decimal.getcontext().prec = 100
        
        # set entry values to corresponding variable     
        entries = [self.entry0, self.entry1, self.entry2, self.entry3]
        values = []                
        
        # if no entry is given, set to NaN
        for entry in entries:
            try:
                values.append(float(entry.get()))
            except ValueError:
                values.append(decimal.Decimal('NaN'))

        # make each a decimal type
        mu_0, xBar, sigma, s = map(decimal.Decimal, values)

        # same process but for different types
        try:
            n = int(self.entry4.get())
        except ValueError:
            n = decimal.Decimal('NaN')
        try:
            alpha = float(self.entry5.get())
        except ValueError:
            alpha = decimal.Decimal('NaN')
            
            
        # check user input for hypothesis specific requirements     
        if mu_0.is_nan():
            messagebox.showerror("Error", "Please enter value for μ₀")
            return
        elif xBar.is_nan():
            messagebox.showerror("Error", "Please enter value for x̄")
            return
        elif sigma.is_nan() and s.is_nan():
            messagebox.showerror("Error", "Please enter value for σ or s")
            return
        elif decimal.Decimal(n).is_nan():
            messagebox.showerror("Error", "Please enter value for n")
            return
        elif decimal.Decimal(alpha).is_nan():
            messagebox.showerror("Error", "Please enter value for α")
            return
        elif sigma == 0:
            messagebox.showerror("Error", "σ cannot be 0")
            return
        elif sigma.is_nan() and s == 0:
            messagebox.showerror("Error", "s cannot be 0")
            return
        elif alpha > 1 or alpha < 0:
            messagebox.showerror("Error", "α must be within range of 0 - 1")
            return
        elif n < 1:
            messagebox.showerror("Error", "n must be greater than 0")
            return

        # determine p-value by performing appropriate test based on information provided
        
        # if sigma is known, use sigma for z value and find Phi
        if not sigma.is_nan():
            # (x - mu) / sqrt(sigma / n)
            z = (xBar - mu_0) / (sigma / decimal.Decimal(n).sqrt())
            
            # ensure number stability by rejecting extreme values
            if z < -6:
               messagebox.showerror("Error", "Test statistic extreme.\n"
                                    "H₀ should be rejected at any reasonable significance level")
               return 
            if z > 6:
                messagebox.showerror("Error", "Test statistic extreme.\n"
                                    "H₀ should be maintained at any reasonable significance level")
                return
            
            # P(Z < z_0) = Phi(z)
            try:
                P = normalCDF.Phi(z)
            except Exception as exc:
                messagebox.showerror("Error", "Failed, please check for invalid entries")
                return
            
        # if sigma is not known, but sample size is large (n >= 30), use s for z value and find Phi
        elif n >= 30:
            # (x - mu) / sqrt(s / n)
            z = (xBar - mu_0) / (s / decimal.Decimal(n).sqrt())
            
            # ensure number stability by rejecting extreme values
            if z < -6:
               messagebox.showerror("Error", "Test statistic extreme.\n"
                                    "H₀ should be rejected at any reasonable significance level")
               return 
            if z > 6:
                messagebox.showerror("Error", "Test statistic extreme.\n"
                                    "H₀ should be maintained at any reasonable significance level")
                return
            
            # P(Z < z_0) = Phi(z)
            try:
                P = normalCDF.Phi(z)
            except Exception as exc:
                messagebox.showerror("Error", "Failed, please check for invalid entries")
                return
            
        # if sigma is not known, and sample size is small (n < 30), use s for t value and perform t-test
        else:
            # (x - mu) / sqrt(s / n)
            t = (xBar - mu_0) / (s / decimal.Decimal(n).sqrt())
            
            # ensure number stability by rejecting extreme values
            if t < -6:
               messagebox.showerror("Error", "Test statistic extreme.\n"
                                    "H₀ should be rejected at any reasonable significance level")
               return 
            if t > 6:
                messagebox.showerror("Error", "Test statistic extreme.\n"
                                    "H₀ should be maintained at any reasonable significance level")
                return
            
            # P(T < t_0) = T_n-1(z)
            try:
                P = studentsTApproximateCDF.ScaledNormalApproximation(t, n - 1)
            except Exception as exc:
                messagebox.showerror("Error", "Failed, please check for invalid entries")
                return
        
        # determine if hypothesis should be rejected based on p-value and alpha    
        if P <= alpha:
            messagebox.showinfo("Result", f"P-value: {round(P, 4)}\n"
                                f"There is sufficient evidence to suggest that H₀: μ = μ₀ should be rejected "
                                f"at the significance level α = {alpha} in favor of Hₐ: μ < μ₀")
        else:
            messagebox.showinfo("Result", f"P-value {round(P, 4)}\n"
                                f"There is NOT sufficient evidence to suggest that H₀: μ = μ₀ should be rejected "
                                f"at the significance level α = {alpha} in favor of Hₐ: μ < μ₀")

    # tests the hypothesis that true average is not equal to what is stated
    # against the null hypothesis that the true average is equal to what is stated
    def TestMuNotEqualTo(self):  
        
        # set to track 100 decimal places
        decimal.getcontext().prec = 100
        
        # set entry values to corresponding variable 
        entries = [self.entry0, self.entry1, self.entry2, self.entry3]
        values = []                
        
        # if no entry is given, set to NaN
        for entry in entries:
            try:
                values.append(float(entry.get()))
            except ValueError:
                values.append(decimal.Decimal('NaN'))

        # make each a decimal type
        mu_0, xBar, sigma, s = map(decimal.Decimal, values)

        # same process but for different types
        try:
            n = int(self.entry4.get())
        except ValueError:
            n = decimal.Decimal('NaN')      
        try:
            alpha = float(self.entry5.get())
        except ValueError:
            alpha = decimal.Decimal('NaN')
            
                
        # check user input for hypothesis specific requirements   
        if mu_0.is_nan():
            messagebox.showerror("Error", "Please enter value for μ₀")
            return
        elif xBar.is_nan():
            messagebox.showerror("Error", "Please enter value for x̄")
            return
        elif sigma.is_nan() and s.is_nan():
            messagebox.showerror("Error", "Please enter value for σ or s")
            return
        elif decimal.Decimal(n).is_nan():
            messagebox.showerror("Error", "Please enter value for n")
            return
        elif decimal.Decimal(alpha).is_nan():
            messagebox.showerror("Error", "Please enter value for α")
            return
        elif sigma == 0:
            messagebox.showerror("Error", "σ cannot be 0")
            return
        elif sigma.is_nan() and s == 0:
            messagebox.showerror("Error", "s cannot be 0")
            return
        elif alpha > 1 or alpha < 0:
            messagebox.showerror("Error", "α must be within range of 0 - 1")
            return
        elif n < 1:
            messagebox.showerror("Error", "n must be greater than 0")
            return

   
        # determine p-value by performing appropriate test based on information provided
        
        # if sigma is known, use sigma for z value and find Phi
        if not sigma.is_nan():
            # | (x - mu) / sqrt(sigma / n) |
            z = abs((xBar - mu_0) / (sigma / decimal.Decimal(n).sqrt()))
            
            # ensure number stability by rejecting extreme values
            if z > 6:
               messagebox.showerror("Error", "Test statistic extreme.\n"
                                    "H₀ should be rejected at any reasonable significance level")
               return 

            # P(Z > z_0 and Z < z_0) = 2 * (1 - Phi(| z |))
            try:
                P = 2 * (1 - normalCDF.Phi(z))
            except Exception as exc:
                messagebox.showerror("Error", "Failed, please check for invalid entries")
                return
            
        # if sigma is not known, but sample size is large (n >= 30), use s for z value and find Phi
        elif n >= 30:
            # | (x - mu) / sqrt(s / n) |
            z = abs((xBar - mu_0) / (s / decimal.Decimal(n).sqrt()))
            
            # ensure number stability by rejecting extreme values
            if z > 6:
               messagebox.showerror("Error", "Test statistic extreme.\n"
                                    "H₀ should be rejected at any reasonable significance level")
               return 
           
            # P(Z > z_0 and Z < z_0) = 2 * (1 - Phi(| z |))  
            try:
                P = 2 * (1 - normalCDF.Phi(z))
            except Exception as exc:
                messagebox.showerror("Error", "Failed, please check for invalid entries")
                return
            
        # if sigma is not known, and sample size is small (n < 30), use s for t value and perform t-test  
        else:
            # | (x - mu) / sqrt(s / n) |
            t = abs((xBar - mu_0) / (s / decimal.Decimal(n).sqrt()))
            
            # ensure number stability by rejecting extreme values
            if t > 6:
               messagebox.showerror("Error", "Test statistic extreme.\n"
                                    "H₀ should be rejected at any reasonable significance level")
               return 

            # P(T > t_0 and T < t_0) = 2 * (1 - T_n-1(| t |)) 
            try:
                P = 2 * (1 - studentsTApproximateCDF.ScaledNormalApproximation(t, n - 1))
            except Exception as exc:
                messagebox.showerror("Error", "Failed, please check for invalid entries")
                return
        
        # determine if hypothesis should be rejected based on p-value and alpha     
        if P <= alpha:
            messagebox.showinfo("Result", f"P-value: {round(P, 4)}\n"
                                f"There is sufficient evidence to suggest that H₀: μ = μ₀ should be rejected "
                                f"at the significance level α = {alpha} in favor of Hₐ: μ ≠ μ₀")
        else:
            messagebox.showinfo("Result", f"P-value {round(P, 4)}\n"
                                f"There is NOT sufficient evidence to suggest that H₀: μ = μ₀ should be rejected "
                                f"at the significance level α = {alpha} in favor of Hₐ: μ ≠ μ₀")

    # tests the hypothesis that true population proportion is greater than what is stated
    # against the null hypothesis that the true population is equal to what is stated
    def TestPGreaterThan(self):  
        
        # set to track 100 decimal places
        decimal.getcontext().prec = 100
        
        # set entry values to corresponding variable     
        entries = [self.entry0, self.entry1]
        values = []                
        
        # if no entry is given, set to NaN
        for entry in entries:
            try:
                values.append(float(entry.get()))
            except ValueError:
                values.append(decimal.Decimal('NaN'))

        # make each a decimal type
        p_0, pHat = map(decimal.Decimal, values)

        # same process but for different types
        try:
            n = int(self.entry4.get())
        except ValueError:
            n = decimal.Decimal('NaN')  
        try:
            alpha = float(self.entry5.get())
        except ValueError:
            alpha = decimal.Decimal('NaN')
         
            
        # check user input for hypothesis specific requirements           
        if p_0.is_nan():
            messagebox.showerror("Error", "Please enter value for p₀")
            return
        elif pHat.is_nan():
            messagebox.showerror("Error", "Please enter value for p̂")
            return
        elif decimal.Decimal(n).is_nan():
            messagebox.showerror("Error", "Please enter value for n")
            return
        elif decimal.Decimal(alpha).is_nan():
            messagebox.showerror("Error", "Please enter value for α")
            return
        elif p_0 > 1 or p_0 < 0:
            messagebox.showerror("Error", "p₀ must be within range of 0 - 1")
            return
        elif pHat > 1 or pHat < 0:
            messagebox.showerror("Error", "p̂ must be within range of 0 - 1")
            return
        elif alpha > 1 or alpha < 0:
            messagebox.showerror("Error", "α must be within range of 0 - 1")
            return
        elif n < 1:
            messagebox.showerror("Error", "n must be greater than 0")
            return


        # determine p-value for population proportion

        # (p - p_0) / sqrt((p_0 * (1 - p_0)) / n)
        z = (pHat - p_0) / ((p_0 * (1 - p_0)) / n).sqrt()
        
        # ensure number stability by rejecting extreme values
        if z > 6:
            messagebox.showerror("Error", "Test statistic extreme.\n"
                                "H₀ should be rejected at any reasonable significance level")
            return 
        if z < -6:
            messagebox.showerror("Error", "Test statistic extreme.\n"
                                "H₀ should be maintained at any reasonable significance level")
            return
        
        # P(Z > z_0) = 1 - Phi(z)
        try:
            P = 1 - normalCDF.Phi(z)
        except Exception as exc:
            messagebox.showerror("Error", "Failed, please check for invalid entries")
        
        # determine if hypothesis should be rejected based on p-value and alpha    
        if P <= alpha:
            messagebox.showinfo("Result", f"P-value: {round(P, 4)}\n"
                                f"There is sufficient evidence to suggest that H₀: p = p₀ should be rejected "
                                f"at the significance level α = {alpha} in favor of Hₐ: p > p₀")
        else:
            messagebox.showinfo("Result", f"P-value {round(P, 4)}\n"
                                f"There is NOT sufficient evidence to suggest that H₀: p = p₀ should be rejected "
                                f"at the significance level α = {alpha} in favor of Hₐ: p > p₀")

    # tests the hypothesis that true population proportion is less than what is stated
    # against the null hypothesis that the true population proportion is equal to what is stated
    def TestPLessThan(self):  
        
        # set to track 100 decimal places
        decimal.getcontext().prec = 100
        
        # set entry values to corresponding variable     
        entries = [self.entry0, self.entry1]
        values = []                
        
        # if no entry is given, set to NaN
        for entry in entries:
            try:
                values.append(float(entry.get()))
            except ValueError:
                values.append(decimal.Decimal('NaN'))

        # make each a decimal type
        p_0, pHat = map(decimal.Decimal, values)

        # same process but for different types
        try:
            n = int(self.entry4.get())
        except ValueError:
            n = decimal.Decimal('NaN')  
        try:
            alpha = float(self.entry5.get())
        except ValueError:
            alpha = decimal.Decimal('NaN')
         
            
        # check user input for hypothesis specific requirements           
        if p_0.is_nan():
            messagebox.showerror("Error", "Please enter value for p₀")
            return
        elif pHat.is_nan():
            messagebox.showerror("Error", "Please enter value for p̂")
            return
        elif decimal.Decimal(n).is_nan():
            messagebox.showerror("Error", "Please enter value for n")
            return
        elif decimal.Decimal(alpha).is_nan():
            messagebox.showerror("Error", "Please enter value for α")
            return
        elif p_0 > 1 or p_0 < 0:
            messagebox.showerror("Error", "p₀ must be within range of 0 - 1")
            return
        elif pHat > 1 or pHat < 0:
            messagebox.showerror("Error", "p̂ must be within range of 0 - 1")
            return
        elif alpha > 1 or alpha < 0:
            messagebox.showerror("Error", "α must be within range of 0 - 1")
            return
        elif n < 1:
            messagebox.showerror("Error", "n must be greater than 0")
            return


        # determine p-value for population proportion

        # (p - p_0) / sqrt((p_0 * (1 - p_0)) / n)
        z = (pHat - p_0) / ((p_0 * (1 - p_0)) / n).sqrt()
        
        # ensure number stability by rejecting extreme values
        if z < -6:
            messagebox.showerror("Error", "Test statistic extreme.\n"
                                "H₀ should be rejected at any reasonable significance level")
            return 
        if z > 6:
            messagebox.showerror("Error", "Test statistic extreme.\n"
                                "H₀ should be maintained at any reasonable significance level")
            return
        
        # P(Z < z_0) = Phi(z)
        try:
            P = normalCDF.Phi(z)
        except Exception as exc:
            messagebox.showerror("Error", "Failed, please check for invalid entries")
        
        # determine if hypothesis should be rejected based on p-value and alpha   
        if P <= alpha:
            messagebox.showinfo("Result", f"P-value: {round(P, 4)}\n"
                                f"There is sufficient evidence to suggest that H₀: p = p₀ should be rejected "
                                f"at the significance level α = {alpha} in favor of Hₐ: p < p₀")
        else:
            messagebox.showinfo("Result", f"P-value {round(P, 4)}\n"
                                f"There is NOT sufficient evidence to suggest that H₀: p = p₀ should be rejected "
                                f"at the significance level α = {alpha} in favor of Hₐ: p < p₀")

    # tests the hypothesis that true population proportion is not equal to what is stated
    # against the null hypothesis that the true population proportion is equal to what is stated
    def TestPNotEqualTo(self):  
        
        # set to track 100 decimal places
        decimal.getcontext().prec = 100
        
        # set entry values to corresponding variable     
        entries = [self.entry0, self.entry1]
        values = []                
        
        # if no entry is given, set to NaN
        for entry in entries:
            try:
                values.append(float(entry.get()))
            except ValueError:
                values.append(decimal.Decimal('NaN'))

        # make each a decimal type
        p_0, pHat = map(decimal.Decimal, values)

        # same process but for different types
        try:
            n = int(self.entry4.get())
        except ValueError:
            n = decimal.Decimal('NaN')  
        try:
            alpha = float(self.entry5.get())
        except ValueError:
            alpha = decimal.Decimal('NaN')
         
            
        # check user input for hypothesis specific requirements           
        if p_0.is_nan():
            messagebox.showerror("Error", "Please enter value for p₀")
            return
        elif pHat.is_nan():
            messagebox.showerror("Error", "Please enter value for p̂")
            return
        elif decimal.Decimal(n).is_nan():
            messagebox.showerror("Error", "Please enter value for n")
            return
        elif decimal.Decimal(alpha).is_nan():
            messagebox.showerror("Error", "Please enter value for α")
            return
        elif p_0 > 1 or p_0 < 0:
            messagebox.showerror("Error", "p₀ must be within range of 0 - 1")
            return
        elif pHat > 1 or pHat < 0:
            messagebox.showerror("Error", "p̂ must be within range of 0 - 1")
            return
        elif alpha > 1 or alpha < 0:
            messagebox.showerror("Error", "α must be within range of 0 - 1")
            return
        elif n < 1:
            messagebox.showerror("Error", "n must be greater than 0")
            return


        # determine p-value for population proportion

        # | (p - p_0) / sqrt((p_0 * (1 - p_0)) / n) |
        z = abs((pHat - p_0) / ((p_0 * (1 - p_0)) / n).sqrt())
        
        # ensure number stability by rejecting extreme values
        if z > 6:
            messagebox.showerror("Error", "Test statistic extreme.\n"
                                "H₀ should be rejected at any reasonable significance level")
            return 
        
        # P(Z > z_0 and Z < z_0) = 2 * (1 - Phi(| z |))  
        try:
            P = 2 * (1 - normalCDF.Phi(z))
        except Exception as exc:
            messagebox.showerror("Error", "Failed, please check for invalid entries")
        
        
        # determine if hypothesis should be rejected based on p-value and alpha    
        if P <= alpha:
            messagebox.showinfo("Result", f"P-value: {round(P, 4)}\n"
                                f"There is sufficient evidence to suggest that H₀: p = p₀ should be rejected "
                                f"at the significance level α = {alpha} in favor of Hₐ: p ≠ p₀")
        else:
            messagebox.showinfo("Result", f"P-value {round(P, 4)}\n"
                                f"There is NOT sufficient evidence to suggest that H₀: p = p₀ should be rejected "
                                f"at the significance level α = {alpha} in favor of Hₐ: p ≠ p₀")

