import datapackage
import pandas as pd


def load_cboe_volatility(data_url='https://datahub.io/core/finance-vix/datapackage.json'):
    # to load Data Package into storage
    package = datapackage.Package(data_url)

    # to load only tabular data
    resources = package.resources
    for resource in resources:
        if resource.tabular:
            data = pd.read_csv(resource.descriptor['path'])
    return data


def load_companies_data(data_url='https://datahub.io/core/s-and-p-500-companies/datapackage.json'):
    # to load Data Package into storage
    package = datapackage.Package(data_url)

    # to load only tabular data
    resources = package.resources
    for resource in resources:
        if resource.tabular:
            data = pd.read_csv(resource.descriptor['path'])

    return data


def load_company_financials(data_url='https://datahub.io/core/s-and-p-500-companies-financials/datapackage.json'):
    # to load Data Package into storage
    package = datapackage.Package(data_url)

    # to load only tabular data
    resources = package.resources
    for resource in resources:
        if resource.tabular:
            data = pd.read_csv(resource.descriptor['path'])

    return data