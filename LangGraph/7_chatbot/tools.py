from langchain_core.tools import tool
from langchain_community.tools import DuckDuckGoSearchRun
import requests


# calculator tool
@tool
def calculator(first_num:float,second_num:float,operator:str) -> dict:
    """Perform arithmetic using add, sub, div, or mul.
    Always use this tool for numerical calculations instead of calculating mentally.
    """\
    
    try:
        if operator in ['add',"+"]:
            result =  first_num+second_num
        elif operator in ['sub',"-"]:
            result =  first_num - second_num
        elif operator in ['div',"/"]:
            if second_num == 0:
                 return  {'error':"division is not possible with 0"}
            else:
                result =  first_num/second_num
        elif operator in ['mul',"*"]:
            result =  first_num * second_num
        else:
            return {"error":f"no operator found"}

        return {"first_num":first_num,"second_num":second_num,"operator":operator,"result":result}
    except Exception as e:
        print(e)


# web search tool
search_tool = DuckDuckGoSearchRun(region='us-en')

# stock tool
@tool
def get_stock_price(symbol:str) -> dict:
    """fetch the latest price of the stock for a given symbol like(eg:AAPL,TSLA)"""
    url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey=KYHTK1K1JGC1DSFF"
    response = requests.get(url)
    return response.json()


# weather tool
@tool
def get_weather(city:str) -> dict:
    """Get the current weather for a specified city."""
    url = f"https://api.weatherstack.com/current?access_key=0f5e2ad544e78876200c6532e6a77de7&query={city}"
    response = requests.get(url)
    return response.json()