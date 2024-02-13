import streamlit as st
import pandas as pd
import subprocess

popular_symbols = ["AAPL", "GOOGL", "MSFT", "AMZN", "TSLA", "SPY"]

def main():
    st.title("SentixTrade: Your AI Stock Trading Assistant")
    # Instructional feature boxes in the main area
    col1, col2 = st.columns(2)

    with col1:
        st.info("**Sentiment Analysis Driven 🧐**\n\n SentixTrade dyamically adjusts trading strategy based on accurate sentiment analysis of financial news")

    with col2:
        st.info("**Disclaimer ⚠️** \n\n SentixTrade currently supports paper trading simulation and analysis, which does not include commission and fees")

    # Get user input for start date, end date, and symbol
    start_date = st.date_input("Select start date", pd.to_datetime('today') - pd.to_timedelta(365, unit='d'))
    end_date = st.date_input("Select end date", pd.to_datetime('today'))
    symbol = st.selectbox("Select symbol", popular_symbols, index=popular_symbols.index("SPY"))

    # Submit button to run tradingbot.py script
    if st.button("Run Trading Bot"):
        with st.spinner("Running Trading Bot..."):
            run_trading_bot(symbol, start_date, end_date)
        
        st.success("Indicator plot and tear sheet generated. Please visit the popup windows.")

def run_trading_bot(symbol, start_date, end_date):
    try:
        # Construct the command to run the tradingbot.py script with parameters
        command = ["python", "tradingbot.py", symbol, str(start_date), str(end_date)]
        
        # Run the script using subprocess
        subprocess.run(command, check=True)
        
    except subprocess.CalledProcessError as e:
        st.error(f"Error running the script: {e}")
    
    

if __name__ == "__main__":
    main()