'''
    ******************************************************************************************
      Assembly:                FiscalTools
      Filename:                budget_fiscal_year.py
      Author:                  Terry D. Eppler
      Created:                 08-26-2025
    
      Last Modified By:        Terry D. Eppler
      Last Modified On:        08-26-2025
    ******************************************************************************************
    <copyright file="budget_fiscal_year.py" company="Terry D. Eppler">
    
         Budget Tempus Year Tools
    
     Permission is hereby granted, free of charge, to any person obtaining a copy
     of this software and associated documentation files (the “Software”),
     to deal in the Software without restriction,
     including without limitation the rights to use,
     copy, modify, merge, publish, distribute, sublicense,
     and/or sell copies of the Software,
     and to permit persons to whom the Software is furnished to do so,
     subject to the following conditions:
    
     The above copyright notice and this permission notice shall be included in all
     copies or substantial portions of the Software.
    
     THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
     INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
     FITNESS FOR A PARTICULAR PURPOSE AND NON-INFRINGEMENT.
     IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
     DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
     ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
     DEALINGS IN THE SOFTWARE.
    
     You can contact me at:  terryeppler@gmail.com or eppler.terry@epa.gov
    
    </copyright>
    <summary>
        budget_fiscal_year.py
    </summary>
    ******************************************************************************************
'''
from __future__ import annotations
from datetime import date, datetime, timedelta
from typing import Dict, List, Tuple
import calendar
from booger import Error, ErrorDialog 


def throw_if( name: str, value: object ) -> None:
    """
        
        Purpose:
        --------
        Simple guard that raises ValueError if `value` is falsy.
    
        Parameters:
        -----------
        name (str): Variable name used in error message.
        value (object): Value to validate.
    
        Returns:
        --------
        None
    
    """
    if not value:
        raise ValueError( f'Argument "{name}" cannot be empty!' )


def _to_date( value: date | datetime | None ) -> date:
    """
        
        Purpose:
        --------
        Normalize supported date-like inputs to `datetime.date`.
    
        Parameters:
        -----------
        value (date | datetime | None): Input; None -> today().
    
        Returns:
        --------
        date: Normalized date.
    
    """
    if value is None:
        return date.today( )
    if isinstance( value, datetime ):
        return value.date( )
    if isinstance( value, date ):
        return value


# noinspection PyTypeChecker
class FiscalYear( ):
    """
        
        Purpose:
        --------
        Encapsulate U.S. federal Budget Tempus Year (FY) logic. Given any calendar date,
        compute Calendar Year (CY), Tempus Year (FY), Beginning/Ending FY (BBFY/EBFY), and
        both calendar and fiscal year boundaries. Provide elapsed/remaining days and months,
        day-of-year indices, percent complete, and convenience boundary/holiday checks.
        
    """
    
    date: date
    today: datetime
    current_date: datetime
    calendar_year: int
    fiscal_year: int
    beginning_fiscal_year: int
    ending_fiscal_year: int
    cy_start_date: datetime
    cy_end_date: datetime
    fy_start_date: datetime
    fy_end_date: datetime
    
    
    def __init__( self, current_date: datetime | None ) -> None:
        """
        Purpose:
        --------
        Initialize fiscal/calendar state for a given date (defaults to today).

        Parameters:
        -----------
        current_date (date | datetime | None): Reference date; if None, uses today().

        Returns:
        --------
        None
        """
        try:
            self.current_date = current_date
            self.today = _to_date( self.current_date )
            self._bind( self.today )
        except Exception as e:
            exception = Error( e )
            exception.module = 'fiscal'
            exception.cause = 'FiscalYear'
            exception.method = '__init__(self, current_date)'
            error = ErrorDialog( exception )
            error.show( )
    
    
    def __repr__( self ) -> str:
        """
            
            Purpose:
            --------
            Provide concise string representation for debugging/logging.
    
            Returns:
            --------
            str: Human-readable summary.
            
        """
        return (
                f"BudgetFiscalYear(date={self.date.isoformat( )}, CY={self.calendar_year}, "
                f"FY={self.fiscal_year}, BBFY={self.beginning_fiscal_year}, "
                f"EBFY={self.ending_fiscal_year})"
        )
    
    
    def _bind( self, d: datetime ) -> None:
        """
            
            Purpose:
            --------
            (Re)bind the object to a concrete date and recompute all boundaries/fields.
    
            Parameters:
            -----------
            d (date): Reference date.
    
            Returns:
            --------
            None
        
        """
        try:
            throw_if( 'd', d )
            self.date = d
            self.calendar_year = d.year
            if d.month >= 10:
                self.fiscal_year = d.year + 1
                self.beginning_fiscal_year = d.year
                self.ending_fiscal_year = d.year + 1
                self.fy_start_date = datetime( d.year, 10, 1 )
                self.fy_end_date = datetime( d.year + 1, 9, 30 )
            else:
                self.fiscal_year = d.year
                self.beginning_fiscal_year = d.year - 1
                self.ending_fiscal_year = d.year
                self.fy_start_date = datetime( d.year - 1, 10, 1 )
                self.fy_end_date = datetime( d.year, 9, 30 )
            self.cy_start_date = datetime( d.year, 1, 1 )
            self.cy_end_date = datetime( d.year, 12, 31 )
        except Exception as e:
            exception = Error( e )
            exception.module = 'tempus'
            exception.cause = ''
            exception.method = ''
            error = ErrorDialog( exception )
            error.show( )
    

    def calendar_day_of_year( self ) -> int:
        """
            
            Purpose:
            --------
            Get the 1-based day-of-year index within the Calendar Year.
    
            Returns:
            --------
            int: Value in 1..366.
        
        """
        try:
            return (self.date - self.cy_start_date).days + 1
        except Exception as e:
            exception = Error( e )
            exception.module = 'tempus'
            exception.cause = ''
            exception.method = ''
            error = ErrorDialog( exception )
            error.show( )
    
    
    def calendar_days_in_year( self ) -> int:
        """
        
            Purpose:
            --------
            Get the total number of days in the Calendar Year.
    
            Returns:
            --------
            int: 365 or 366.
            
        """
        try:
            return (self.cy_end_date - self.cy_start_date).days + 1
        except Exception as e:
            exception = Error( e )
            exception.module = 'tempus'
            exception.cause = ''
            exception.method = ''
            error = ErrorDialog( exception )
            error.show( )
    
    
    def calendar_elapsed_days( self ) -> int:
        """
        
            Purpose:
            --------
            Compute completed days elapsed in the Calendar Year as of `self.date`.
    
            Returns:
            --------
            int: Number of days.
        
        """
        try:
            return max( 0, (self.date - self.cy_start_date).days )
        except Exception as e:
            exception = Error( e )
            exception.module = 'tempus'
            exception.cause = ''
            exception.method = ''
            error = ErrorDialog( exception )
            error.show( )
    
    
    def calendar_remaining_days( self ) -> int:
        """
            
            Purpose:
            --------
            Compute remaining days in the Calendar Year after `self.date`.
    
            Returns:
            --------
            int: Number of days.
        
        """
        try:
            return max( 0, (self.cy_end_date - self.date).days )
        except Exception as e:
            exception = Error( e )
            exception.module = 'tempus'
            exception.cause = ''
            exception.method = ''
            error = ErrorDialog( exception )
            error.show( )
    
    
    def calendar_elapsed_months( self ) -> int:
        """
        
            Purpose:
            --------
            Compute completed months elapsed in the Calendar Year.
    
            Returns:
            --------
            int: 0..11
        
        """
        try:
            return max( 0, self.date.month - 1 )
        except Exception as e:
            exception = Error( e )
            exception.module = 'tempus'
            exception.cause = ''
            exception.method = ''
            error = ErrorDialog( exception )
            error.show( )
    
    
    def calendar_remaining_months( self ) -> int:
        """
        
            Purpose:
            --------
            Compute months remaining in the Calendar Year after current month.
    
            Returns:
            --------
            int: 0..11
        
        """
        try:
            return 12 - self.date.month
        except Exception as e:
            exception = Error( e )
            exception.module = 'tempus'
            exception.cause = ''
            exception.method = ''
            error = ErrorDialog( exception )
            error.show( )
    
    
    def calendar_percent_elapsed( self ) -> float:
        """
        
            Purpose:
            --------
            Compute percentage of the Calendar Year completed as of `self.date`.
    
            Returns:
            --------
            float: Percentage 0.0–100.0
        
        """
        try:
            completed = self.calendar_elapsed_days( )
            total = self.calendar_days_in_year( )
            return (completed / total) * 100.0
        except Exception as e:
            exception = Error( e )
            exception.module = 'tempus'
            exception.cause = ''
            exception.method = ''
            error = ErrorDialog( exception )
            error.show( )
    

    def fiscal_day_of_year( self ) -> int:
        """
            
            Purpose:
            --------
            Get the 1-based day-of-year index within the Tempus Year.
    
            Returns:
            --------
            int: Value in 1..366.
        
        """
        try:
            return ( self.date - self.fy_start_date ) + 1
        except Exception as e:
            exception = Error( e )
            exception.module = 'tempus'
            exception.cause = ''
            exception.method = ''
            error = ErrorDialog( exception )
            error.show( )
    
    
    def fiscal_days_in_year( self ) -> int:
        """
        
            Purpose:
            --------
            Get the total number of days in the Tempus Year.
    
            Returns:
            --------
            int: 365 or 366.
        
        """
        try:
            return (self.fy_end_date - self.fy_start_date).days + 1
        except Exception as e:
            exception = Error( e )
            exception.module = 'tempus'
            exception.cause = ''
            exception.method = ''
            error = ErrorDialog( exception )
            error.show( )
    
    
    def fiscal_month_number( self ) -> int:
        """
        
            Purpose:
            --------
            Get the fiscal month number (Oct=1 .. Sep=12).
    
            Returns:
            --------
            int: 1..12
        
        """
        try:
            m = self.date.month
            return ((m - 10) % 12) + 1
        except Exception as e:
            exception = Error( e )
            exception.module = 'tempus'
            exception.cause = ''
            exception.method = ''
            error = ErrorDialog( exception )
            error.show( )
    
    
    def fiscal_elapsed_days( self ) -> int:
        """
            
            Purpose:
            --------
            Compute completed days elapsed in the Tempus Year.
    
            Returns:
            --------
            int: Number of days.
        
        """
        try:
            return max( 0, (self.date - self.fy_start_date)  )
        except Exception as e:
            exception = Error( e )
            exception.module = 'tempus'
            exception.cause = ''
            exception.method = ''
            error = ErrorDialog( exception )
            error.show( )
    
    
    def fiscal_days_remaining( self ) -> int:
        """
        
            Purpose:
            --------
            Compute remaining days in the Tempus Year after `self.date`.
    
            Returns:
            --------
            int: Number of days.
        
        """
        try:
            return max( 0, ( self.fy_end_date - self.date ).days )
        except Exception as e:
            exception = Error( e )
            exception.module = 'tempus'
            exception.cause = ''
            exception.method = ''
            error = ErrorDialog( exception )
            error.show( )
    
    
    def fiscal_elapsed_months( self ) -> int:
        """
            
            Purpose:
            --------
            Compute completed months elapsed in the Tempus Year.
    
            Returns:
            --------
            int: 0..11
        
        """
        try:
            return self.fiscal_month_number( ) - 1
        except Exception as e:
            exception = Error( e )
            exception.module = 'tempus'
            exception.cause = ''
            exception.method = ''
            error = ErrorDialog( exception )
            error.show( )
    
    
    def fiscal_remaining_months( self ) -> int:
        """
        
            Purpose:
            --------
            Compute remaining months in the Tempus Year.
    
            Returns:
            --------
            int: 0..11
        
        """
        try:
            return 12 - self.fiscal_month_number( )
        except Exception as e:
            exception = Error( e )
            exception.module = 'tempus'
            exception.cause = ''
            exception.method = ''
            error = ErrorDialog( exception )
            error.show( )
    
    
    def fiscal_percent_elapsed( self ) -> float:
        """
        
            Purpose:
            --------
            Compute percentage of the Tempus Year completed.
    
            Returns:
            --------
            float: Percentage 0.0–100.0
        
        """
        try:
            completed = self.fiscal_elapsed_days( )
            total = self.fiscal_days_in_year( )
            return (completed / total) * 100.0
        except Exception as e:
            exception = Error( e )
            exception.module = 'tempus'
            exception.cause = ''
            exception.method = ''
            error = ErrorDialog( exception )
            error.show( )
    
    
    def count_weekends( self, start: datetime, end: datetime ) -> int:
        """
        
            Purpose:
            --------
            Count the number of weekend days (Saturday/Sunday) between two dates inclusive.
    
            Parameters:
            -----------
            start (date | datetime): Start date.
            end (date | datetime): End date.
    
            Returns:
            --------
            int: Number of weekend days.
        
        """
        try:
            s, e = _to_date( start ), _to_date( end )
            if s > e:
                return 0
            count = 0
            cur = s
            while cur <= e:
                if cur.weekday( ) >= 5:
                    count += 1
                cur += timedelta( days=1 )
            return count
        except Exception as e:
            exception = Error( e )
            exception.module = 'fiscal'
            exception.cause = 'FiscalYear'
            exception.method = 'count_weekends(self, start, end)'
            error = ErrorDialog( exception )
            error.show( )
    
    
    def count_holidays( self, start: datetime, end: datetime, use_observed: bool = True ) -> int:
        """
        
            Purpose:
            --------
            Count the number of U.S. federal holidays between two dates inclusive, restricted
            to this Tempus Year.
    
            Parameters:
            -----------
            start (date | datetime): Start date.
            end (date | datetime): End date.
            use_observed (bool): Count observed holidays if True; otherwise actual.
    
            Returns:
            --------
            int: Number of holidays in range.
        
        """
        try:
            s, e = _to_date( start ), _to_date( end )
            if s > e:
                return 0
            fh = FederalHoliday( self.fiscal_year )
            hols = fh.holidays( )
            key = 'observed' if use_observed else 'actual'
            return sum( 1 for payload in hols.values( ) if s <= payload[ key ] <= e )
        except Exception as e:
            exception = Error( e )
            exception.module = 'fiscal'
            exception.cause = 'FiscalYear'
            exception.method = 'count_holidays(self, start, end)'
            error = ErrorDialog( exception )
            error.show( )
    
    
    def count_workdays( self, start: datetime, end: datetime, use_observed: bool = True ) -> int:
        """
        
            Purpose:
            --------
            Count the number of business days (Mon–Fri excluding holidays) between two dates
            inclusive, restricted to this Tempus Year.
    
            Parameters:
            -----------
            start (date | datetime): Start date.
            end (date | datetime): End date.
            use_observed (bool): Exclude observed holidays if True; otherwise actual.
    
            Returns:
            --------
            int: Number of business days.
        
        """
        try:
            s, e = _to_date( start ), _to_date( end )
            if s > e:
                return 0
            fh = FederalHoliday( self.fiscal_year )
            hols = fh.holidays( )
            hset = { payload[ 'observed' if use_observed else 'actual' ] for payload in
                     hols.values( ) }
            count, cur = 0, s
            while cur <= e:
                if cur.weekday( ) < 5 and cur not in hset:
                    count += 1
                cur += timedelta( days=1 )
            return count
        except Exception as e:
            exception = Error( e )
            exception.module = 'fiscal'
            exception.cause = 'FiscalYear'
            exception.method = 'count_workdays(self, start, end)'
            error = ErrorDialog( exception )
            error.show( )
    
    
    def calendar_bounds( self ) -> Tuple[ date, date ]:
        """
            
            Purpose:
            --------
            Get the start/end dates for the Calendar Year containing `self.date`.
    
            Returns:
            --------
            (date, date): (calendar_start, calendar_end)
            
        """
        try:
            return self.cy_start_date, self.cy_end_date
        except Exception as e:
            exception = Error( e )
            exception.module = 'tempus'
            exception.cause = ''
            exception.method = ''
            error = ErrorDialog( exception )
            error.show( )
    
    
    def fiscal_bounfds( self ) -> Tuple[ date, date ]:
        """
        
            Purpose:
            --------
            Get the start/end dates for the Tempus Year containing `self.date`.
    
            Returns:
            --------
            (date, date): (fiscal_start, fiscal_end)
        
        """
        try:
            return self.fy_start_date, self.fy_end_date
        except Exception as e:
            exception = Error( e )
            exception.module = 'tempus'
            exception.cause = ''
            exception.method = ''
            error = ErrorDialog( exception )
            error.show( )
    
    
    def is_fiscal_start_year( self ) -> bool:
        """
        
            Purpose:
            --------
            Determine whether `self.date` is the first day of the Tempus Year (Oct 1).
    
            Returns:
            --------
            bool: True/False
        
        """
        try:
            return self.date == self.fy_start_date
        except Exception as e:
            exception = Error( e )
            exception.module = 'tempus'
            exception.cause = ''
            exception.method = ''
            error = ErrorDialog( exception )
            error.show( )
    
    
    def is_fiscal_end_year( self ) -> bool:
        """
        
            Purpose:
            --------
            Determine whether `self.date` is the last day of the Tempus Year (Sep 30).
    
            Returns:
            --------
            bool: True/False
        
        """
        try:
            return self.date == self.fy_end_date
        except Exception as e:
            exception = Error( e )
            exception.module = 'tempus'
            exception.cause = ''
            exception.method = ''
            error = ErrorDialog( exception )
            error.show( )
    
    
    def is_calendar_start_year( self ) -> bool:
        """
        
            Purpose:
            --------
            Determine whether `self.date` is Jan 1 of its Calendar Year.
    
            Returns:
            --------
            bool: True/False
        
        """
        try:
            return self.date == self.cy_start_date
        except Exception as e:
            exception = Error( e )
            exception.module = 'tempus'
            exception.cause = ''
            exception.method = ''
            error = ErrorDialog( exception )
            error.show( )
    
    
    def is_calendar_end_date( self ) -> bool:
        """
        
            Purpose:
            --------
            Determine whether `self.date` is Dec 31 of its Calendar Year.
    
            Returns:
            --------
            bool: True/False
        
        """
        try:
            return self.date == self.cy_end_date
        except Exception as e:
            exception = Error( e )
            exception.module = 'tempus'
            exception.cause = ''
            exception.method = ''
            error = ErrorDialog( exception )
            error.show( )
    
    
    def to_dict( self ) -> Dict[ str, object ]:
        """
            
            Purpose:
            --------
            Export a structured snapshot of the current state for logging/BI.
    
            Returns:
            --------
            dict: Field/value mapping.
        
        """
        return {
                'date': self.date,
                'calendar_year': self.calendar_year,
                'fiscal_year': self.fiscal_year,
                'beginning_fiscal_year': self.beginning_fiscal_year,
                'ending_fiscal_year': self.ending_fiscal_year,
                'cy_start_date': self.cy_start_date,
                'cy_end_date': self.cy_end_date,
                'fy_start_date': self.fy_start_date,
                'fy_end_date': self.fy_end_date,
        }


class FederalHoliday:
    """
    
        Purpose:
        --------
        Encapsulate U.S. federal holiday logic for a specific Tempus Year (FY). Computes
        actual and observed holiday dates that fall within the fiscal-year window.
    
        Fields:
        -------
        fiscal_year (int): The FY for which holidays are computed (FY named for its end year).
        fy_start (date): Start of FY -> Oct 1 of (fiscal_year - 1).
        fy_end (date): End of FY -> Sep 30 of (fiscal_year).
        
    """
    fiscal_year: int
    fy_start_date: date
    fy_end_date: date
    holidays: Dict[ str, Dict[ str, date ] ]
    
    
    def __init__( self, fiscal_year: int ) -> None:
        """
        
            Purpose:
            --------
            Initialize a FederalHoliday instance for a fiscal year.
    
            Parameters:
            -----------
            fiscal_year (int): Tempus year label (end year).
    
            Returns:
            --------
            None
        
        """
        self.fiscal_year = int( fiscal_year )
        self.fy_start_date = date( self.fiscal_year - 1, 10, 1 )
        self.fy_end_date = date( self.fiscal_year, 9, 30 )
    
    
    def _observed_date( self, d: date ) -> date | None:
        """
            
            Purpose:
            --------
            Compute the observed date if a holiday falls on a weekend.
    
            Parameters:
            -----------
            d (date): Actual holiday date.
    
            Returns:
            --------
            date: Observed holiday date.
        
        """
        try:
            if d.weekday( ) == 5:
                return d - timedelta( days=1 )
            if d.weekday( ) == 6:
                return d + timedelta( days=1 )
            return d
        except Exception as e:
            exception = Error( e )
            exception.module = 'tempus'
            exception.cause = ''
            exception.method = ''
            error = ErrorDialog( exception )
            error.show( )
    
    
    def _nth_weekday_of_month( self, year: int, month: int, weekday: int, n: int ) -> date | None:
        """
            
            Purpose:
            --------
            Compute the date of the n-th weekday in a given month/year.
    
            Parameters:
            -----------
            year (int): Calendar year.
            month (int): Calendar month (1–12).
            weekday (int): Target weekday (0=Monday .. 6=Sunday).
            n (int): Occurrence index (e.g., 3 = third Monday).
    
            Returns:
            --------
            date: The date of the n-th weekday.
        
        """
        try:
            cal = calendar.Calendar( )
            matches = [ d for d in cal.itermonthdates( year, month )
                        if d.month == month and d.weekday( ) == weekday ]
            return matches[ n - 1 ]
        except Exception as e:
            exception = Error( e )
            exception.module = 'tempus'
            exception.cause = ''
            exception.method = ''
            error = ErrorDialog( exception )
            error.show( )
    
    
    def _last_weekday_of_month( self, year: int, month: int, weekday: int ) -> date | None:
        """
        
            Purpose:
            --------
            Compute the date of the last given weekday in a month/year.
    
            Parameters:
            -----------
            year (int): Calendar year.
            month (int): Calendar month (1–12).
            weekday (int): Target weekday (0=Monday .. 6=Sunday).
    
            Returns:
            --------
            date: The date of the last weekday.
        
        """
        try:
            cal = calendar.Calendar( )
            matches = [ d for d in cal.itermonthdates( year, month )
                        if d.month == month and d.weekday( ) == weekday ]
            return matches[ -1 ]
        except Exception as e:
            exception = Error( e )
            exception.module = 'tempus'
            exception.cause = ''
            exception.method = ''
            error = ErrorDialog( exception )
            error.show( )
    
    
    def _add_holiday( self, hols: Dict[ str, Dict[ str, date ] ], name: str, actual: date ) -> None:
        """
        
            Purpose:
            --------
            Add a holiday to the holiday dictionary if the observed date is within the
            fiscal-year window.
        
        
            Parameters:
            -----------
            hols (dict): The holiday dictionary being built.
            name (str): Holiday name.
            actual (date): Actual holiday date.
        
        
            Returns:
            --------
            None
        
        """
        try:
            obs = self._observed_date( actual )
            if self.fy_start_date <= obs <= self.fy_end_date:
                hols[ name ] = { 'actual': actual, 'observed': obs }
        except Exception as e:
            exception = Error( e )
            exception.module = 'tempus'
            exception.cause = 'FederalHoliday'
            exception.method = ''
            error = ErrorDialog( exception )
            error.show( )
    
    
    def holidays( self ) -> Dict[ str, Dict[ str, date ] ] | None:
        """
        
            Purpose:
            --------
            Compute the set of U.S. federal holidays for this fiscal year. Only holidays whose
            observed date falls within the fiscal window (Oct 1 of FY-1 through Sep 30 of FY)
            are included.
            
            Parameters:
            -----------
            None
            
            Returns:
            --------
            Dict[str, Dict[str, date]]: A mapping of holiday name to a dictionary containing:
            - 'actual': The actual calendar date of the holiday.
            - 'observed': The observed date (adjusted for weekends).
            
        """
        try:
            hols: Dict[ str, Dict[ str, date ] ] = { }
            start = self.fy_start_date.year
            end = self.fiscal_year
            self._add_holiday( hols, 'Columbus Day',
            self._nth_weekday_of_month( start, 10, calendar.MONDAY, 2 ) )
            self._add_holiday( hols, 'Veterans Day', date( start, 11, 11 ) )
            self._add_holiday( hols, 'Thanksgiving Day',
            self._nth_weekday_of_month( start, 11, calendar.THURSDAY, 4 ) )
            self._add_holiday( hols, 'Christmas Day', date( start, 12, 25 ) )
            self._add_holiday( hols, "New Year's Day", date( end, 1, 1 ) )
            self._add_holiday( hols, 'Birthday of Martin Luther King, Jr.',
            self._nth_weekday_of_month( end, 1, calendar.MONDAY, 3 ) )
            self._add_holiday( hols, "Washington's Birthday",
            self._nth_weekday_of_month( end, 2, calendar.MONDAY, 3 ) )
            self._add_holiday( hols, 'Memorial Day',
            self._last_weekday_of_month( end, 5, calendar.MONDAY ) )
            self._add_holiday( hols, 'Juneteenth National Independence Day', date( end, 6, 19 ) )
            self._add_holiday( hols, 'Independence Day', date( end, 7, 4 ) )
            self._add_holiday( hols, 'Labor Day',
            self._nth_weekday_of_month( end, 9, calendar.MONDAY, 1 ) )
            return hols
        except Exception as e:
            exception = Error( e )
            exception.module = 'tempus'
            exception.cause = 'FederalHoliday'
            exception.method = 'holidays( self ) -> Dict[ str, Dict[ str, date ] ]'
            error = ErrorDialog( exception )
            error.show( )
    
    
    def is_holiday( self, when: datetime, observed: bool=True ) -> bool | None:
        """
            
            Purpose:
            --------
            Determine whether a given date is a federal holiday for this FY.
    
            Parameters:
            -----------
            when (date | datetime): Date to evaluate.
            use_observed (bool): If True, compare against observed dates; otherwise actual.
    
            Returns:
            --------
            bool: True if the date is a holiday in this FY; False otherwise.
        
        """
        try:
            d = _to_date( when )
            hols = self.holidays( )
            if observed:
                return any( d == payload[ 'observed' ] for payload in hols.values( ) )
            return any( d == payload[ 'actual' ] for payload in hols.values( ) )
        except Exception as e:
            exception = Error( e )
            exception.module = 'tempus'
            exception.cause = 'FederalHoliday'
            exception.method = 'is_holiday( self, when: datetime, use_observed: bool=True ) -> bool'
            error = ErrorDialog( exception )
            error.show( )
    
    
    def is_weekend( self, when: datetime ) -> bool | None:
        """
            
            Purpose:
            --------
            Determine whether a given date falls on a weekend (Saturday/Sunday).
    
            Parameters:
            -----------
            when (date | datetime): Date to evaluate.
    
            Returns:
            --------
            bool: True if Saturday or Sunday; otherwise False.
            
        """
        try:
            throw_if( 'when', when )
            d = _to_date( when )
            return d.weekday( ) >= 5
        except Exception as e:
            exception = Error( e )
            exception.module = 'tempus'
            exception.cause = 'FederalHoliday'
            exception.method = 'is_weekend( self, when: datetime ) -> bool '
            error = ErrorDialog( exception )
            error.show( )
