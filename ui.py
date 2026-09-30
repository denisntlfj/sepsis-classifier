import streamlit as st
from analysis import DataSet
#import storage_handler
#import os
#import sys
import streamlit as st

data_file = st.file_uploader('Выберите файл',
                             help='Target - первый столбец, 1 - Сепсис, 0 - Не сепсис',
                             type = ['csv'],)

if data_file is None:
    st.error("Не выбран файл с данными")
else:
    ds = DataSet(data_file)

    #if st.toggle('Показать отчёт модели'):
    st.code(ds.report())

    with st.container(border=True):
        st.markdown('Ввод данных тестируемого пациента:')
        sample = ds.sample()
        tested_patient = st.data_editor(
                sample,
                num_rows = 'fixed',
                use_container_width = True,
                hide_index = True,)

        if st.button('Спрогнозировать'):
            tp_vector = tested_patient.to_numpy()
            prediction = ds.predict(tp_vector)
            if prediction == 1:
                st.write('Прогноз: **Сепсис**')
            else:
                st.write('Прогноз: **Не сепсис**')

#    if st.toggle('Редактор данных'):
#        with st.container(border=True):
#
#            edited_df = st.data_editor(qda.df,num_rows='dynamic',key='data')
#
#
#            col1,col2 = st.columns(2,
#                                   vertical_alignment = 'center')
#            with col1:
#                st.download_button(
#                    label = 'Экспорт таблицы',
#                    data = edited_df.to_csv(),
#                    file_name='saved_data.csv',
#                    use_container_width=True,)
#            with col2:
#                if st.button('Сохранить как по-умолчанию',
#                             use_container_width=True,):
#                    try:
#                        edited_df.to_csv("data.csv", index=False)
#                        st.success('База данных успешно обновлена')
#                        st.rerun()
#                    except Exception as e:
#                        st.error(f'Не удалось сохранить файл. Ошибка: {e}')

