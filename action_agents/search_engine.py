import requests
from bs4 import BeautifulSoup
from urllib.parse import quote
import urllib.parse
import datetime
import re
from tavily import TavilyClient
from langchain.schema import Document
from utils.config import *
import httpx
import json
import http.client
from langchain_community.retrievers import ArxivRetriever
from model.models import tavily_engine
from utils.config import state_name_list, states_bank
from functools import reduce

tavily_client=tavily_engine()

class Search_API:
    @staticmethod
    def wikipedia_ko(query):
        try:
            return httpx.get("https://ko.wikipedia.org/w/api.php", params={
                "action": "query",
                "list": "search",
                "srsearch": query,
                "format": "json"
            }).json()["query"]["search"][0]["snippet"]
        except Exception as e: return None

    @staticmethod
    def wikipedia_en(query):
        try:
            return httpx.get("https://en.wikipedia.org/w/api.php", params={
                "action": "query",
                "list": "search",
                "srsearch": query,
                "format": "json"
            }).json()["query"]["search"][0]["snippet"]
        except Exception as e: return None

    @staticmethod
    def tavily(query):
        tavily_response = tavily_client.search(query=query,search_depth="advanced")
        tavily_response2 = tavily_client.qna_search(query=query, search_depth="advanced",max_results =3)
        web_results = "\n".join([d["content"] for d in tavily_response["results"]])
        web_results+=f"\n{tavily_response2}"
        # web_results = Document(page_content=web_results)
        return web_results

    @staticmethod
    def serper(query):
        serper_client = http.client.HTTPSConnection("google.serper.dev")
        payload = json.dumps({
          "q": query,
          "hl": "en",
          "num": 4,
          "page": 2
        })
        headers = {
          'X-API-KEY': SERPER_API_KEY,
          'Content-Type': 'application/json'
        }
        serper_client.request("POST", "/search", payload, headers)
        response_res = serper_client.getresponse()
        data = response_res.read()
        result=json.loads(data.decode("utf-8"))["organic"]
        
        search_res=""
        for r in result:
            title=r["title"]
            snippet=r["snippet"]
            search_res+=f"{title}: {snippet}\n"
        return search_res
        
    @staticmethod
    def arxiv(query):
        retriever = ArxivRetriever(
            # load_max_docs=1,
            get_ful_documents=True,
            top_k_results=2
        )
        docs = retriever.invoke(query)

        search_res=""
        for d in docs:
            title=d.metadata["Title"]
            page_content=d.page_content
            search_res+=f"{title}: {page_content}\n"

            return search_res

class NAVER_NEWS:
    def __call__(self,keyword):
        return self.search(keyword)
        
    def get_news_with_query(self, keyword):
        keyword=quote(keyword)
        url=f"https://search.naver.com/search.naver?where=news&query={keyword}&sm=tab_opt&sort=0&photo=3&field=0&pd=0&ds=&de=&docid=&related=0&mynews=0&office_type=0&office_section_code=0&news_office_checked=&nso=so%3Ar%2Cp%3Aall&is_sug_officeid=0&office_category=0&service_area=0" 
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        news_titles = []
        news_contents = []
        news_release_date = []
        naver_news_links=[]
        
        def parse_page(soup):
            for idx,info in enumerate(soup.find_all(class_='news_info')):
                if idx<5:
                    date=info.find_all('span',{"class":"info"})[1]
                    news_release_date.append(date.get_text().strip())
    
                    naver_news_link=info.find_all('a', {"class":"info"},href=True)[-1]
                    naver_news_links.append(naver_news_link['href'])
                
            for tit_idx,title in enumerate(soup.find_all(class_='news_tit')):
                if tit_idx<5:
                    news_titles.append(title.get_text().strip())
            for con_idx,content in enumerate(soup.find_all(class_='news_dsc')):
                if con_idx<5:
                    news_contents.append(content.get_text().strip())
    
        parse_page(soup)
        
        next_page_url = url+"#"
        response = requests.get(next_page_url, stream=True)
        response.raw.decode_content = True
        soup = BeautifulSoup(response.text, 'html.parser')
        parse_page(soup)
        return news_titles,news_contents,news_release_date,naver_news_links
    
    def news_crawling(self, naver_news_link):
        response = requests.get(naver_news_link, stream=True)
        response.raw.decode_content = True
        soup = BeautifulSoup(response.text, 'html.parser')
    
        articles=[]
        article = soup.select_one("#dic_area")
        for a in article:
            # print(a)
            articles.append(a.get_text())
        articles=[value for value in articles if value != ""]
        articles=[value for value in articles if value != "\n"]
        articles=articles[1:7]
        articles_str= "\n".join(articles)
        return articles_str
    
    def parse_date(self, date_str):
        now = datetime.datetime.now()
        if '전' in date_str:
            number, unit = re.match(r'(\d+)(\D+)', date_str).groups()
            number = int(number)
            
            if '시간' in unit:
                return now - datetime.timedelta(hours=number)
            elif '분' in unit:
                return now - datetime.timedelta(minutes=number)
            elif '일' in unit:
                return now - datetime.timedelta(days=number)
            elif '주' in unit:
                return now - datetime.timedelta(weeks=number)
            elif '개월' in unit or "달" in unit:
                return now - datetime.timedelta(days=number*30)
        else:
            date_str = date_str.rstrip('.')
            return datetime.datetime.strptime(date_str, "%Y.%m.%d")
    
    def get_news(self, news_titles,news_contents,news_release_date,naver_news_links):
        crawling_result=[]
        for title,content,date,link in zip(news_titles,news_contents,news_release_date,naver_news_links):
            try:
                article_source=self.news_crawling(link)
                res={"title":title,"date":date, "article_source":article_source}
                # res={"title":title,"content":article_source}
                crawling_result.append(res)
            except Exception as e: pass
        crawling_result = sorted(crawling_result, key=lambda x: self.parse_date(x['date']), reverse=True)
        return crawling_result
    
    def search(self, keyword):
        res=[]
        news_titles,news_contents,news_release_date,naver_news_links= self.get_news_with_query(keyword)
        crawling_res= self.get_news(news_titles,news_contents,news_release_date,naver_news_links)
        for idx,c in enumerate(crawling_res):# search result number control
            if idx==0:return c
        #     if idx<5:
        #         res.append(c)
        # return res

class NAVER_FINANCE:
    @staticmethod
    def finance():
        news_res=[]
        url ="https://finance.naver.com/news/mainnews.naver"
        response = requests.get(url)

        soup = BeautifulSoup(response.text, 'html.parser')
        # print(soup)
        news_titles = []
        for title in soup.find_all(class_='articleSubject'):
            news_titles.append(title.get_text().strip())

        news_contents = []
        for content in soup.find_all(class_='articleSummary'):
            news_contents.append(content.get_text().split('\n\t')[1].strip())

        for idx,(t,c) in enumerate(zip(news_titles,news_contents)):
            if idx <5:
                news_res.append({'title': f"[최근 금융 시장 주요 뉴스] {t}", 'article_source': c})
        
        return news_res

    @staticmethod
    def finance_search(query):
        search_res=[]

        replacements={"\t":"",
                    "\n":""}
        replace_func = lambda text: reduce(lambda t, kv: t.replace(kv[0], kv[1]), replacements.items(), text)


        query=urllib.parse.quote(query.encode('euc-kr'))
        url=f"https://finance.naver.com/news/news_search.naver?q={query}"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        for news in soup.find_all(class_='newsList'):
            article_subject=news.find_all('dd',{"class":"articleSubject"})
            article_summary=news.find_all('dd',{"class":"articleSummary"})
            for idx,(sub,sum) in enumerate(zip(article_subject,article_summary)):
                if idx <5:
                    search_res.append({"title":replace_func(sub.get_text().strip()), "article_source":replace_func(sum.get_text())})
        return search_res


    @staticmethod
    def finance_sise_top():
        news_res=[]
        url ="https://finance.naver.com/"
        response = requests.get(url)
    
        soup = BeautifulSoup(response.text, 'html.parser')
        table = soup.find('table', class_='tbl_home')
        
        rows = table.find('tbody').find_all('tr')
        
        table_data = []
        
        for row in rows:
            stock_name = row.find('th').get_text(strip=True)
            current_price = row.find_all('td')[0].get_text(strip=True)
            change = row.find_all('td')[1].get_text(strip=True)
            rate_of_change = row.find_all('td')[2].get_text(strip=True)
            
            table_data.append({
                '종목명': stock_name,
                '현재가': current_price,
                '전일대비': change,
                '등락률': rate_of_change
            })
    
        return table_data

    @staticmethod
    def finance_sise_top_global():
        url ="https://finance.naver.com/world/"
        response = requests.get(url)
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        data_list = soup.select('ul.data_lst li')
        
        results = []
        
        for item in data_list:
            title = item.select_one('dt a').text.strip()  # 제목
            value = item.select_one('dd.point_status strong').text.strip()  # 지수 값
            change = item.select_one('dd.point_status em').text.strip()  # 변화 값
            percentage_change = item.select_one('dd.point_status span').text.strip()  # 퍼센트 변화
            date = item.select_one('dd.date em').text.strip()  # 날짜
            
            # 정보를 딕셔너리로 저장
            result = {
                "지수명": title,
                "지수 값": value,
                "변동 값": change,
                "변동 퍼센트": percentage_change,
                "기준 날짜": date
            }
            
            results.append(result)

    @staticmethod
    def finance_stock_market():
        index_data=[]
        url ="https://finance.naver.com/"
        response = requests.get(url)
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        for area in soup.find_all('div', class_='heading_area'):
            index_name = area.find('a', class_='_stock_section').get_text(strip=True)
            index_value = area.find('span', class_='num').get_text(strip=True)
            change_value = area.find('span', class_='num2').get_text(strip=True)
            percentage_change = area.find('span', class_='num3').get_text(strip=True)
            
            index_data.append({
                'Index Name': index_name,
                'Index Value': index_value,
                'Change Value': change_value,
                'Percentage Change': percentage_change
            })
        return index_data

    @staticmethod
    def kor_base_interest_rate():
        url=f"https://search.naver.com/search.naver?sm=tab_sug.top&where=nexearch&ssc=tab.nx.all&query=%ED%95%9C%EA%B5%AD+%EA%B8%B0%EC%A4%80%EA%B8%88%EB%A6%AC+%EC%B6%94%EC%9D%B4&oquery=%EA%B8%B0%EC%A4%80%EA%B8%88%EB%A6%AC&tqi=ir78KsqptbNssDJYcJGssssss5N-333521&acq=%EA%B8%B0%EC%A4%80%EA%B8%88%EB%A6%AC%EC%B6%94%EC%9D%B4&acr=4&qdt=0"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        base_interest_rate=[]
        base_interest_rate_final=[]
        def parse_page(soup):
            for infos in soup.find_all(class_='cont_info'):
                info_list=infos.find_all('span',{"class":"text"})
                for info in info_list:
                    base_interest_rate.append(info.get_text().strip())

        parse_page(soup)

        for i in range(0, len(base_interest_rate), 3):
            base_interest_rate_final.append(base_interest_rate[i:i+3])

        final_res=""
        for r in base_interest_rate_final[1:]:
            txt=f"{r[0]} 기준 금리 {r[1]}"
            if r[2] == "-": txt += " 변동 없음"
            else: txt += r[2]
            final_res+= f"{txt}\n"
        
        return final_res

    @staticmethod
    def global_base_interest_rate(keyword):
        def find_state(keyword):
            key_list=[]
            for key, values in state_name_list.items():
                for value in values:
                    if value in keyword:
                        key_list.append(key)
            if len(key_list)!=0:
                return key_list
            else:
                return None

        global_base_interest_rate_final=[]
        def parse_page(soup):
            base_interest_rate=[]
            for infos in soup.find_all(class_='cont_info'):
                info_list=infos.find_all('span',{"class":"text"})
                for info in info_list:
                    base_interest_rate.append(info.get_text().strip())
            return base_interest_rate
            
        states=find_state(keyword)
        if states:
            for state in states:
                state_bank=states_bank[state]
                try:
                    query=quote(state_bank)
                    url=f"https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=0&ie=utf8&query={query}"
                    response = requests.get(url)
                    soup = BeautifulSoup(response.text, 'html.parser')
                
                    base_interest_rate=[]
                    base_interest_rate_final=[]
                    base_interest_rate=parse_page(soup)
        
                    for i in range(0, len(base_interest_rate), 3):
                        base_interest_rate_final.append(base_interest_rate[i:i+3])
                
                    final_res=""
                    for r in base_interest_rate_final[1:]:
                        txt=f"{r[0]} 기준 금리 {r[1]}"
                        if r[2] == "-": txt += " 변동 없음"
                        else: txt += r[2]
                        final_res+= f"{txt}\n"
                    if final_res=="":pass
                    else:
                        global_base_interest_rate_final.append({"state":state,"interest_rate":final_res})
                except Exception as e: pass

        return global_base_interest_rate_final