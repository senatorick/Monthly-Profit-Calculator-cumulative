import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import random

# Initialize Streamlit dashboard
st.title("Monthly Profit Calculator")

# Step 1: Input fields
investment = st.number_input("Enter your initial investment (e.g., 100 USDT):", min_value=0.0, value=100.0)
ror = st.number_input("Enter the Risk to Reward ratio (e.g., 2):", min_value=0.0, value=2.0)
risk_percentage = st.number_input("Enter your risk percentage (daily loss in %):", min_value=0.0, max_value=100.0, value=3.0)
win_rate = st.number_input("Enter your monthly win rate (in %):", min_value=0.0, max_value=100.0, value=40.0)
avg_trades_per_day = st.number_input("Enter the average number of trades per day:", min_value=1, value=1)
num_months = st.number_input("Enter the number of months to simulate:", min_value=1, value=25)

# Step 2: Monthly profit calculation
# Prepare initial variables
monthly_balances = []
cumulative_balance = investment
days_in_month = 30

# Step 3: Simulate win/loss based on the win rate
total_trades = days_in_month * avg_trades_per_day
num_wins = int((win_rate / 100) * total_trades)  # Calculate the number of wins based on the win rate
num_losses = total_trades - num_wins  # The rest are losses

# Create a list of 'Win' and 'Lose' based on the win rate
trade_results = ['Win'] * num_wins + ['Lose'] * num_losses
random.shuffle(trade_results)  # Shuffle the list so the wins/losses are random across the days

# Step 4: Calculate monthly balance
for month in range(1, num_months + 1):
    for result in trade_results:
        # Recalculate risk and reward based on the current balance
        risk_amount = (risk_percentage / 100) * cumulative_balance
        reward_amount = ror * risk_amount

        # Apply win/loss with the proper loss limit
        if result == 'Win':
            cumulative_balance += reward_amount
        else:  # Lose, but ensure the loss is capped at 3% of the current balance
            cumulative_balance -= min(risk_amount, (risk_percentage / 100) * cumulative_balance)

    # Record end-of-month balance
    monthly_balances.append((month, cumulative_balance))

# Step 5: Display results
st.subheader("Monthly Balances")
df = pd.DataFrame(monthly_balances, columns=["Month", "Balance"])
st.table(df)

# Step 6: Plot results
st.subheader("Balance Growth Over Time")
plt.figure(figsize=(10, 5))
plt.plot(df["Month"], df["Balance"], marker="o", linestyle="-", color="b")
plt.title("Balance Growth Over Time")
plt.xlabel("Month")
plt.ylabel("Balance (USDT)")
plt.grid()
st.pyplot(plt)
