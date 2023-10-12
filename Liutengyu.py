import requests
from html.parser import HTMLParser
import sys
import nlp_rake
from wordcloud import WordCloud
import matplotlib.pyplot as plt
url = 'https://encyclopedia.thefreedictionary.com/DATA'
text = requests.get(url,timeout=500).content.decode('utf-8')
print(text[:1000])
class MyHTMLParser(HTMLParser):
    script = False
    res = ""
    def handle_starttag(self, tag, attrs):
        if tag.lower() in ["script","style"]:
            self.script = True
    def handle_endtag(self, tag):
        if tag.lower() in ["script","style"]:
            self.script = False
    def handle_data(self, data):
        if str.strip(data)=="" or self.script:
            return
        self.res += ' '+data.replace('[ edit ]','')
parser = MyHTMLParser()
parser.feed(text)
text = parser.res
print(text[:1000])
extractor = nlp_rake.Rake(max_words=2,min_freq=3,min_chars=5)
res = extractor.apply(text)
res
plt.gcf().subplots_adjust(left=0.05,top=0.91,bottom=0.09)

plt.rcParams['font.family'] = ['Arial', 'Helvetica', 'Times New Roman']
plt.rcParams['axes.unicode_minus'] = False

def plot(pair_list):
    plt.figure(figsize=(12,6)).patch.set_facecolor('white')
    k,v = zip(*pair_list)
    plt.bar(range(len(k)),v)
    plt.xticks(range(len(k)),k,rotation='vertical',fontsize=16)
    plt.tight_layout()
    plt.savefig('SHUJU.png',dpi=600)
    plt.show()
plot(res[:20])
wc = WordCloud(background_color='white',width=800,height=600)
plt.figure(figsize=(15,7)).patch.set_facecolor('white')
plt.imshow(wc.generate_from_frequencies({ k:v for k,v in res }))
plt.figure(figsize=(15,7)).patch.set_facecolor('white')
plt.imshow(wc.generate(text))
wc.generate(text).to_file('CIYUN.png')