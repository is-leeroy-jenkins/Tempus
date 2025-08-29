###### tempus
![](https://github.com/is-leeroy-jenkins/Tempus/blob/master/resources/images/github/project_tempus.png)

> Modern Fiscal & Calendar Utilities for Python  
> Precise, production-ready tools to unify U.S. fiscal year (FY) and calendar year (CY) calculations, including workdays, weekends, and official U.S. federal holidays — all with a clean, well-documented API.



### 📝 Features

- **Fiscal Year Engine**  
  Compute CY, FY, Beginning/Ending FY (BBFY/EBFY), and both calendar/fiscal boundaries.

- **Elapsed & Remaining Counters**  
  Days, months, day-of-year indices, and percent elapsed for both CY and FY.

- **Federal Holiday Logic**  
  Actual and observed U.S. federal holidays, filtered to the active fiscal window.

- **Range Utilities**  
  Count workdays, weekends, and holidays between any two dates.

- **Production-Hardened**  
  Guard clauses, consistent error handling, rich docstrings, and deterministic calculations.



### 🏗️ Installation

- Use pip:

```

    pip install tempus
  
```

- Or add via Poetry (pyproject.toml):

```
    [tool.poetry.dependencies]
    tempus = "^1.0.0"
  
 ```



### 🎯 Quick Start

    from datetime import date
    from tempus import FiscalYear, FederalHoliday

    # Bind a date to FiscalYear
    bfy = FiscalYear(date(2025, 8, 27))

    print(bfy.fiscal_year)                     # 2025
    print(bfy.beginning_fiscal_year, bfy.ending_fiscal_year)  # 2024 2025
    print(round(bfy.fiscal_percent_elapsed(), 2))             # e.g., 91.23

    # Range utilities
    print(bfy.count_workdays(date(2025, 8, 1), date(2025, 8, 31)))
    print(bfy.count_weekends(date(2025, 8, 1), date(2025, 8, 31)))
    print(bfy.count_holidays(date(2025, 1, 1), date(2025, 9, 30)))

    # Holiday checks
    hol = FederalHoliday(bfy.fiscal_year)
    print(hol.is_holiday(date(2025, 7, 4)))    # True (Independence Day)
    print(hol.is_weekend(date(2025, 7, 5)))    # True (Saturday)



### 🧠 API Overview

#### BudgetFiscalYear

- calendar: `calendar_day_of_year()`, `calendar_days_in_year()`, `calendar_elapsed_days()`, `calendar_remaining_days()`, `calendar_elapsed_months()`, `calendar_remaining_months()`, `calendar_percent_elapsed()`
- fiscal: `fiscal_day_of_year()`, `fiscal_days_in_year()`, `fiscal_month_number()`, `fiscal_elapsed_days()`, `fiscal_remaining_days()`, `fiscal_elapsed_months()`, `fiscal_remaining_months()`, `fiscal_percent_elapsed()`
- ranges: `count_weekends(start, end)`, `count_holidays(start, end)`, `count_workdays(start, end)`
- bounds & checks: `calendar_bounds()`, `fiscal_bounds()`, `is_calendar_year_start()`, `is_calendar_year_end()`, `is_fiscal_year_start()`, `is_fiscal_year_end()`

#### FederalHoliday

- `holidays() -> dict` — holiday map with `actual` and `observed` dates within the FY window  
- `is_holiday(date, use_observed=True) -> bool`  
- `is_weekend(date) -> bool`



### 📝 Design Notes

- **FY Naming**: FY is named for its ending year. For example, FY 2026 runs 2025-10-01 through 2026-09-30.  
- **Observed Dates**: Saturday holidays observe on Friday; Sunday on Monday.  
- **Juneteenth**: Included from FY 2021 forward.  
- **Determinism**: All calculations are pure functions of the input date(s); no I/O or timezone side-effects.



### 🏁 Roadmap

- ISO week numbers and fiscal week helpers  
- Optional state/local holiday overlays  
- CLI (`tempus`) for shell-friendly queries  
- Pandas integration for DataFrame fiscal transformations



### 🚀 Contributing

1. Fork and create a feature branch.  
2. Follow PEP 8 and include Purpose / Parameters / Returns docstrings.  
3. Add tests for all new logic.  
4. Submit a PR with a clear description and examples.



### 📜 [License](https://github.com/is-leeroy-jenkins/Tempus/blob/master/LICENSE.txt)

- MIT © 2025 Terry D. Eppler
