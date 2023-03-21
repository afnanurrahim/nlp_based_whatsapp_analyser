import get_dataframe
f=open('/Users/afnan/Downloads/AIMLChats.txt',encoding='utf-8')
content = f.read()
info_df=get_dataframe.create_dataframe(content).df_table()
print(info_df)