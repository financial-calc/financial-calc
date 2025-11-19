"""
Financial interest rates operations
Author: Vitor Beltrao Abdo - vitorbeltrao300@gmail.com
"""


class equivalent_rates:

    def __init__(
        self,
        term_to_convert,
        day_basis_to_convert,
        rate_to_convert,
        required_term,
        required_day_basis,
    ):

        self.term_to_convert = term_to_convert
        self.day_basis_to_convert = day_basis_to_convert
        self.rate_to_convert = rate_to_convert
        self.required_term = required_term
        self.required_day_basis = required_day_basis

    def calculate_equivalent_rates(self, capitalization_regime="exp"):
        """
        Calculate the equivalent rate for a given capitalization regime and period conversion.

        Parameters
        ----------
        capitalization_regime : str, default='exp'
            The capitalization regime for the calculation.
            - 'exp' : Exponential (compound) regime.
            - 'lin' : Linear (simple interest) regime.

        Returns
        -------
        required_rate : float
            The equivalent rate for the specified regime and period conversion.

        Notes
        -----
        This method calculates the equivalent interest rate for converting from one period (term/day_basis)
        to another, according to the selected capitalization regime:
            - For 'lin' (linear/simple): proportional rate conversion.
            - For 'exp' (exponential/compound): equivalent compound rate conversion.

        The calculation uses attributes:
            - self.rate_to_convert: the original rate to convert.
            - self.term_to_convert: the term of the original rate.
            - self.day_basis_to_convert: the day basis of the original rate.
            - self.required_term: the required converted period.
            - self.required_day_basis: the day basis of the required period.

        Examples
        --------
        >>> er = equivalent_rates(360, 360, 0.30, 360, 90, 6.78)
        >>> required_rate = er.calculate_equivalent_rates(capitalization_regime='exp')
        0.0678
        """
        if capitalization_regime == "lin":
            required_rate = (
                self.rate_to_convert
                * (self.term_to_convert / self.day_basis_to_convert)
                / (self.required_term / self.required_day_basis)
            )
            return required_rate

        elif capitalization_regime == "exp":
            required_rate = (
                (1 + self.rate_to_convert)
                ** (
                    (self.term_to_convert / self.day_basis_to_convert)
                    / (self.required_term / self.required_day_basis)
                )
            ) - 1
            return required_rate
