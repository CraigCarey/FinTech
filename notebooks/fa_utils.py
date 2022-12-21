from datetime import datetime

import fa_mods as famods
import fundamentalanalysis as fa
import pandas as pd


def get_ticker_data(ticker: str, api_key: str):
    data = {}
    data["timestamp"] = datetime.timestamp(datetime.now())
    data["income_statement"] = fa.income_statement(
        ticker, api_key, period="annual"
    ).drop(labels=["calendarYear", "period", "link", "finalLink"], axis=0)
    data["income_statement_growth"] = famods.income_statement_growth(ticker, api_key)
    data["cashflow_statement"] = fa.cash_flow_statement(
        ticker, api_key, period="annual"
    ).drop(labels=["calendarYear", "period", "link", "finalLink"], axis=0)
    data["cashflow_statement_growth"] = famods.cash_flow_statement_growth(
        ticker, api_key
    )
    data["balance_sheet_statement"] = fa.balance_sheet_statement(
        ticker, api_key, period="annual"
    ).drop(labels=["calendarYear", "period", "link", "finalLink"], axis=0)
    data["balance_sheet_statement_growth"] = famods.balance_sheet_statement_growth(
        ticker, api_key
    )
    data["discounted_cash_flow"] = famods.discounted_cash_flow(ticker, api_key)
    data["advanced_discounted_cash_flow"] = famods.advanced_discounted_cash_flow(
        ticker, api_key
    )
    data[
        "advanced_levered_discounted_cash_flow"
    ] = famods.advanced_levered_discounted_cash_flow(ticker, api_key)
    data["key_metrics"] = fa.key_metrics(ticker, api_key, period="annual").drop(
        ["period"]
    )
    data["financial_ratios"] = fa.financial_ratios(
        ticker, api_key, period="annual"
    ).drop(["period"])
    data["growth"] = fa.financial_statement_growth(
        ticker, api_key, period="annual"
    ).drop(["period"])
    data["owner_earnings"] = famods.owner_earnings(ticker, api_key)
    data["enterprise_values"] = famods.enterprise_values(ticker, api_key)

    try:
        data["dividends"] = fa.stock_dividend(ticker, api_key).drop(
            ["recordDate", "declarationDate"], axis=1
        )
    except:
        pass

    try:
        data["scores"] = famods.score(ticker, api_key)
    except:
        pass

    # try:
    #     data['income_statement'].drop(labels=['calendarYear', 'period', 'link', 'finalLink'], axis=0)
    #     data['cashflow_statement'].drop(labels=['calendarYear', 'period', 'link', 'finalLink'], axis=0)
    #     data['balance_sheet_statement'].drop(labels=['calendarYear', 'period', 'link', 'finalLink'], axis=0)
    #     data['key_metrics'].drop(['period'])
    #     data['financial_ratios'].drop(['period'])
    #     data['growth'].drop(['period'])
    #     data['dividends'].drop(['recordDate', 'declarationDate'], axis=1)
    # except:
    #     pass

    return data


def fmp_request(api: str, ticker: str, api_key, v4: bool = False):
    """
    Sends an API request to financialmodelingprep.com, converting the response to a df

        Parameters:
            api (str):     The API to query, e.g. 'income-statement'
            ticker (str):  The tickername to query, e.g 'MSFT'
            api_key (str): Your fmp API key

        Returns:
            dataframe
    """
    if v4:
        url = f"https://financialmodelingprep.com/api/v4/{api}?symbol={ticker}&apikey={api_key}"
    else:
        url = (
            f"https://financialmodelingprep.com/api/v3/{api}/{ticker}?apikey={api_key}"
        )
    return pd.read_json(url)
