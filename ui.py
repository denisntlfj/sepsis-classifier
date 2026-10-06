import streamlit as st
from analysis import DataSet
if 'prediction' not in st.session_state:
    st.session_state['prediction'] = -1
if 'tested_is_calculated' not in st.session_state:
    st.session_state['tested_is_calculated'] = False
if 'dataset_is_edited' not in st.session_state:
    st.session_state['dataset_is_edited'] = False

def reset_tested_status():
    st.session_state['tested_is_calculated'] = False
def set_dataset_edited():
    st.session_state['dataset_is_edited'] = False


data_file = st.file_uploader('Выберите файл',
                             help='Target - первый столбец, 1 - Сепсис, 0 - Не сепсис',
                             type = ['csv'],)

if data_file is None:
    st.error('Не выбран файл с данными')
else:
    ds = DataSet(data_file)

    if st.session_state['dataset_is_edited']:
        st.code(ds.report())
        st.session_state['dataset_is_edited'] = True

    #prediction block
    with st.container(border = True):
        st.markdown('Ввод данных тестируемого пациента:')

        sample = ds.sample()


        tested_patient = st.data_editor(
                sample,
                num_rows = 'fixed',
                use_container_width = True,
                hide_index = True,
                on_change = reset_tested_status,
                )


        col1,col2 = st.columns(2,
                                    vertical_alignment = 'center')
        with col1:
            if st.button('Раcсчитать',width = 'stretch'):
                tp_vector = tested_patient.to_numpy()
                st.session_state['prediction'] = ds.predict(tp_vector)
                st.session_state['tested_is_calculated'] = True
        with col2:
            if st.session_state['tested_is_calculated']:
                if st.session_state['prediction'] == 1:
                    st.write('Прогноз: **Сепсис**', )
                else:
                    st.write('Прогноз: **Не сепсис**', )

        #dataset table block
        with st.container(border = True):
            edited_df = st.data_editor(ds.df,
                                       num_rows = 'dynamic',
                                       hide_index = False,
                                       on_change = set_dataset_edited,
                                       )
            col1,col2,col3 = st.columns(3,
                                   vertical_alignment = 'center')
            with col1:
                if st.button('Пересчитать',width = 'stretch'):
                    pass
            with col2:#load from file
                if st.button('Отменить изменения',width = 'stretch'):
                    pass
            with col3:
                if st.button('Сохранить файл',width = 'stretch'):
                    pass
