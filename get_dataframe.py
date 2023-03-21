import re
from textblob import TextBlob
import pandas as pd
import emoji

class create_dataframe:
    

    def __init__(self, content):
        self.content=content

        self.timestamps=[]
        self.txt_msg=[]
        self.sender=[]
        self.polarity=[]
        self.subjectivity=[]
        self.emoji_list=[]
        self.url_list=[]
        self.df = pd.DataFrame()
        

    def df_table(self):
        self.column_elements()

        self.df['Timestamp']=self.timestamps
        self.df['Sender']=self.sender
        self.df['Message']=self.txt_msg
        self.df['Polarity']=self.polarity
        self.df['Subjectivity']=self.subjectivity

        self.df['Timestamp']=pd.to_datetime(self.df['Timestamp'],format='%d/%m/%y, %I:%M %p - ')

        self.df['Date']=self.df['Timestamp'].dt.date
        self.df['Year']= self.df['Timestamp'].dt.year
        self.df['Month']= self.df['Timestamp'].dt.month_name()
        self.df['Day']= self.df['Timestamp'].dt.day
        self.df['Hour']= self.df['Timestamp'].dt.hour
        self.df['Weekday']= self.df['Timestamp'].dt.day_name()
        
        self.df['word_count'] = self.df['Message'].str.split().str.len()
        self.df['emoji']=self.emoji_list
        self.df['url']=self.url_list
        
        self.df=self.df[self.df['Sender']!='grp_info']
        self.df=self.df.dropna()
        return self.df

    def column_elements(self):
        pattern = "\d{2}[/-]\d{2}[/-]\d{2},\s\d{1,2}:\d{2}\s[a|p]m\s-\s" 
        messages = re.split(pattern, self.content)
        messages=messages[1:]  # 1st element is blank space

        self.timestamps=re.findall(pattern, self.content)

        sender_pattern="([\w\W]+?):\s"      #+91 77740 09408: / Pratik Agrawal: 
        url_pattern = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')

        for msg in messages:
            temp=re.split(sender_pattern,msg,maxsplit=1)    # maxsplit=1 so that if a same format is present in msg it won't split it
            if len(temp)>1:
                m=temp[2].replace("\n"," ")
                link = re.findall(url_pattern, m)
                if link:
                    m=re.sub(url_pattern, "", m)
                self.url_list.append(link)

                sentiment=TextBlob(m)
                # sentiment= sentiment.correct()  # spelling check
                
                self.txt_msg.append(m)
                p=round(sentiment.sentiment[0], 2)
                self.polarity.append(p)
                s=round(sentiment.sentiment[1], 2)
                self.subjectivity.append(s)
                self.sender.append(temp[1])
            else:
                m=temp[0].replace("\n"," ")
                self.txt_msg.append(m)
                self.url_list.append([])
                self.polarity.append(0)
                self.subjectivity.append(0)
                self.sender.append("grp_info")
        
        def extract_emojis(text):
            return [c for c in text if c in emoji.EMOJI_DATA]

        for msg in self.txt_msg:
            emojis=extract_emojis(msg)
            self.emoji_list.append(emojis)
        