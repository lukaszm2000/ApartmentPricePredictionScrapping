from matplotlib.ticker import FuncFormatter
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

@st.cache_data()
def load_data():
    df = pd.read_csv(r'C:\Users\Lukasz\Desktop\Project - Otodom\offers_details_2_cleaned.csv')
    return df

def main():

    st.title('Dashboard - mieszkania')

    df = load_data()

    def format_number(x,decimals=0):
        return f"{x:.{decimals}f}" if pd.notnull(x) else ""
      

    st.write('### Szczegóły ofert mieszkaniowych:')
    st.dataframe(df.style.format({
        'Rok budowy': lambda x: format_number(x, 0),
        'Cena': lambda x: format_number(x, 0),
        'Cena [zł/m²]': lambda x: format_number(x, 0),
        'Powierzchnia': lambda x: format_number(x,0),
        'Czynsz': lambda x: format_number(x,0)
    }))

    st.write('### Ilość mieszkań w danej dzielnicy')
    apartments_count = df['Dzielnica'].value_counts().reset_index()
    apartments_count.columns = ['Dzielnica','Ilość']
    fig,ax = plt.subplots(figsize=(10,6))
    sns.barplot(apartments_count,x='Dzielnica',y='Ilość',hue='Dzielnica')
    plt.xticks(rotation = 90)
    st.pyplot(fig)

    st.write('### Średnia cena za m² w danej dzielnicy')
    price_by_district = df.groupby('Dzielnica')['Cena [zł/m²]'].mean().reset_index()
    price_by_district.sort_values(by='Cena [zł/m²]',ascending=False,inplace=True)
    price_by_district.columns = ['Dzielnica','Średnia cena za m² [zł/m²]']
    fig,ax = plt.subplots(figsize=(10,6))
    sns.barplot(price_by_district,x='Dzielnica',y='Średnia cena za m² [zł/m²]',hue='Dzielnica')
    plt.xticks(rotation = 90)
    st.pyplot(fig)

    st.write('### Średnia cena mieszkania wedłgu typu ogłoszeniodawcy')
    price_by_advertiser = df.groupby('Typ ogłoszeniodawcy')['Cena'].mean().reset_index()
    price_by_advertiser.sort_values(by='Cena',ascending=False,inplace=True)
    price_by_advertiser.columns = ['Typ ogłoszeniodawcy','Średnia cena']
    fig,ax = plt.subplots(figsize=(10,6))
    sns.barplot(price_by_advertiser,x='Typ ogłoszeniodawcy',y='Średnia cena',hue='Typ ogłoszeniodawcy')
    plt.xticks(rotation = 90)
    ax.yaxis.set_major_formatter(FuncFormatter(lambda x, _: f'{int(x):,}'.replace(',', ' ')))
    st.pyplot(fig)

    st.write('### Średnia cena za m² w zależności od rodzaju zabudowy')
    price_by_building = df.groupby('Rodzaj zabudowy')['Cena [zł/m²]'].mean().reset_index()
    price_by_building.sort_values(by='Cena [zł/m²]',ascending=False,inplace=True)
    price_by_building.columns = ['Rodzaj zabudowy','Średnia cena']
    fig,ax = plt.subplots(figsize=(10,6))
    sns.barplot(price_by_building,x='Rodzaj zabudowy',y='Średnia cena',hue='Rodzaj zabudowy')
    plt.xticks(rotation = 90)
    st.pyplot(fig)

    st.write('### Średnia cena za m² w zależności od rynku ')
    price_by_market = df.groupby('Rynek')['Cena [zł/m²]'].mean().reset_index()
    price_by_market.sort_values(by='Cena [zł/m²]',ascending=False,inplace=True)
    price_by_market.columns = ['Rynek','Średnia cena']
    fig,ax = plt.subplots(figsize=(10,6))
    sns.barplot(price_by_market,x='Rynek',y='Średnia cena',hue='Rynek')
    plt.xticks(rotation = 90)
    st.pyplot(fig)

    st.write('### Rozkład ceny mieszkań')
    fig,ax = plt.subplots(figsize=(10,6))
    sns.histplot(df['Cena'],bins=20)
    plt.xticks(rotation = 90)
    plt.ylabel('Ilość')
    ax.xaxis.set_major_formatter(FuncFormatter(lambda x, _: f'{int(x):,}'.replace(',', ' ')))
    st.pyplot(fig)

    st.write('### Rozkład liczby pokoi')
    fig,ax = plt.subplots(figsize=(10,6))
    sns.histplot(df['Liczba pokoi'],bins=7)
    plt.xticks(rotation = 90)
    plt.ylabel('Ilość')
    st.pyplot(fig)

    st.write('### Rozkład czynszu')
    fig,ax = plt.subplots(figsize=(10,6))
    sns.histplot(df['Czynsz'],bins=15)
    plt.xticks(rotation = 90)
    plt.ylabel('Ilość')
    st.pyplot(fig)

    st.write('### Rozkład roku budowy')
    fig,ax = plt.subplots(figsize=(10,6))
    sns.histplot(df['Rok budowy'],bins=300)
    plt.xticks(rotation = 90)
    plt.ylabel('Ilość')
    plt.xlim(1875,2025)
    st.pyplot(fig)

    st.write('### Procentowy podział budynków z windą i bez windy')
    wind_presence = df['Winda'].value_counts()
    labels = ['Z windą', 'Bez windy']
    sizes = wind_presence.values
    colors = ['#ff9999','#66b3ff']
    explode = (0.1, 0)
    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, explode=explode, labels=labels, colors=colors,
            autopct='%1.1f%%', shadow=True, startangle=90)
    ax1.axis('equal') 
    st.pyplot(fig1)

    st.write('### Procentowy podział mieszkań według rodzaju ogrzewania')
    heating_type = df['Ogrzewanie'].value_counts()
    labels = heating_type.index
    sizes = heating_type.values
    colors = sns.color_palette('pastel', len(labels))
    explode = (0.1,) + (0,) * (len(labels) - 1) 

    fig2, ax2 = plt.subplots()
    wedges, texts = ax2.pie(sizes, explode=explode, colors=colors, shadow=True, startangle=90, textprops=dict(color="w"))

    legend_labels = [f'{label} - {size/sum(sizes)*100:.2f}%' for label, size in zip(labels, sizes)]

    ax2.legend(wedges, legend_labels, title="Rodzaj ogrzewania", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))
    ax2.axis('equal')  

    st.pyplot(fig2)





if __name__ == '__main__':
    main()