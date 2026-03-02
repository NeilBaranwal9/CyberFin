import pandas as pd

cyber = pd.read_csv('cyber_events.csv')
txns = pd.read_csv('transactions.csv')

print(f'✅ Cyber Events: {len(cyber)} rows')
print(cyber.head())
print(f'\n✅ Transactions: {len(txns)} rows')
print(txns.head())
print(f'\n📊 Event Types Distribution:')
print(cyber['event_type'].value_counts())
print(f'\n🌍 Location Distribution:')
print(cyber['location'].value_counts())
print(f'\n💰 Transaction Amount Stats:')
print(txns['amount'].describe())
