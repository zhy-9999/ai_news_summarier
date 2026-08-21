class ai_news_summarizer():
    def __init__(self,**kwargs)->None:
        self.get_url = kwargs['get_url']
        self.token = kwargs['token']
        self.ai_url = kwargs['ai_url']
        self.api_key = kwargs['api_key']
        self.ai_model = kwargs['ai_model']
    def get(self)->str:
        import requests
        info = { 'token':self.token }
        req = requests.get(self.get_url, timeout=30, params=info)
        self.raw_news = str(req.text)
        # print(req.status_code)
        if req.status_code == 200:
            return self.raw_news
        else:
            return ''

    def summary(self,*raw:str)->str:
        from openai import OpenAI
        if raw:
            self.raw_news = str(raw)
        client = OpenAI(
            base_url = self.ai_url,
            api_key = self.api_key
        )
        messages = [
            {"role": "system", "content": '按新闻格式总结用户发来的源文件，按重要性排序并概括近1个月内的事件，输出约1000字'},
            {"role": "user", "content": self.raw_news}
        ]
        response = client.chat.completions.create(
            model = self.ai_model,
            messages = messages # type: ignore
        )

        return str(response.choices[0].message.content)
if __name__ == '__main__':
    try:
        import json
        with open('config.json','r',encoding='utf-8') as f:
            config = json.loads(f.read())  
        summarize = ai_news_summarizer(**config)
        raw_news = summarize.get()
        if raw_news:
            with open('raw_news.txt','w',encoding='utf-8') as f:
                f.write(raw_news)
        else:
            with open('raw_news.txt','r',encoding='utf-8') as f:
                summarize.raw_news = f.read()
        summ = summarize.summary()
        with open('summaries.txt','w',encoding='utf-8') as f:
            f.write(summ)
    except Exception as e:
        from log import log
        log(0,str(e))