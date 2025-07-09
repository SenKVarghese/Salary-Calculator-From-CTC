import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox

def calculate_salary_breakdown(ctc_annual):
    """
    Calculates the annual and monthly salary breakdown based on India's
    New Tax Regime for FY 2025-26, assuming 12 LPA exemption is effectively applied.

    Args:
        ctc_annual (float): The annual Cost to Company (CTC) in Indian Rupees.

    Returns:
        dict: A dictionary containing annual and monthly salary breakdown details.
              Returns None if input is invalid.
    """
    results = {}

    # --- Annual Calculations ---
    
    # Standard Deduction in New Tax Regime for FY 2025-26
    # This is a fixed deduction for salaried individuals and pensioners.
    standard_deduction_annual = 75000

    # PF Contribution (Employee's share: 12% of Basic + DA, capped at Rs. 15,000 basic for calculation purposes)
    # IMPORTANT SIMPLIFICATION:
    # In a real-world scenario, CTC is broken down into various components (Basic, HRA, LTA, etc.).
    # PF is typically calculated on 'Basic Salary' + 'Dearness Allowance (DA)'.
    # The statutory wage ceiling for PF contribution is ₹15,000 per month (₹1,80,000 annually) for Basic + DA.
    # For this simplified calculator, we are assuming 'Basic + DA' is 50% of the CTC.
    # This is a common, but not universal, industry practice. For exact figures,
    # you would need the precise Basic + DA component of your CTC.
    
    pf_basic_limit_annual = 15000 * 12 # Annual statutory limit for Basic + DA for PF calculation
    assumed_basic_da_annual = ctc_annual * 0.50 # Assuming 50% of CTC is Basic + DA

    if assumed_basic_da_annual > pf_basic_limit_annual:
        # If assumed Basic+DA exceeds the statutory limit, PF is calculated on the limit.
        pf_employee_annual = 0.12 * pf_basic_limit_annual
    else:
        # Otherwise, PF is calculated on the assumed Basic+DA.
        pf_employee_annual = 0.12 * assumed_basic_da_annual

    # Taxable Income Calculation (New Regime FY 2025-26)
    # Under the New Tax Regime, most traditional deductions (like 80C, 80D, HRA exemption)
    # are not allowed. Only the standard deduction (for salaried) and employer's NPS contribution
    # (if applicable, not included in this simplified model) are typically considered.
    # For simplicity, we consider CTC as the starting point and subtract PF and standard deduction.
    
    taxable_income_before_rebate = ctc_annual - pf_employee_annual - standard_deduction_annual
    
    # Ensure taxable income doesn't go below zero
    if taxable_income_before_rebate < 0:
        taxable_income_before_rebate = 0

    # Income Tax Calculation as per New Tax Regime Slabs (FY 2025-26)
    # Slabs:
    # Up to ₹4,00,000 – Nil
    # ₹4,00,001 to ₹8,00,000 – 5%
    # ₹8,00,001 to ₹12,00,000 – 10%
    # ₹12,00,001 to ₹16,00,000 – 15%
    # ₹16,00,001 to ₹20,00,000 – 20%
    # ₹20,00,001 to ₹24,00,000 – 25%
    # Above ₹24,00,000 – 30%
    
    annual_tax_before_cess = 0
    income_for_tax_calculation = taxable_income_before_rebate

    # Calculate tax slab by slab, from highest to lowest income bracket
    if income_for_tax_calculation > 2400000:
        annual_tax_before_cess += (income_for_tax_calculation - 2400000) * 0.30
        income_for_tax_calculation = 2400000 # Reduce income to the next slab's upper limit
    if income_for_tax_calculation > 2000000:
        annual_tax_before_cess += (income_for_tax_calculation - 2000000) * 0.25
        income_for_tax_calculation = 2000000
    if income_for_tax_calculation > 1600000:
        annual_tax_before_cess += (income_for_tax_calculation - 1600000) * 0.20
        income_for_tax_calculation = 1600000
    if income_for_tax_calculation > 1200000:
        annual_tax_before_cess += (income_for_tax_calculation - 1200000) * 0.15
        income_for_tax_calculation = 1200000
    if income_for_tax_calculation > 800000:
        annual_tax_before_cess += (income_for_tax_calculation - 800000) * 0.10
        income_for_tax_calculation = 800000
    if income_for_tax_calculation > 400000:
        annual_tax_before_cess += (income_for_tax_calculation - 400000) * 0.05
    # Income up to 4,00,000 is Nil, so no calculation needed for that slab after this point.

    # Section 87A Rebate for FY 2025-26
    # This rebate ensures that individuals with net taxable income up to ₹12,00,000
    # pay zero income tax. The maximum rebate is ₹60,000.
    if taxable_income_before_rebate <= 1200000:
        annual_tax_before_cess = max(0, annual_tax_before_cess - 60000) # Apply rebate, ensure tax doesn't go negative

    # Surcharge Calculation (Simplified)
    # Surcharge applies to very high incomes. For this calculator's scope,
    # we are assuming no surcharge. For incomes > ₹50 Lakhs, surcharge rates apply:
    # >₹50L to ₹1Cr: 10%
    # >₹1Cr to ₹2Cr: 15%
    # >₹2Cr to ₹5Cr: 25%
    # >₹5Cr: 25% (under new regime, reduced from 37% in old regime)
    surcharge = 0 

    # Health and Education Cess
    # A mandatory 4% cess is levied on the income tax (including surcharge, if any).
    health_cess = annual_tax_before_cess * 0.04
    
    total_annual_tax = annual_tax_before_cess + surcharge + health_cess

    # Final In-Hand Salary Calculation (Annual)
    # This is a simplified "in-hand" calculation.
    # Actual in-hand salary would also account for other deductions like:
    # Professional Tax (state-specific), company-specific deductions (e.g., loan repayments,
    # voluntary deductions, other allowances, etc.).
    annual_in_hand_salary = ctc_annual - total_annual_tax - pf_employee_annual

    # --- Monthly Calculations ---
    # Divide annual figures by 12 to get monthly equivalents.
    monthly_ctc = ctc_annual / 12
    monthly_pf_deduction = pf_employee_annual / 12
    monthly_tax = total_annual_tax / 12
    monthly_in_hand = annual_in_hand_salary / 12

    # Store results in a dictionary
    results['annual'] = {
        'Annual CTC': ctc_annual,
        'Annual Standard Deduction': standard_deduction_annual,
        'Annual Employee PF Deduction': pf_employee_annual,
        'Annual Taxable Income (before rebate)': taxable_income_before_rebate,
        'Total Annual Income Tax': total_annual_tax,
        'Annual In-Hand Salary': annual_in_hand_salary
    }

    results['monthly'] = {
        'Monthly CTC': monthly_ctc,
        'Monthly Employee PF Deduction': monthly_pf_deduction,
        'Monthly Income Tax': monthly_tax,
        'Monthly In-Hand Salary': monthly_in_hand
    }

    return results

def calculate_and_display():
    """
    Handles the UI interaction: gets CTC input, performs calculations,
    and displays the results in the text area.
    Includes error handling for invalid input.
    """
    try:
        ctc_str = ctc_entry.get()
        if not ctc_str:
            messagebox.showwarning("Input Error", "Please enter your Annual CTC.")
            return

        ctc_annual = float(ctc_str)
        if ctc_annual <= 0:
            messagebox.showwarning("Input Error", "Annual CTC must be a positive number.")
            return

        calculations = calculate_salary_breakdown(ctc_annual)

        # Clear previous results in the output text widget
        output_text.config(state=tk.NORMAL) # Enable editing to clear content
        output_text.delete(1.0, tk.END)

        # Display Annual Breakdown
        output_text.insert(tk.END, "--- Annual Breakdown (FY 2025-26, New Regime) ---\n")
        for key, value in calculations['annual'].items():
            output_text.insert(tk.END, f"{key}: ₹{value:,.2f}\n") # Format to 2 decimal places with commas

        # Display Monthly Breakdown
        output_text.insert(tk.END, "\n--- Monthly Breakdown ---\n")
        for key, value in calculations['monthly'].items():
            output_text.insert(tk.END, f"{key}: ₹{value:,.2f}\n") # Format to 2 decimal places with commas

        output_text.config(state=tk.DISABLED) # Disable editing after displaying results

    except ValueError:
        messagebox.showerror("Input Error", "Please enter a valid numerical value for CTC.")
    except Exception as e:
        # Catch any other unexpected errors
        messagebox.showerror("An Unexpected Error Occurred", str(e))

def set_ctc_value(lacs_per_annum):
    """Sets the CTC entry to a predefined LPA value."""
    ctc_entry.delete(0, tk.END)
    ctc_entry.insert(0, str(lacs_per_annum * 100000))
    calculate_and_display() # Automatically calculate after setting

def adjust_ctc_value(lacs_to_add):
    """Adjusts the current CTC value by a given LPA amount."""
    try:
        current_ctc_str = ctc_entry.get()
        if not current_ctc_str:
            current_ctc = 0.0
        else:
            current_ctc = float(current_ctc_str)
        
        new_ctc = current_ctc + (lacs_to_add * 100000)
        if new_ctc < 0: # Ensure CTC doesn't go negative
            new_ctc = 0
        
        ctc_entry.delete(0, tk.END)
        ctc_entry.insert(0, str(new_ctc))
        calculate_and_display() # Automatically calculate after adjusting
    except ValueError:
        messagebox.showerror("Input Error", "Current CTC is not a valid number. Please enter a number before adjusting.")
    except Exception as e:
        messagebox.showerror("An Error Occurred", str(e))


# --- Tkinter UI Setup ---

# Create the main window
root = tk.Tk()
root.title("India Salary & Tax Calculator (FY 2025-26 New Regime)")
root.geometry("650x650") # Increased height to accommodate new buttons
root.resizable(False, False) # Prevent resizing for a fixed layout

# Configure styles for a modern look
style = ttk.Style()
style.theme_use('clam') # 'clam' or 'alt' often look better than default 'tk'
style.configure('TLabel', font=('Arial', 10))
style.configure('TButton', font=('Arial', 10, 'bold'), padding=8)
style.configure('TEntry', font=('Arial', 10), padding=5)
style.configure('TLabelFrame.Label', font=('Arial', 11, 'bold'))

# Input Frame: Contains CTC entry and Calculate button
input_frame = ttk.LabelFrame(root, text="Enter Annual CTC")
input_frame.pack(padx=20, pady=15, fill="x") # Pad X and Y, fill horizontally

ctc_label = ttk.Label(input_frame, text="Annual CTC (in ₹):")
ctc_label.pack(side=tk.LEFT, padx=10, pady=10)

ctc_entry = ttk.Entry(input_frame, width=30)
ctc_entry.pack(side=tk.LEFT, padx=10, pady=10, expand=True, fill='x') # Allow entry to expand

calculate_button = ttk.Button(input_frame, text="Calculate Tax", command=calculate_and_display)
calculate_button.pack(side=tk.LEFT, padx=10, pady=10)

# Quick Set CTC Buttons Frame
quick_set_frame = ttk.LabelFrame(root, text="Quick Set CTC")
quick_set_frame.pack(padx=20, pady=10, fill="x")

btn_10lpa = ttk.Button(quick_set_frame, text="10 LPA", command=lambda: set_ctc_value(10))
btn_10lpa.pack(side=tk.LEFT, padx=5, pady=5, expand=True, fill='x')

btn_20lpa = ttk.Button(quick_set_frame, text="20 LPA", command=lambda: set_ctc_value(20))
btn_20lpa.pack(side=tk.LEFT, padx=5, pady=5, expand=True, fill='x')

btn_50lpa = ttk.Button(quick_set_frame, text="50 LPA", command=lambda: set_ctc_value(50))
btn_50lpa.pack(side=tk.LEFT, padx=5, pady=5, expand=True, fill='x')

# Adjust CTC Buttons Frame
adjust_ctc_frame = ttk.LabelFrame(root, text="Adjust Current CTC")
adjust_ctc_frame.pack(padx=20, pady=10, fill="x")

btn_add_5lpa = ttk.Button(adjust_ctc_frame, text="+5 LPA", command=lambda: adjust_ctc_value(5))
btn_add_5lpa.pack(side=tk.LEFT, padx=5, pady=5, expand=True, fill='x')

btn_add_2lpa = ttk.Button(adjust_ctc_frame, text="+2 LPA", command=lambda: adjust_ctc_value(2))
btn_add_2lpa.pack(side=tk.LEFT, padx=5, pady=5, expand=True, fill='x')

btn_sub_2lpa = ttk.Button(adjust_ctc_frame, text="-2 LPA", command=lambda: adjust_ctc_value(-2))
btn_sub_2lpa.pack(side=tk.LEFT, padx=5, pady=5, expand=True, fill='x')

btn_sub_5lpa = ttk.Button(adjust_ctc_frame, text="-5 LPA", command=lambda: adjust_ctc_value(-5))
btn_sub_5lpa.pack(side=tk.LEFT, padx=5, pady=5, expand=True, fill='x')

# Output Frame: Displays the calculation results
output_frame = ttk.LabelFrame(root, text="Calculation Results")
output_frame.pack(padx=20, pady=10, fill="both", expand=True) # Fill both and expand

# ScrolledText widget for displaying results, allowing scrolling if content is long
output_text = scrolledtext.ScrolledText(output_frame, wrap=tk.WORD, state=tk.DISABLED, 
                                        width=70, height=15, font=('Consolas', 10),
                                        background='#f0f0f0', foreground='#333333')
output_text.pack(padx=10, pady=10, fill="both", expand=True)

# Run the Tkinter event loop
root.mainloop()
