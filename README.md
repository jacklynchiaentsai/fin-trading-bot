lumibot: easy algo trading framework
https://lumibot.lumiwealth.com/getting_started.html

Process:
- building strategy structure
- position sizing: cash at risk metric = how much of our cash balance do we want to risk at every trade
- incorporating informative news data
- develop ML algorithm for sentiment analysis
- incorporate ML predictions into trading strategy
    - if positive sentiment (expected increase in asset prices): close shorts, place buy
    - if negative sentiment (expected decrease in asset prices): close long, place sell
- interactive interfaces

technical challenge
1. leveraging the api: trial and error & debugging
2. continuously improvising trading strategy with the integration of new informative data:
- intially only relying on prices: limited -> cash management strategy stop loss and take profit
- dynamically incorporating new information (news: sentiment of the market) & data processing
    -> sentiment analysis: only want to trade on strong positive or negative sentiment (need proabability)
    1. NLTK that counts the occurence of positive & negative words --> doesn't consider context
    2. RNN that has vanishing gradient problem only considers short window of context
    3. finbert: BERT language model finetuned in finance domain for financial sentiment classification (https://huggingface.co/ProsusAI/finbert)

personal note:
- paper trading doen't include commission and fees
- short position: selling assets you don't own with the expctation of buying them back at a lower price (taking loans)
- long position: buying assets with the expectation of selling them at a higher price later