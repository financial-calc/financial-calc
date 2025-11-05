'''
Financial math operations
Author: Vitor Beltrao Abdo - vitorbeltrao300@gmail.com
'''

import math
import numpy_financial as npf


class capitalization_regime:
    '''
    Provides methods for calculating present value, future value, and effective rates
    under various capitalization regimes (linear/simple, exponential/compound, and continuous).

    Parameters
    ----------
    term : int or float
        The period, denominated strictly in days, over which the capitalization or discount is applied.
    day_basis : int or float
        The base period for interest rate conversion, also in days. Typical values are:
            - daily       = 1
            - monthly     = 30
            - working month (useful) = 21
            - quarterly   = 90
            - yearly (useful) = 252
            - yearly      = 360
            etc.

    Attributes
    ----------
    term : int or float
        The period, in days, for the calculation.
    day_basis : int or float
        The basis of calculation, in days, defining how the rates are interpreted for period conversion.

    Notes
    -----
    - The `term` must always be provided in **days**.
    - The `day_basis` is the period basis (also in days) for rate conversions.
    - This class supports three main capitalization regimes:
        - 'exp' : Exponential/compound regime (default)
        - 'lin' : Linear/simple regime
        - 'continuous' : Continuous compounding and discounting (via dedicated methods)
    - All formulas account for conversion between different time bases, allowing, for example,
      an annualized rate (basis 360 days) to be applied over any number of days.
    '''
    def __init__(self, term, day_basis):
        self.term = term
        self.day_basis = day_basis

    def discrete_present_value(
            self,
            target_value: float,
            fee: float,
            capitalization_regime: str = 'exp') -> float:
        '''
        Calculate the present value for a given future value using the specified capitalization regime.

        Parameters
        ----------
        target_value : float
            The future value to be discounted to the present.
        fee: float
            The fee used in the capitalization regime.
        capitalization_regime : {'exp', 'lin'}, default='exp'
            The regime of capitalization:
            - 'exp' : exponential/compound regime
            - 'lin' : linear/simple regime

        Returns
        -------
        present_value : float
            The present value corresponding to the given future value.

        Notes
        -----
        This method applies either the linear/simple (lin) or exponential/compound (exp) formula for present value
        calculation.
        The exponential regime discounts using compound interest, while the linear regime uses simple interest.

        Examples
        --------
        >>> cr = capitalization_regime(term=5, day_basis=1)
        >>> cr.discrete_present_value(30000, 0.08, capitalization_regime='exp')
        20417.5
        '''
        if capitalization_regime == 'lin':
            present_value = target_value / (1 + (fee * self.term / self.day_basis))
            return present_value

        elif capitalization_regime == 'exp':
            present_value = target_value / (1 + fee) ** (self.term / self.day_basis)
            return present_value

    def discrete_future_value(
            self,
            target_value: float,
            fee: float,
            capitalization_regime: str = 'exp') -> float:
        '''
        Calculate the future value for a given present value using the specified capitalization regime.

        Parameters
        ----------
        target_value : float
            The present value to be compounded to the future.
        fee: float
            The fee used in the capitalization regime.
        capitalization_regime : {'exp', 'lin'}, default='exp'
            The regime of capitalization:
            - 'exp' : exponential/compound regime
            - 'lin' : linear/simple regime

        Returns
        -------
        future_value : float
            The future value corresponding to the given present value.

        Notes
        -----
        This method applies either the linear/simple (lin) or exponential/compound (exp) formula for future value
        calculation.
        The exponential regime compounds using compound interest, while the linear regime uses simple interest.

        Examples
        --------
        >>> cr = capitalization_regime(term=5, day_basis=1)
        >>> cr.discrete_future_value(20000, 0.09, capitalization_regime='lin')
        29000.0
        '''
        if capitalization_regime == 'lin':
            present_value = target_value * (1 + (fee * self.term / self.day_basis))
            return present_value

        elif capitalization_regime == 'exp':
            present_value = target_value * (1 + fee) ** (self.term / self.day_basis)
            return present_value

    def discrete_effective_transaction_rate(
            self,
            future_target_value: float,
            present_target_value: float,
            capitalization_regime: str = 'exp') -> float:
        '''
        Calculate the effective transaction rate given the present and future values, according to the specified
        capitalization regime.

        Parameters
        ----------
        future_target_value : float
            The target amount in the future value of the transaction.
        present_target_value : float
            The present amount for the transaction.
        capitalization_regime : {'exp', 'lin'}, default='exp'
            The regime of capitalization:
            - 'exp' : exponential/compound regime
            - 'lin' : linear/simple regime

        Returns
        -------
        effective_transaction_rate : float
            The effective transaction rate corresponding to the given present and future values.

        Notes
        -----
        This method calculates the rate that equates the present value to the future value,
        depending on the capitalization regime provided.
        The exponential regime uses the compound interest formula, while the linear regime uses the simple
        interest formula.

        Examples
        --------
        >>> cr = capitalization_regime(term=5, day_basis=1)
        >>> cr.effective_transaction_rate(29000, 20000, capitalization_regime='lin')
        0.09
        '''
        if capitalization_regime == 'lin':
            etr = ((future_target_value / present_target_value) - 1) / (self.term / self.day_basis)
            return etr

        elif capitalization_regime == 'exp':
            etr = ((future_target_value / present_target_value) ** (1 / (self.term / self.day_basis))) - 1
            return etr

    def continuous_future_value(
            self,
            target_value: float,
            fee: float) -> float:
        '''
        Calculate the future value for a given present value using the continuous capitalization regime.

        Parameters
        ----------
        target_value : float
            The present value to be compounded continuously to the future.
        fee : float
            The rate used in the continuous capitalization regime.

        Returns
        -------
        future_value : float
            The future value corresponding to the given present value under continuous capitalization.

        Notes
        -----
        This method applies the continuous compounding formula using the exponential function. The calculation is
        based on the formula: FV = PV * e^(fee * (term / day_basis)), where e is Euler's number.

        Examples
        --------
        >>> cr = capitalization_regime(term=5, day_basis=1)
        >>> cr.continuous_future_value(20000, 0.09)
        31366.24
        '''
        euler_number = math.e
        future_value = target_value * (euler_number) ** (fee * (self.term / self.day_basis))
        return future_value

    def continuous_present_value(
            self,
            target_value: float,
            fee: float) -> float:
        '''
        Calculate the present value for a given future value using the continuous capitalization regime.

        Parameters
        ----------
        target_value : float
            The future value to be discounted to its present value.
        fee : float
            The rate used in the continuous capitalization regime.

        Returns
        -------
        present_value : float
            The present value corresponding to the given future value under continuous capitalization.

        Notes
        -----
        This method applies the continuous discounting formula using the exponential function. The calculation is
        based on the formula: PV = FV / e^(fee * (term / day_basis)), where e is Euler's number.

        Examples
        --------
        >>> cr = capitalization_regime(term=5, day_basis=1)
        >>> cr.continuous_present_value(31229.238405, 0.09)
        20000.0
        '''
        euler_number = math.e
        future_value = target_value / (euler_number) ** (fee * (self.term / self.day_basis))
        return future_value

    def continuous_effective_transaction_rate(
            self,
            future_target_value: float,
            present_target_value: float) -> float:
        '''
        Calculate the effective transaction rate for continuous capitalization, based on present and future values.

        Parameters
        ----------
        future_target_value : float
            The future value of the transaction.
        present_target_value : float
            The present value of the transaction.

        Returns
        -------
        effective_transaction_rate : float
            The effective transaction rate under continuous capitalization, as a decimal (not percentage).

        Notes
        -----
        This method applies the formula for continuous compounding to obtain the effective transaction rate. The
        calculation is performed as: rate = ln(future_target_value / present_target_value) / (term / day_basis),
        where ln is the natural logarithm.

        Examples
        --------
        >>> cr = capitalization_regime(term=3, day_basis=1)
        >>> cr.continuous_effective_transaction_rate(105.0, 100.0)
        0.016263
        '''
        etr = math.log(future_target_value / present_target_value) / (self.term / self.day_basis)
        return etr


class uniform_payments_series:
    '''
    Provides methods for calculating present value, future value, and payment values for uniform (equal) payment series
    under various conditions, including deferred (ordinary) and advance (annuity due) schemes.

    Parameters
    ----------
    term : int or float
        The total term (duration) of the payment series, **expressed in days**.
        This is the overall length across which the uniform payments occur.
    day_basis : int or float
        The basis of computation (in days) for the payments and period rate.
        Examples:
            - daily       = 1
            - monthly     = 30
            - working month (useful) = 21
            - quarterly   = 90
            - yearly (useful) = 252
            - yearly      = 360
            etc.

    Attributes
    ----------
    term : int or float
        The length of time (in days) over which the payments are made.
    day_basis : int or float
        The number of days that correspond to one payment period.

    Notes
    -----
    - The `term` parameter must always be provided in **days**.
    - The `day_basis` defines the time span for each interest/discount period and must also be expressed in days.
    - The class supports the calculation of both deferred (ordinary) series—payments at the end of periods—and
      advance (annuity due) series—payments at the beginning of periods.
    - These methods can be used for classical financial math problems such as loans (installment calculation),
      saving plans, or any context involving regular payments.
    '''
    def __init__(self, term, day_basis):
        self.term = term
        self.day_basis = day_basis

    def deferred_uniform_payments_series(
            self,
            fee: float,
            present_target_value: float = 1.00) -> float:
        '''
        Calculate the value of each payment in a deferred uniform payments series and the financing coefficient.

        Parameters
        ----------
        fee : float
            The rate used in the capitalization regime.
        present_target_value : float, default=1.00
            The present value to be financed by the uniform payments series.

        Returns
        -------
        payments_value : float
            The value of each uniform deferred payment in the series.
        financing_coef : float
            The coefficient used to calculate the payment value per present value.

        Notes
        -----
        This method computes the fixed payment amount for a deferred payment plan with uniform installments,
        using the formula for the present value of an ordinary annuity. The financing coefficient is also
        provided, representing the ratio between the payment and the present value.

        The calculation assumes that payments are made at the end of each period.

        Examples
        --------
        >>> ups = uniform_payments_series(term=12, day_basis=1)
        >>> ups.deferred_uniform_payments_series(0.02, 1000)
        (94.56, 0.09)
        '''
        payments_value = present_target_value * (((1 + fee) ** (self.term / self.day_basis)) * fee) / (
            ((1 + fee) ** (self.term / self.day_basis)) - 1)

        financing_coef = (((1 + fee) ** (self.term / self.day_basis)) * fee) / (
            ((1 + fee) ** (self.term / self.day_basis)) - 1)

        return payments_value, financing_coef

    def present_value_deferred_uniform_series(
            self,
            fee: float,
            payments: float = 1.00) -> float:
        '''
        Calculate the present value for a deferred uniform payments series given the payment amount and rate.

        Parameters
        ----------
        fee : float
            The rate used in the capitalization regime.
        payments : float, default=1.00
            The amount of each uniform deferred payment in the series.

        Returns
        -------
        present_value : float
            The present value equivalent to the specified deferred uniform payment series.

        Notes
        -----
        This method calculates the present value of an ordinary deferred annuity with uniform payments, using the
        formula for the present value of an annuity. It assumes payments are made at the end of each period.

        The calculation is based on: PV = payment * [(1+fee)^(term/day_basis) - 1] / [(1+fee)^(term/day_basis) * fee]

        Examples
        --------
        >>> ups = uniform_payments_series(term=12, day_basis=1)
        >>> ups.present_value_deferred_uniform_series(0.02, 100)
        1057.53
        '''
        present_value = payments * (((1 + fee) ** (self.term / self.day_basis)) - 1) / (
            ((1 + fee) ** (self.term / self.day_basis)) * fee)

        return present_value

    def advance_uniform_payments_series(
            self,
            fee: float,
            present_target_value: float = 1.00) -> float:
        '''
        Calculate the value of each payment in an advance (annuity due) uniform payments series and the
        corresponding financing coefficient.

        Parameters
        ----------
        fee : float
            The rate used in the capitalization regime.
        present_target_value : float, default=1.00
            The present value to be financed by the advance uniform payments series.

        Returns
        -------
        payments_value : float
            The value of each uniform payment in the advance (annuity due) payment series.
        financing_coef : float
            The coefficient used to calculate the payment value per present value for advance uniform payments.

        Notes
        -----
        This method calculates the fixed payment for an annuity due (payments made at the start of each period)
        and the respective financing coefficient. The computation is based on the formula:
        Payment = PV * [((1 + fee)^(term/day_basis) * fee) / ((1 + fee)^(term/day_basis) - 1)] * (1 / (1 + fee))

        Examples
        --------
        >>> ups = uniform_payments_series(term=12, day_basis=1)
        >>> ups.advance_uniform_payments_series(0.02, 1000)
        (92.71, 0.09)
        '''
        payments_value = present_target_value * ((((1 + fee) ** (self.term / self.day_basis)) * fee) / (
            ((1 + fee) ** (self.term / self.day_basis)) - 1)) * (1 / (1 + fee))

        financing_coef = ((((1 + fee) ** (self.term / self.day_basis)) * fee) / (
            ((1 + fee) ** (self.term / self.day_basis)) - 1)) * (1 / (1 + fee))

        return payments_value, financing_coef

    def present_value_advance_uniform_series(
            self,
            fee: float,
            payments: float = 1.00) -> float:
        '''
        Calculate the present value of an advance (annuity due) uniform payment series for a given payment and rate.

        Parameters
        ----------
        fee : float
            The rate used in the capitalization regime.
        payments : float, default=1.00
            The amount of each uniform advance payment in the series.

        Returns
        -------
        present_value : float
            The present value equivalent to the specified uniform payment series paid in advance (annuity due).

        Notes
        -----
        This method calculates the present value of an advance annuity (payments made at the start of each period),
        using the annuity due formula. The calculation is:
        PV = payment * [((1 + fee)^(term/day_basis) - 1) / ((1 + fee)^(term/day_basis) * fee)] * (1 + fee)

        Examples
        --------
        >>> ups = uniform_payments_series(term=12, day_basis=1)
        >>> ups.present_value_advance_uniform_series(0.02, 100)
        1078.68
        '''
        present_value = payments * (((1 + fee) ** (self.term / self.day_basis)) - 1) / (
            ((1 + fee) ** (self.term / self.day_basis)) * fee) * (1 + fee)

        return present_value

    def future_value_uniform_payments_series(
            self,
            fee: float,
            payments: float = 1.00,
            future_target_value: float = 1.00) -> float:
        '''
        Calculate the future value of a uniform payment series (ordinary annuity) and the required payment amount
        for a given future value.

        Parameters
        ----------
        fee : float
            The rate used in the capitalization regime.
        payments : float, default=1.00
            The amount of each regular payment in the series. Set to 1 to calculate only the future value.
        future_target_value : float, default=1.00
            The target accumulated future value of the series. Set to 1 to calculate only the payment value.

        Returns
        -------
        future_value : float
            The accumulated future value obtained by making periodic payments of the given amount.
        payments_value : float
            The amount of each payment required to reach the specified target future value.

        Notes
        -----
        This method returns both:
        - The future value given a payment amount: set `future_target_value=1.00` (default) and specify `payments`.
        - The payment required for a desired future value: set `payments=1.00` (default) and specify
        `future_target_value`.

        The calculation uses the formula:
        - FV = payments * [((1 + fee)^(term/day_basis) - 1) / fee]
        - Payment = future_target_value * [fee / ((1 + fee)^(term/day_basis) - 1)]
        '''
        future_value = payments * (((1 + fee) ** (self.term / self.day_basis)) - 1) / fee
        payments_value = future_target_value * (fee / (((1 + fee) ** (self.term / self.day_basis)) - 1))

        return future_value, payments_value


class investment_evaluation_methods:
    '''
    Provides static methods for classical investment appraisal: Net Present Value (NPV)
    and Internal Rate of Return (IRR). Supports calculation of NPV with time-varying discount
    rates (non-uniform cash flows and rates) and traditional IRR with a constant rate.

    Methods
    -------
    net_present_value(flows, rates)
        Calculate the Net Present Value (NPV) for a series of cash flows with possibly different discount
        rates per period.
    internal_rate_return(flows)
        Calculate the Internal Rate of Return (IRR) for a series of cash flows, assuming a constant rate throughout.

    Notes
    -----
    - NPV allows each period to have its own discount rate, and is suitable for analyses where market rates or
    project risks change over time.
    - The IRR method assumes that a single, constant rate applies for all periods; using it with time-varying
    rates is not recommended and may produce misleading results.
    - These methods are fundamental tools in financial mathematics for investment decisions, capital budgeting,
    and comparing project alternatives.
    '''
    @staticmethod
    def net_present_value(flows: list, rates: list) -> float:
        '''
        Calculate the Net Present Value (NPV) for a series of cash flows and discount rates that may vary over time.

        Parameters
        ----------
        flows : list of float
            The cash flows for each period. Positive values represent inflows, negative values represent outflows.
        rates : list of float
            The discount rate used in each period, in decimal form (e.g., 0.1 for 10%).

        Returns
        -------
        npv : float
            The Net Present Value (NPV) for the specified series of cash flows and discount rates.

        Notes
        -----
        This function calculates the present value of a non-uniform cash flow series,
        where both the cash flow and the interest rate may change each period.
        The formula used is:
            NPV = sum_{t=0}^{n} (FC_t / prod_{i=1}^{t} (1 + r_i))
        where FC_t is the cash flow at period t, and r_i is the rate for period i.

        Examples
        --------
        >>> flows = [-200000.00, 0, 0, 50000.00, 50000.00, 50000.00, 50000.00, 76000.00, 76000.00]
        >>> rates = [0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08]
        >>> net_present_value(flows, rates)
        27386.45
        '''
        if len(flows) != len(rates):
            raise ValueError("The lists of cash flows and rates must have the same length.")

        npv = 0.0
        discount_factor = 1.0
        for t in range(len(flows)):
            if t > 0:
                discount_factor *= (1 + rates[t])
            npv += flows[t] / discount_factor

        return npv

    @staticmethod
    def internal_rate_return(flows: list) -> float:
        '''
        Calculate the Internal Rate of Return (IRR) for a series of cash flows using a constant rate.

        Parameters
        ----------
        flows : list of float
            The cash flows for each period. Positive values represent inflows, negative values represent outflows.

        Returns
        -------
        irr : float
            The Internal Rate of Return (IRR) as a decimal (e.g., 0.12 for 12%).

        Notes
        -----
        This method calculates the IRR assuming that the discount rate remains constant throughout all periods.
        If the discount rates vary from period to period, this method is not appropriate and may produce misleading
        results.
        In financial analysis, IRR is the single rate that makes the net present value (NPV) of the cash flows equal to
        zero.

        Examples
        --------
        >>> flows = [-10000.00, 2500.00, 2500.00, 2500.00, 3000.00, 3000.00]
        >>> internal_rate_return(flows)
        0.1048
        '''
        irr = npf.irr(flows)
        return irr
