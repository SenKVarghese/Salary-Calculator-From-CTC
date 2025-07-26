from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton, MDIconButton
from kivymd.uix.label import MDLabel
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.card import MDCard
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivy.metrics import dp

class SalaryCalculatorApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.dialog = None

    def build(self):
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Blue"
        
        screen = MDScreen()
        main_layout = MDBoxLayout(
            orientation="vertical",
            padding=dp(20),
            spacing=dp(15)
        )

        # Title
        title = MDLabel(
            text="India Salary Calculator\n(FY 2025-26 New Regime)",
            theme_text_color="Primary",
            size_hint_y=None,
            height=dp(80),
            halign="center"
        )

        # CTC Input
        self.ctc_input = MDTextField(
            hint_text="Enter Annual CTC (₹)",
            input_filter="float",
            size_hint_y=None,
            height=dp(56)
        )

        # Quick set buttons
        quick_buttons_layout = MDBoxLayout(
            orientation="horizontal",
            spacing=dp(10),
            size_hint_y=None,
            height=dp(40)
        )
        
        for lpa in [10, 20, 50]:
            btn = MDRaisedButton(
                text=f"{lpa} LPA",
                size_hint_x=1,
                on_release=lambda x, lpa=lpa: self.set_ctc_value(lpa)
            )
            quick_buttons_layout.add_widget(btn)

        # Calculate button
        calculate_btn = MDRaisedButton(
            text="Calculate Tax",
            size_hint_y=None,
            height=dp(48),
            on_release=self.calculate_salary
        )

        # Results scroll view
        self.results_scroll = MDScrollView()
        self.results_layout = MDBoxLayout(
            orientation="vertical",
            spacing=dp(10),
            adaptive_height=True
        )
        self.results_scroll.add_widget(self.results_layout)

        # Add all widgets
        main_layout.add_widget(title)
        main_layout.add_widget(self.ctc_input)
        main_layout.add_widget(quick_buttons_layout)
        main_layout.add_widget(calculate_btn)
        main_layout.add_widget(self.results_scroll)

        screen.add_widget(main_layout)
        return screen

    def set_ctc_value(self, lpa):
        self.ctc_input.text = str(lpa * 100000)
        self.calculate_salary()

    def calculate_salary(self, *args):
        try:
            if not self.ctc_input.text:
                self.show_error("Please enter your Annual CTC")
                return

            ctc_annual = float(self.ctc_input.text)
            if ctc_annual <= 0:
                self.show_error("Annual CTC must be positive")
                return

            results = self.calculate_salary_breakdown(ctc_annual)
            self.display_results(results)

        except ValueError:
            self.show_error("Please enter a valid number")

    def calculate_salary_breakdown(self, ctc_annual):
        results = {}
        
        standard_deduction_annual = 75000
        pf_basic_limit_annual = 15000 * 12
        assumed_basic_da_annual = ctc_annual * 0.50

        if assumed_basic_da_annual > pf_basic_limit_annual:
            pf_employee_annual = 0.12 * pf_basic_limit_annual
        else:
            pf_employee_annual = 0.12 * assumed_basic_da_annual

        taxable_income_before_rebate = max(0, ctc_annual - pf_employee_annual - standard_deduction_annual)

        annual_tax_before_cess = 0
        income_for_tax_calculation = taxable_income_before_rebate

        if income_for_tax_calculation > 2400000:
            annual_tax_before_cess += (income_for_tax_calculation - 2400000) * 0.30
            income_for_tax_calculation = 2400000
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

        if taxable_income_before_rebate <= 1200000:
            annual_tax_before_cess = max(0, annual_tax_before_cess - 60000)

        health_cess = annual_tax_before_cess * 0.04
        total_annual_tax = annual_tax_before_cess + health_cess
        annual_in_hand_salary = ctc_annual - total_annual_tax - pf_employee_annual

        results['annual'] = {
            'Annual CTC': ctc_annual,
            'Annual Standard Deduction': standard_deduction_annual,
            'Annual Employee PF Deduction': pf_employee_annual,
            'Annual Taxable Income (before rebate)': taxable_income_before_rebate,
            'Total Annual Income Tax': total_annual_tax,
            'Annual In-Hand Salary': annual_in_hand_salary
        }

        results['monthly'] = {
            'Monthly CTC': ctc_annual / 12,
            'Monthly Employee PF Deduction': pf_employee_annual / 12,
            'Monthly Income Tax': total_annual_tax / 12,
            'Monthly In-Hand Salary': annual_in_hand_salary / 12
        }

        return results

    def display_results(self, results):
        self.results_layout.clear_widgets()

        annual_card = self.create_results_card("Annual Breakdown", results['annual'])
        self.results_layout.add_widget(annual_card)

        monthly_card = self.create_results_card("Monthly Breakdown", results['monthly'])
        self.results_layout.add_widget(monthly_card)

    def create_results_card(self, title, data):
        card = MDCard(
            size_hint_y=None,
            height=dp(200),
            padding=dp(15),
            elevation=2
        )
        
        layout = MDBoxLayout(orientation="vertical", spacing=dp(5))
        
        title_label = MDLabel(
            text=title,
            theme_text_color="Primary",
            size_hint_y=None,
            height=dp(30),
            bold=True
        )
        layout.add_widget(title_label)

        for key, value in data.items():
            result_label = MDLabel(
                text=f"{key}: ₹{value:,.2f}",
                size_hint_y=None,
                height=dp(25)
            )
            layout.add_widget(result_label)

        card.add_widget(layout)
        return card

    def show_error(self, message):
        if not self.dialog:
            self.dialog = MDDialog(
                title="Error",
                text=message,
                buttons=[
                    MDFlatButton(
                        text="OK",
                        on_release=self.close_dialog
                    )
                ]
            )
        else:
            self.dialog.text = message
        self.dialog.open()

    def close_dialog(self, *args):
        if self.dialog:
            self.dialog.dismiss()

if __name__ == "__main__":
    SalaryCalculatorApp().run()