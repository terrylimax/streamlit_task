# импортируем библиотеку streamlit
import streamlit as st
import pandas as pd
from streamlit import session_state as ss
import base64

#if st.button('Click me!'):
    #st.write('Hello, AI Student! :pig:')
    
def open_data(path="Data/train.csv"):
    df = pd.read_csv(path)
    df = df[['LotShape', "LotArea", "BldgType", "HouseStyle", "YearRemodAdd", "RoofStyle", "BsmtCond"]]
    return df

def sidebar_input_features(df):
    st.sidebar.header('Введите параметры жилья')
    options = st.sidebar.multiselect('Общая форма собственности', ['Regular', 'Slightly irregular', 'Moderately Irregular', 'Irregular'])
    start, end = st.sidebar.slider('Размер участка в квадратных футах',df['LotArea'].min(), df['LotArea'].max(), (df['LotArea'].min(), int(df['LotArea'].max()*3/4)))
    selected_years = st.sidebar.multiselect('Год ремонта', sorted(df['YearRemodAdd'].unique().tolist()))
    roof_choice = st.sidebar.radio("Выберите тип крыши", df['RoofStyle'].unique())
    dwelling_type = st.sidebar.number_input("Введите номер типа жилья", 1, 5)
    house_style_choices = ["One story", "One and one-half story: 2nd level finished", 
            "One and one-half story: 2nd level unfinished","Two story",
            "Two and one-half story: 2nd level finished",
            "Two and one-half story: 2nd level unfinished",
            "Split Foyer",
            "Split Level"]
    house_style_choice = st.sidebar.selectbox('Стиль дома', house_style_choices)
    translation = {
        "LotShape": {
            "Regular": "Reg",
            "Slightly irregular": "IR1",
            "Moderately Irregular": "IR2",
            "Irregular": "IR3"},
        "HouseStyle": {
            "One story": "1Story",
            "One and one-half story: 2nd level finished": "1.5Fin",
            "One and one-half story: 2nd level unfinished": "1.5Unf",
            "Two story": "2Story",
            "Two and one-half story: 2nd level finished": "2.5Fin",
            "Two and one-half story: 2nd level unfinished": "2.5Unf",
            "Split Foyer": "SFoyer",
            "Split Level": "SLvl"},
        "DwellingType": {
            1: "1Fam",
            2: "2FmCon",
            3: "Duplx",
            4: "TwnhsE",
            5: "TwnhsI"
        }
    }
    
    # Преобразуем выбранные опции в соответствующие значения для DataFrame
    lot_shapes = [translation["LotShape"][option] for option in options]
    # Преобразуем выбранные опции в соответствующие значения для DataFrame
    style_shape = translation["HouseStyle"][house_style_choice]
    # Фильтруем DataFrame по выбранным опциям и диапазону слайдера
    if options:
        df = df[df['LotShape'].isin(lot_shapes)]
    if start > df['LotArea'].min() or end < df['LotArea'].max():
        df = df[(df['LotArea'] >= start) & (df['LotArea'] <= end)]
    if house_style_choice:
        df = df[df['HouseStyle'] == style_shape] # фильтруем данные по стилю дома
    if selected_years:
        df = df[df['YearRemodAdd'].isin(selected_years)]
    if roof_choice:
        df = df[df['RoofStyle'] == roof_choice]
    if dwelling_type:
        df = df[df['BldgType'] == translation["DwellingType"][dwelling_type]]
    return df


def download_csv(filtered_df):
# Сохранение отфильтрованного DataFrame в CSV
    csv = filtered_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        "Скачать отфильтрованный список в CSV",
        csv,
        file_name="data.csv",
        mime="text/csv"
    )

def process_side_bar_inputs():
    # Открываем данные и сохраняем в переменную df
    df = open_data()
    # Пример использования функции
    if 'start_df' not in st.session_state:
        st.session_state.start_df = df # сохраняем данные в состоянии сессии

    filtered_df = sidebar_input_features(st.session_state.start_df) # фильтруем данные

    st.write(filtered_df) # выводим отфильтрованные данные


if __name__ == "__main__":
    process_side_bar_inputs()