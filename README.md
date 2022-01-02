# TDC subscription creator for business self-service.

## Features
1. Choose the account numbers (can be customized based on available accounts)
2. Select desired plan for the subscription (based on the selection)
3. Customize the invoice remark that shows up for the numbers.
4. Multi-thread support to expediate the creation.

## Setup

##### Create the following files:
1. details.py - email and password for the self service.
2. accounts.py - available account numbers.
3. plans.py - available plans.
4. numbers.txt - list of SIM card numbers to be created, separated by a new line

##### Adjust the necessary plan/account/invoice remark in main.py file: