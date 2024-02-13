lumibot: easy algo trading framework
https://lumibot.lumiwealth.com/getting_started.html

Process:
- building strategy structure
- position sizing: cash at risk metric = how much of our cash balance do we want to risk at every trade


- interactive interfaces

technical challenge
1. leveraging the api: trial and error & debugging
2. continuously improvising trading strategy with the integration of new informative data:
- intially only relying on prices: limited -> cash management strategy stop loss and take profit
- dynamically incorporating new information (news: sentiment of the market) & data processing
    -> sentiment analysis
    1. NLTK that counts the occurence of positive & negative words --> doesn't consider context
    2. RNN that has vanishing gradient problem only considers short window of context
    3. finbert: BERT language model finetuned in finance domain for financial sentiment classification (https://huggingface.co/ProsusAI/finbert)